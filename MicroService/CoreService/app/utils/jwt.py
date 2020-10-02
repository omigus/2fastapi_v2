from functools import wraps
from sanic.response import json
import os
import jwt

def authorized():
	def decorator(f):
		@wraps(f)
		async def decorated_function(request, *args, **kwargs):
			token = await check_request_for_authorization_status(request)
			if token:
				access_token = token.split(" ")[1]
				try:
					current_user =  jwt.decode(access_token, os.getenv('SECRET_KEY') )
				except Exception as e :
					return json({'status': 'not_authorized'}, 401)
				response = await f(request,current_user, *args, **kwargs)
				return response
			else:
				return json({'status': 'not_authorized'}, 401)
		return decorated_function
	return decorator


async def check_request_for_authorization_status(request):
	token = None
	if "Authorization" in request.headers:
		token = request.headers["Authorization"]
		return token
	else:
		return None