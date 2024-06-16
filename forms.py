import pandas as pd
from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    DateField,
    TimeField,
    IntegerField,
    SubmitField
)
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError


# # getting the data
# train = pd.read_csv("data/train.csv")
# val = pd.read_csv("data/val.csv")
# X_data = pd.concat([train, val], axis=0).drop(columns="price")

class InputForm(FlaskForm):
    tenure = IntegerField(
        label="Customer Tenure in Months",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Tenure must be a positive integer.")
        ]
    )
    is_monthly_contract = RadioField(
        label="Does Customer have Monthly Contract?",
        choices=[('No', 'No'), ('Yes', 'Yes')],
        validators=[DataRequired()]
    )
    availed_online_security = RadioField(
        label="Has Customer Availed Online Security?",
        choices=[('No', 'No'), ('Yes', 'Yes')],
        validators=[DataRequired()]
    )
    availed_tech_support = RadioField(
        label="Has Customer Availed Tech Support?",
        choices=[('No', 'No'), ('Yes', 'Yes')],
        validators=[DataRequired()]
    )
    availed_fiber_optic_internet_service = RadioField(
        label="Has Customer Availed Fiber Optic Internet Service?",
        choices=[('No', 'No'), ('Yes', 'Yes')],
        validators=[DataRequired()]
    )
    makes_electronic_check_payment = RadioField(
        label="Does Customer make Payment through Electronic Check?",
        choices=[('No', 'No'), ('Yes', 'Yes')],
        validators=[DataRequired()]
    )
    submit = SubmitField("Predict")


class LoginForm(FlaskForm):
    id = StringField(
        'Employee ID', 
        validators=[
            DataRequired(), 
            Length(min=10, max=10, message="ID must be exactly 10 characters long")
        ],
        render_kw={"pattern": "[A-Z]{5}[0-9]{5}", "title": "ID must be 5 uppercase letters followed by 5 numbers"}
    )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long")
        ],
        render_kw={"pattern": "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
                   "title": "Password must contain at least 1 letter, 1 number, and 1 special character"}
    )
    submit = SubmitField('Login')
