from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextField,
    TextAreaField,
    IntegerField,
    DateField,
    SelectField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class ExpenseForm(FlaskForm):
    expense_date = DateField("Date", validators=[DataRequired()])
    expense_detail = StringField("Expense Detail", validators=[DataRequired()])
    amount = IntegerField("Amount", validators=[DataRequired()])
    category_id = SelectField(
        u"Categories",
        validators=[DataRequired()],
        coerce=int
    )
    submit = SubmitField("Submit Expense")

class CategoryForm(FlaskForm):
    name = StringField("New Category", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Submit New Category")
