import os
from app.api.api import api
from prometheus_sanic import monitor
import logging
from app.core import create_app
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
app = create_app()


app.blueprint(api)


if __name__ == "__main__":
    monitor(app , endpoint_type="url").expose_endpoint()
    app.run(port=8000 , debug=True , workers=1 )