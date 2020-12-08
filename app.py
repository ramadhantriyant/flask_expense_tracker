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
from datetime import date
from models.categories import Categories
from models.expenses import Expenses
from models.users import Users
from models.datas import Datas
from login_manager import (
    login_manager,
    login_user,
    login_required,
    logout_user
)


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##################
##### ROUTES #####
##################

@app.route("/", methods=['GET', 'POST'])
def index_page():
    form = LoginForm()

    if form.validate_on_submit() and request.method == "POST":
        user = Users.find_by_username(form.username.data)

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
    top = Datas.top_expense_category(date.today().year, date.today().month)
    print(top)
    data = Expenses.last_5_expenses()
    line_chart = Expenses.last_6_month()
    total = []
    months = []
    sort_expenses = sorted(
        Expenses.find_per_month(
            date.today().year, date.today().month
        ),
        key=lambda x : x.amount,
        reverse=True
    )[0:5]
    list_expense_detail = [x.expense_detail for x in sort_expenses]
    list_amount = [x.amount for x in sort_expenses]

    for tot in line_chart:
        total.append(tot['total'])

    for mon in line_chart:
        months.append(mon['date'].strftime("%b %Y"))

    return render_template(
        "dashboard.html.j2",
        data=data,
        months=months,
        total=total,
        list_expense_detail=list_expense_detail,
        list_amount=list_amount
    )


@app.route("/expenses")
@login_required
def expenses():
    data = Datas.join_expense_category()
    return render_template(
        "expenses.html.j2",
        data=data
    )


@app.route("/new_expense", methods=['GET', 'POST'])
@login_required
def new_expense():
    categories = Categories.find_all()
    form = ExpenseForm(obj=categories)
    form.category_id.choices = [(cat.id, cat.name) for cat in categories]

    if form.validate_on_submit() and request.method == "POST":
        expense_date = form.expense_date.data
        category_id = form.category_id.data
        expense_detail = form.expense_detail.data
        amount = form.amount.data

        expense = Expenses(expense_date, category_id, expense_detail, amount)
        expense.save_to_db()

        flash("New expense was added successfully")

        return redirect(url_for("new_expense"))

    return render_template(
        "new_expense.html.j2",
        form=form
    )


@app.route("/expense/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expenses.find_by_id(id)

    if not expense:
        return render_template("404.html.j2")

    categories = Categories.find_all()
    form = ExpenseForm()
    form.category_id.choices = [(cat.id, cat.name) for cat in categories]

    if form.validate_on_submit() and request.method == "POST":
        expense.expense_date = form.expense_date.data
        expense.category_id = form.category_id.data
        expense.expense_detail = form.expense_detail.data
        expense.amount = form.amount.data

        expense.save_to_db()

        return redirect(url_for("expenses"))

    return render_template(
        "edit_expense.html.j2",
        form=form,
        expense=expense
    )


@app.route("/expense/delete/<int:id>")
@login_required
def delete_expense(id):
    expense = Expenses.find_by_id(id)
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


@app.route("/category/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Categories.find_by_id(id)

    if not category:
        return render_template("404.html.j2")

    form = CategoryForm()

    if form.validate_on_submit() and request.method == "POST":
        category.name = form.name.data
        category.description = form.description.data
        category.save_to_db()

        return redirect(url_for("categories"))

    return render_template(
        "edit_category.html.j2",
        form=form,
        category=category
    )


@app.route("/category/delete/<int:id>")
@login_required
def delete_category(id):
    category = Categories.find_by_id(id)
    category.delete_from_db()

    return redirect(url_for("categories"))


@app.route("/history")
@login_required
def history():
    total = []
    year_total = 0
    list_year = sorted([year for year in range(2019, date.today().year + 1)], reverse=True)

    try:
        search_year = int(request.args.get("year"))
    except:
        search_year = date.today().year

    if not search_year:
        search_year = date.today().year

    if search_year == date.today().year:
        for i in range(0, date.today().month):
            data_dict = Expenses.summary(search_year, date.today().month - i)
            total.append(data_dict)
            year_total = year_total + data_dict['total']
    elif search_year < date.today().year:
        for i in range(0, 12):
            data_dict = Expenses.summary(search_year, 12 - i)
            total.append(data_dict)
            year_total = year_total + data_dict['total']
    else:
        flash("Year is in the future!")
        search_year = date.today().year
        for i in range(0, date.today().month):
            data_dict = Expenses.summary(search_year, date.today().month - i)
            total.append(data_dict)
            year_total = year_total + data_dict['total']

    return render_template(
        "history.html.j2",
        total=total,
        search_year=search_year,
        list_year=list_year,
        year_total=year_total
    )


@app.route("/history_detail/<int:y>/<int:m>")
@login_required
def history_detail(y, m):
    tgl = date(year=y, month=m, day=1)
    data = Datas.join_expense_category_history(y, m)

    return render_template(
        "history_detail.html.j2",
        tgl=tgl,
        data=data
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
