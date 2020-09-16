import flask
import requests
import os

def create_storage(current_user_jwt_token,company_uuid):
        domain_name = os.getenv('DOMAIN_NAME')
        storage_service_url = domain_name + ':5005/api/v2/create_storage/' + company_uuid
        headers = {'Authorization': 'Bearer '+str(current_user_jwt_token)}
        r = requests.post(storage_service_url, headers=headers)
        return r.status_code 