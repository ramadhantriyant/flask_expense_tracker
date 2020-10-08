from app import db, Expenses, Users

db.create_all()

rama = Users("rama", "asdf")
adel = Users("adel", "asdf")

db.session.add_all([rama, adel])
db.session.commit()
