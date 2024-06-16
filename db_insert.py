from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees_db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    @validates('password')
    def validate_password(self, key, password):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            raise ValueError("Password must be at least 8 characters long and contain at least one letter, one number, and one special character.")
        return password

    def __repr__(self):
        return f"Employee('{self.id}', {self.name}')"

if __name__ == "__main__":
    with app.app_context():
        #db.create_all()
        mukund = Employee(id="BMISE00099", name="Mukund Rao", password="$MLGAPP42")
        monika = Employee(id="BMISE00097", name="Monika K", password="%APPMLG23")
        nidhi = Employee(id="BMISE00101", name="Nidhi S Adiga", password="#MLGMLG33")
        db.session.add_all([mukund,monika,nidhi])
        db.session.commit()
    #app.run(debug=True)
