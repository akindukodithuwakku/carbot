from flask import Flask , render_template,request
from Cars import car_data


app = Flask(__name__)


@app.route('/',methods = ["GET", "POST"])
def home():

    if request.method == "POST":
        carname = request.form.get("carname")
        return car_data(carname)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
