from flask import jsonify

def http_response(data):
  return jsonify({'status' : data[0] , 'payload' : data[1] }), data[2]