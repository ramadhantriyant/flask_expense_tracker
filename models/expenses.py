from db import db
from sqlalchemy import extract
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
        return f"Spent {self.amount} for {self.expense_detail} in {self.expense_date}"

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
        this_month = date.today().month
        this_year = date.today().year
        six_month_ago = this_month - 5

        if six_month_ago <= 0:
            six_month_ago = six_month_ago + 12
            last_year = this_year - 1

            for i in range(six_month_ago, 13):
                data.append(Expenses.summary(last_year, i))

            for i in range(1, this_month + 1):
                data.append(Expenses.summary(this_year, i))

        else:
            for i in range(six_month_ago, this_month + 1):
                data.append(Expenses.summary(this_year, i))
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
