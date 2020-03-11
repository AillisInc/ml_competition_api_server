import os
import json
from flask import Flask, request, jsonify, abort
from metrics_util import map_metrics as _map_metrics, auc_metrics as _auc_metrics
app = Flask(__name__)


def _parse_request_json():
    request_data = request.json
    y_pred = request_data['y_pred']
    y_true = request_data['y_true']
    return y_pred, y_true


@app.route('/')
@app.route('/health')
def health():
    return 'ok'


@app.route('/metrics/AUC', methods=['POST'])
def auc_metrics():
    if not authenticate_request(request):
        return jsonify({"message": "ERROR: Unauthorized"}), 401
    y_pred, y_true = _parse_request_json()
    if len(y_pred) != len(y_true):
        abort(422, 'len(y_pred) != len(y_true)')

    return jsonify({
        'metrics': _auc_metrics(y_true, y_pred)
    })


@app.route('/metrics/mAP', methods=['POST'])
def map_metrics():
    if not authenticate_request(request):
        return jsonify({"message": "ERROR: Unauthorized"}), 401
    y_pred, y_true = _parse_request_json()
    return jsonify({
        'metrics': _map_metrics(y_true, y_pred)
    })


@app.errorhandler(422)
@app.errorhandler(404)
def error_handler(error):
    response = jsonify({'message': error.description, 'code': error.code})
    return response, error.code


@app.errorhandler(Exception)
def server_error_handler(error):
    response = jsonify({'message': str(error), 'code': 500})
    return response, 500


def authenticate_request(request):
    headers = request.headers
    auth = headers.get("X-Authorization-Key")
    return auth == os.environ.get('API_KEY_TOKEN')


if __name__ == '__main__':
    app.run(port=os.environ.get('PORT') or 8000)
