from flask import Flask, render_template

app: Flask = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/viewer")
def index():
    return render_template("index.html")


def main():
    db.init_db()
    app.run(debug=False)


if __name__ == "__main__":
    main()
