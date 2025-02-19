from flask import *
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
# Home
@app.route("/pedindo")
def pedindo():
    return render_template("pedindo_Quentinha.html")    




if __name__ == "__main__":
    app.run(debug=True)
