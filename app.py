import pandas as pd
import joblib
from flask import Flask, url_for, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import InputForm, LoginForm
from werkzeug.security import check_password_hash
from db_create import Employee, db

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees_db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Load models
models = {
    "Logistic Regression": joblib.load("ccp_2_lr.joblib"),
    "Random Forest": joblib.load("ccp_2_rf.joblib"),
    "Support Vector Classifier": joblib.load("ccp_2_svc.joblib"),
    "K-Nearest Neighbors": joblib.load("ccp_2_knn.joblib"),
    "Decision Tree": joblib.load("ccp_2_dt.joblib"),
    "Voting Classifier": joblib.load("ccp_2_voting.joblib")
}

@app.route("/")
def home():
    flash("Welcome to the Customer Churn Prediction Portal!")
    return render_template("home.html", title="Home")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    form = InputForm()
    if form.validate_on_submit():
        x_new = pd.DataFrame(dict(
            tenure=[form.tenure.data],
            monthly_contract=[form.is_monthly_contract.data],
            online_security=[form.availed_online_security.data],
            tech_support=[form.availed_tech_support.data],
            fiber_optic_internet=[form.availed_fiber_optic_internet_service.data],
            electronic_check_payment=[form.makes_electronic_check_payment.data]
        ))

        predictions = {}
        for model_name, model in models.items():
            prediction = model.predict(x_new)[0]
            if prediction == 0:
                predictions[model_name] = "Customer is unlikely to Churn!"
            elif prediction == 1:
                predictions[model_name] = "Customer is likely to Churn!"
    else:
        predictions = {"": "Model Predictions will appear here"}

    return render_template("predict.html", title="Predict", form=form, predictions=predictions)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        employee_id = form.id.data
        password = form.password.data
        print(employee_id)
        print(password)
        employee = Employee.query.filter_by(id=employee_id).first()
        print(employee)
        
        if employee!=None:
            if employee.password == password:
                session["employee_id"] = employee.id
                flash("Login Successful!", "success")
                return redirect(url_for("predict"))
            else:
                print("Incorrect password for employee:", employee_id)
                flash("Login Failed. Incorrect ID or Password!", "danger")
        else:
            print("Employee not found:", employee_id)
            flash("Login Failed. Employee not Found!", "warning")
    
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    session.pop("employee_id", None)
    flash("You have been logged out.")
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

