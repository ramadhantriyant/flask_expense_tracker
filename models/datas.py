from datetime import date
from calendar import monthrange
from db import db
from models.categories import Categories
from models.expenses import Expenses

class Datas():

    def join_expense_category():
        this_month = date(
            year=date.today().year,
            month=date.today().month,
            day=1
        )

        return db.session.query(
            Expenses, Categories
        ).join(Categories).order_by(
            Expenses.id.desc()
        ).filter(Expenses.expense_date >= this_month)


    def join_expense_category_history(y, m):
        start_date = date(year=y, month=m, day=1)
        end_date = date(
            year=y,
            month=m,
            day=monthrange(y, m)[1]
        )

        return db.session.query(
            Expenses, Categories
        ).join(Categories).order_by(
            Expenses.id.desc()
        ).filter(
            Expenses.expense_date >= start_date
        ).filter(
            Expenses.expense_date <= end_date
        )


    def top_expense_category(y, m):
        this_month = date(
            year=date.today().year,
            month=date.today().month,
            day=1
        )

        explist = []

        categories = Categories.find_all()
        expenses = Expenses.find_all()

        for category in categories:
            explist.append({
                "category_id": category.id,
                "sum": Expenses.amount
            })

        # return expense
