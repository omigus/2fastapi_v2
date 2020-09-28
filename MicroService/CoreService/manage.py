import os
import unittest
from flask_script import Manager
from app.main import create_app
from app.main.controller.project_controller import ProjectService

app = create_app(os.getenv('ENV_STATE'))


app.app_context().push()
manager = Manager(app)

app.register_blueprint(ProjectService)


@manager.command
def run():
    app.run(port=6000 ,host="0.0.0.0")

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()