import os
from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    flash
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DateField,
    SelectField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"Username {username} exist in database"


class Expenses(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    expdetail = db.Column(db.Text)
    amount = db.Column(db.Integer)

    def __init__(self, date, expdetail, amount):
        self.date = date
        self.expdetail = expdetail
        self.amount = amount

    def __repr__(self):
        return f"Spent {amount} for {expdetail}"


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class ExpenseForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    expdetail = StringField("Expense Detail", validators=[DataRequired()])
    amount = IntegerField("Amount", validators=[DataRequired()])
    categories = SelectField(
        u"Categories",
        validators=[DataRequired()],
        choices=[
            ("fnb", "Food & Beverages"),
            ("transport", "Transportation"),
            ("groceries", "Groceries")
        ]
    )
    submit = SubmitField("Submit Expense")


@app.route("/", methods=['GET', 'POST'])
def index_page():
    form = LoginForm()

    if form.validate_on_submit():
        session['username'] = form.username.data
        session['password'] = form.password.data

        if session['username'] == "asdf" and session['password'] == "asdf":
            return redirect(url_for("dashboard"))
        else:
            flash("Wrong credentials!")

        return redirect(url_for("index_page"))

    return render_template(
        "index.html.j2",
        form=form
    )


@app.route("/dashboard", methods=['GET'])
def dashboard():
    #print(session)
    return render_template(
        "dashboard.html.j2"
    )


@app.route("/new_expense", methods=['GET', 'POST'])
def new_expense():
    form = ExpenseForm()

    if form.validate_on_submit():
        # session['date'] = form.date.data
        # session['expdetail'] = form.expdetail.data
        # session['amount'] = form.amount.data
        # session['categories'] = form.categories.data

        flash("Expense Saved Successfully")
        print(get_flashed_messages())

        # return redirect(url_for("new_expense"))
        return redirect(url_for("index_page"))

    return render_template(
        "new_expense.html.j2",
        form=form
    )


@app.route("/new_category")
def new_category():
    pass


@app.route("/history")
def history():
    return render_template(
        "history.html.j2"
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.html.j2'
    )


if __name__ == "__main__":
    app.run(port=80, debug=True)
