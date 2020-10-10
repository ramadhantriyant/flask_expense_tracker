import os
from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    request
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextField,
    TextAreaField,
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


class Categories(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    expense = db.relationship("Expenses", backref="categories", lazy="dynamic")

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Expenses(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    expense_detail = db.Column(db.Text)
    amount = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    def __init__(self, date, expense_detail, amount, category_id):
        self.date = date
        self.expense_detail = expense_detail
        self.amount = amount
        self.category_id = category_id

    def __repr__(self):
        return f"Spent {amount} for {expdetail}"


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class ExpenseForm(FlaskForm):
    def list_of_categories():
        categories = Categories.query.all()
        return [(cat.id, cat.name) for cat in categories]

    date = DateField("Date", validators=[DataRequired()])
    expense_detail = StringField("Expense Detail", validators=[DataRequired()])
    amount = IntegerField("Amount", validators=[DataRequired()])
    categories = SelectField(
        u"Categories",
        validators=[DataRequired()],
        choices=list_of_categories()
    )
    submit = SubmitField("Submit Expense")



class CategoryForm(FlaskForm):
    name = StringField("New Category", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Submit New Category")


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


@app.route("/expenses")
def expenses():
    return render_template(
        "expenses.html.j2"
    )

@app.route("/new_expense", methods=['GET', 'POST'])
def new_expense():
    form = ExpenseForm()

    if form.validate_on_submit():
        flash("Success")

        return redirect(url_for("expenses"))

    return render_template(
        "new_expense.html.j2",
        form=form
    )


@app.route("/categories")
def categories():
    categories = Categories.query.all()
    return render_template(
        "categories.html.j2",
        categories=categories
    )


@app.route("/new_category", methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()

    if form.validate_on_submit() and request.method == "POST":
        name = form.name.data
        description = form.description.data
        category = Categories(name, description)
        db.session.add(category)
        db.session.commit()
        flash("Success")
        return redirect(url_for("new_category"))

    return render_template(
        "new_category.html.j2",
        form=form
    )


@app.route("/category/edit/<int:id>")
def edit_category(id):
    form = CategoryForm()

    if form.validate_on_submit() and request.method == "POST":
        name = form.name.data
        description = form.description.data
        category = Categories(name, description)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))

    return render_template(
        "edit_category.html.j2",
        form=form
    )


@app.route("/category/delete/<int:id>")
def delete_category(id):
    category = Categories.query.get(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))


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
