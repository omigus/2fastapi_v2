
from functools import wraps
from flask import Flask, request, jsonify, make_response, Blueprint
import uuid 
import jwt
import json
from functools import wraps
import urllib 
import os
import requests

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        
        access_token = token.split(" ")[1]

        try:
            data = jwt.decode(access_token, os.getenv('SECRET_KEY'))
            current_user = data
        except Exception as e:
            return jsonify({"message": "Invalid Token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated
