from sanic import Blueprint
from app.api.projects.view import project_service

api = Blueprint.group(project_service,  url_prefix='/api/v2')