from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from send_email import send_message
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:0808@localhost/age_and_height_collector"
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    age_ = db.Column(db.Integer)
    height_ = db.Column(db.Integer)

    def __init__(self, email_, age_, height_):
        self.email_ = email_
        self.age_ = age_
        self.height_ = height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        age = request.form["age_name"]
        height = request.form["height_name"]
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, age, height)
            db.session.add(data)
            db.session.commit()
            # Extract the scalar value from the SQL query
            average_age = db.session.query(func.avg(Data.age_)).scalar()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_age = round(average_age, 2)
            average_height = round(average_height, 2)
            age_count = db.session.query(Data.age_).count()
            height_count = db.session.query(Data.height_).count()
            send_message(email, age, height, average_age, average_height, age_count, height_count)
            return render_template("success.html")
        return render_template("index.html", text="It appears we have information from that email address already!")


if __name__ == "__main__":
    app.debug = True
    app.run()