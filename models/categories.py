from db import db

class Categories(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    expense = db.relationship("Expenses", backref="categories", lazy="dynamic")

    def __init__(self, name):
        self.name = name
