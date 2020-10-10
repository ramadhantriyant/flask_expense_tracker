from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DateField,
    SelectField,
    PasswordField,
    BooleanField,
    SubmitField
)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class ExpenseForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    expdetail = StringField("Expense Detail", validators=[DataRequired()])
    amount = IntegerField("Amount", validators=[DataRequired()])
    categories = SelectField(
        u"Categories",
        validators=[DataRequired()],
        choices=[
            ("Food & Beverages", "Food & Beverages"),
            ("Transportation", "Transportation"),
            ("Groceries", "Groceries")
        ]
    )
    submit = SubmitField("Submit Expense")
