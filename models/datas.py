from db import db
from models.categories import Categories
from models.expenses import Expenses

class Datas():

    #@classmethod
    def join_expense_category():
        return db.session.query(Expenses, Categories).join(Categories).all()
