from db import db
from datetime import date

class Expenses(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    expense_date = db.Column(db.Date)
    expense_detail = db.Column(db.Text)
    amount = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    def __init__(self, expense_date, category_id, expense_detail, amount):
        self.expense_date = expense_date
        self.category_id = category_id
        self.expense_detail = expense_detail
        self.amount = amount

    def __repr__(self):
        return f"Spent {amount} for {expense_detail} in {expense_date}"

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_this_month(cls):
        this_month = date(year=date.today().year, month=date.today().month, day=1)
        return cls.query.filter(cls.expense_date >= this_month)

    @classmethod
    def last_5_expenses(cls):
        return cls.query.order_by(cls.id.desc()).limit(5)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
