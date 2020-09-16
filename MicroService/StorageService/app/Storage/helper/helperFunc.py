
from functools import wraps
from flask import Flask, request, jsonify, make_response, Blueprint
import uuid 
import jwt
import json
from functools import wraps
from app import SECRET_KEY, EndPoint
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
            data = jwt.decode(access_token, SECRET_KEY)
            print(data)
            current_user = data
        except Exception as e:
            print(e)
            return jsonify({"message": "Invalid Token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def root_dir():
    return os.path.abspath(os.path.dirname(__file__))

def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size
