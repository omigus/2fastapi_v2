import os
import unittest
from flask_script import Manager
from app.main import create_app
from app.main.controller.company_controller import CompanyService
from app.main.controller.member_controller import MemberService
from app.main.controller.team_controller import TeamService
app = create_app(os.getenv('ENV_STATE'))


app.app_context().push()
manager = Manager(app)

app.register_blueprint(CompanyService)
app.register_blueprint(MemberService)
app.register_blueprint(TeamService)


@manager.command
def run():
    app.run(port=5000 ,host="0.0.0.0")

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