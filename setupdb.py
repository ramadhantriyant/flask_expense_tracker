from app import db, Expenses, Users, Categories

db.create_all()

# groceries = Categories("Groceries", "Raw eggs, cooking oil, milk, etc")
# transport = Categories("Transportation", "Taxi, gas, parking fee, toll fee")
# fnb = Categories("Food & Beverages", "Breakfast, lunch, dinner")

# db.session.add_all([transport, groceries, fnb])
db.session.commit()
