from db import db

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
        return f"Spent {amount} for {expense_detail}"
