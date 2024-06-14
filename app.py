import pandas as pd
import joblib
from flask import (
    Flask,
    url_for,
    render_template
)
from forms import InputForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

model = joblib.load("ccp_1_lr.joblib")

@app.route("/")
@app.route("/home")
def home():
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
        prediction = model.predict(x_new)[0]
        if prediction == 0:
            message = "Customer will likely not Churn!"
        elif prediction ==1:
            message = "Customer will likely Churn!"
    else:
        message = "Please provide valid input details!"
    return render_template("predict.html", title="Predict", form=form, output=message)


if __name__ == "__main__":
    app.run(debug=True)