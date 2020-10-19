from app import app
from db import db
from login_manager import (
    login_manager,
    login_user,
    login_required,
    logout_user
)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

login_manager.init_app(app)
login_manager.login_view = "index_page"
# app.run()
