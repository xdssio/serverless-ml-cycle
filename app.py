import json
import logging

from flask import abort, Response, app

from ml.utils import get_pipeline

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

estimator = get_pipeline()


def response(response, status=200, json_dumps=True, mimetype='application/json'):
    if json_dumps:
        response = json.dumps(response)
    return Response(response=response, status=status, mimetype=mimetype)


def bad_request(message="", code=400):
    logger.debug("bad request: %s" % message)
    abort(code, description=message)


@app.route('/version', methods=['GET'])
def version(event=None, context=None):
    pass


@app.route('/versions', methods=['GET'])
def versions(event=None, context=None):
    pass


@app.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    logger.info('Lambda function invoked index()')
    logger.info('event: %s' % event)
    return response('live', mimetype='text/plain')


@app.route('/ping', methods=['GET', 'POST'])
def ping(event=None, context=None):
    logger.info('ping')
    health = True
    status = 200 if health else 404
    return response('ping', status=status, json_dumps=False)


def validate_input(json_data):
    pass


@app.route('/update', methods=['POST'])
def update(event=None, context=None):
    global estimator
    try:
        ret = None
    except Exception as e:
        logger.debug(e)
        ret = str(e)
    return response(ret, json_dumps=True)


@app.route('/invocations', methods=['GET', 'POST'])
def invocations(event=None, context=None):
    return recommend()


@app.route('/recommend', methods=['GET', 'POST'])
def recommend(event=None, context=None):
    try:
        ret = None

    except Exception as e:
        logger.debug(e)
        ret = str(e)

    return response(ret, json_dumps=False)


@app.route('/train', methods=['POST'])
def train(event=None, context=None):
    pass


if __name__ == '__main__':
    print('serving...')
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 8080)
    )
