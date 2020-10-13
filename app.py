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
from forms import LoginForm, ExpenseForm, CategoryForm
from models.categories import Categories
from models.expenses import Expenses
from models.users import Users
from login_manager import login_manager, login_user, login_required, logout_user

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##################
##### ROUTES #####
##################

@app.route("/", methods=['GET', 'POST'])
def index_page():
    form = LoginForm()

    if form.validate_on_submit() and request.method == "POST":
        user = Users.get_user(form.username.data)

        if user and user.check_credentials(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Wrong Credentials!")
        return redirect(url_for("index_page"))

    return render_template(
        "index.html.j2",
        form=form
    )


@app.route("/sign_out")
@login_required
def sign_out():
    logout_user()
    return redirect(url_for("index_page"))

@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    return render_template(
        "dashboard.html.j2"
    )


@app.route("/expenses")
@login_required
def expenses():
    data = db.session.query(Expenses, Categories).join(Categories).all()
    return render_template(
        "expenses.html.j2",
        data=data
    )

@app.route("/new_expense", methods=['GET', 'POST'])
@login_required
def new_expense():
    categories = Categories.query.all()
    form = ExpenseForm(obj=categories)
    form.category_id.choices = [(cat.id, cat.name) for cat in categories]

    if form.validate_on_submit() and request.method == "POST":
        date = form.date.data
        category_id = form.category_id.data
        expense_detail = form.expense_detail.data
        amount = form.amount.data

        expense = Expenses(date, category_id, expense_detail, amount)
        expense.save_to_db()

        flash("New expense was addess successfully")

        return redirect(url_for("new_expense"))

    return render_template(
        "new_expense.html.j2",
        form=form
    )


@app.route("/expense/edit/<int:id>")
@login_required
def edit_expense(id):
    return render_template(
        "expenses.html.j2"
    )


@app.route("/expense/delete/<int:id>")
@login_required
def delete_expense(id):
    expense = Expenses.query.get(id)
    expense.delete_from_db()

    return redirect(url_for("expenses"))


@app.route("/categories")
@login_required
def categories():
    categories = Categories.find_all()
    
    return render_template(
        "categories.html.j2",
        categories=categories
    )


@app.route("/new_category", methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()

    if form.validate_on_submit() and request.method == "POST":
        name = form.name.data
        description = form.description.data

        category = Categories(name, description)
        category.save_to_db()

        flash("New category was added successfully!")

        return redirect(url_for("new_category"))

    return render_template(
        "new_category.html.j2",
        form=form
    )


@app.route("/category/edit/<int:id>")
@login_required
def edit_category(id):
    form = CategoryForm()

    if form.validate_on_submit() and request.method == "POST":
        name = form.name.data
        description = form.description.data

        category = Categories(name, description)
        category.save_to_db()

        return redirect(url_for("categories"))

    return render_template(
        "edit_category.html.j2",
        form=form
    )


@app.route("/category/delete/<int:id>")
@login_required
def delete_category(id):
    category = Categories.query.get(id)
    category.delete_from_db()

    return redirect(url_for("categories"))


@app.route("/history")
@login_required
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
    from db import db

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = "index_page"
    app.run(port=80, debug=True)
