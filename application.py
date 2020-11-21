from app import app
from db import db
from login_manager import (
    login_manager,
    login_user,
    login_required,
    logout_user
)

application = app
db.init_app(application)

@application.before_first_request
def create_tables():
    db.create_all()

login_manager.init_app(application)
login_manager.login_view = "index_page"
