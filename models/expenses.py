from db import db


class Expenses(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    expense_detail = db.Column(db.Text)
    amount = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    def __init__(self, date, category_id, expense_detail, amount):
        self.date = date
        self.category_id = category_id
        self.expense_detail = expense_detail
        self.amount = amount

    def __repr__(self):
        return f"Spent {amount} for {expdetail}"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
