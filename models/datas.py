from datetime import date
from db import db
from models.categories import Categories
from models.expenses import Expenses

class Datas():

    def join_expense_category():
        this_month = date(year=date.today().year, month=date.today().month, day=1)
        return db.session.query(Expenses, Categories).join(Categories).order_by(Expenses.id.desc()).filter(Expenses.expense_date >= this_month)
