import json
import logging
from io import StringIO

import flask
import pandas as pd
from flask import abort, Response, app, request, make_response, Flask, jsonify

from ml.model import Model

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
model = Model.load()


def response(response, status=200, json_dumps=True, mimetype='application/json'):
    if json_dumps:
        response = json.dumps(response)
    return Response(response=response, status=status, mimetype=mimetype)


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
    try:
        if flask.request.content_type == 'text/csv':
            data = flask.request.data.decode('utf-8')
            s = StringIO(data)
            data = pd.read_csv(s)
            predictions = model.predict(data.head())
            df = pd.DataFrame({'results': predictions})
            resp = make_response(df.to_csv())
            resp.headers["Content-Disposition"] = "attachment; filename=predictions.csv"
            resp.headers["Content-Type"] = "text/csv"
            ret = resp
            return resp

        elif flask.request.content_type == 'application/json':
            j = request.get_json()
            data = pd.DataFrame(j)
            predictions = model.predict(data)
            df = pd.DataFrame({'results': predictions})
            result = json.dumps(df.to_json(orient='values'))
            resp = make_response(result)
            resp.headers["Content-Type"] = "application/json"
            ret = resp

            # ret = flask.Response(response=result, status=200, mimetype='application/json')

    except Exception as e:
        logger.debug(e)
        ret = str(e)

    return ret


@app.route('/train', methods=['POST'])
def train(event=None, context=None):
    logger.info('train')
    pass


if __name__ == '__main__':
    print('serving...')
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 8080)
    )
