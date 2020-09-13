import os
import unittest
from flask_script import Manager
from app.main import create_app
from app.main.controller.purchased_controller import PurchasedService
app = create_app(os.getenv('ENV_STATE'))


app.app_context().push()
manager = Manager(app)

app.register_blueprint(PurchasedService)




@manager.command
def run():
    app.run(threaded=True)

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