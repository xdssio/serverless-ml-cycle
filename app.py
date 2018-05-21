import json
import logging
from io import StringIO

import flask
import pandas as pd
from flask import abort, Response, request, make_response, Flask

from ml.model import Model
from ml.utils import get_settings_value, get_version

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
model_name = get_settings_value('model_name')
version = get_version(model_name)
model = Model.load(model_name=model_name, version=version)


def response(replay, status=200, json_dumps=True, mimetype='application/json'):
    if json_dumps:
        replay = json.dumps(replay)
    return Response(response=replay, status=status, mimetype=mimetype)


def bad_request(message="", code=400):
    logger.debug("bad request: %s" % message)
    abort(code, description=message)


@app.route('/version', methods=['GET'])
def version(event=None, context=None):
    return response(model.version)


@app.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    logger.info('Lambda function invoked index()')
    logger.info('event: %s' % event)
    return response('live', mimetype='text/plain')


@app.route('/ping', methods=['GET', 'POST'])
def ping(event=None, context=None):
    logger.info('ping')
    health = model is not None
    status = 200 if health else 404
    return response('ping', status=status, json_dumps=False)


@app.route('/update', methods=['POST'])
def update(event=None, context=None):
    global model
    # TODO
    try:
        ret = None
        # update_function_version()
    except Exception as e:
        logger.debug(e)
        ret = str(e)
    return response(ret, json_dumps=True)


@app.route('/predict', methods=['GET', 'POST'])
def predict(event=None, context=None):
    logger.info('predict')
    ret = None
    try:
        if flask.request.content_type == 'text/csv':
            data = flask.request.data.decode('utf-8')
            s = StringIO(data)
            data = pd.read_csv(s)
            predictions = model.predict(data)
            df = pd.DataFrame({'results': predictions})
            resp = make_response(df.to_csv())
            resp.headers["Content-Disposition"] = "attachment; filename=predictions.csv"
            resp.headers["Content-Type"] = "text/csv"
            ret = resp

        elif flask.request.content_type == 'application/json':
            j = request.get_json()
            data = pd.DataFrame(j)
            predictions = model.predict(data)
            df = pd.DataFrame({'results': predictions})
            result = json.dumps(df.to_json(orient='values'))
            resp = make_response(result)
            resp.headers["Content-Type"] = "application/json"
            ret = resp

    except Exception as e:
        logger.debug(e)
        ret = str(e)

    return ret


@app.route('/train', methods=['POST'])
def train(event=None, context=None):
    global model
    logger.info('train')
    model.fit()
    logger.info('done train model with v%d' % model.version)
    return make_response(flask.jsonify({"version": model.version}))


if __name__ == '__main__':
    print('serving...')
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 8080)
    )
