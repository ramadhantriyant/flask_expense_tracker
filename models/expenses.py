from db import db
from sqlalchemy import extract
from datetime import date, timedelta

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

    def summary(y, m):
        expenses = Expenses.find_per_month(y, m)
        total = 0

        for expense in expenses:
            total = total + expense.amount

        return {
            "date": date(year=y, month=m, day=1),
            "total": total
        }

    def last_6_month():
        data = []
        for i in range(0, 180, 30):
            the_date = date.today() - timedelta(days=i)
            data.append(Expenses.summary(the_date.year, the_date.month))

        return data

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_per_month(cls, y, m):
        return cls.query.filter(
            extract("year", cls.expense_date) == y
        ).filter(
            extract("month", cls.expense_date) == m
        ).all()

    @classmethod
    def last_5_expenses(cls):
        return cls.query.order_by(cls.id.desc()).limit(5)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
