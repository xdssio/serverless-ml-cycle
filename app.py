import json
import logging

import flask
import pandas as pd
from flask import abort, Response, request, make_response, Flask

import config
from ml.model import Model
from ml.utils import get_version

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
model_name = config.model_name
version = get_version(model_name)
#TODO cache
model = Model.load(model_name=model_name, version=version)


@app.route('/', methods=['POST'])
def live(event=None, context=None):
    return Response('live')


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


# @app.route('/', methods=['GET', 'POST'])
# def lambda_handler(event=None, context=None):
#     logger.info('Lambda function invoked index()')
#     logger.info('event: %s' % event)
#     return response('live', mimetype='text/plain')


@app.route('/ping', methods=['GET', 'POST'])
def ping(event=None, context=None):
    logger.info('ping')
    health = model is not None
    status = 200 if health else 404
    return response('ping', status=status, json_dumps=False)


@app.route('/predict', methods=['GET', 'POST'])
def predict(event=None, context=None):
    logger.info('flask.request.content_type: %s' % flask.request.content_type)
    try:
        data = request.get_data()
        if data is None:
            ret = response("missing data to predict", status=400)
        else:
            data = pd.DataFrame(json.loads(data))
            logger.debug('data- %s' % data)
            logger.info('data parsed')
            predictions = model.predict(data)
            logger.info('made predictions')
            predictions = pd.DataFrame({'prediction': predictions})
            predictions['index'] = range(len(predictions))
            logger.debug('predictions- %s' % predictions)
            result = predictions.to_json(orient='records', index=True)
            resp = response(result, json_dumps=False)
            resp.headers["Content-Type"] = "application/json"
            ret = resp

    except Exception as e:
        logger.debug(e)
        ret = response(str(e))

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
