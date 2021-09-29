from flask import Flask, render_template, request

app = Flask(__name__,template_folder="templates")

# rendering the html 
@app.route("/", methods=["GET"])
def index():
  return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
  if request.method == "POST":
    user = request.form["username"]
    return redirect(url_for("user", usr=user))
  else:
    return render_template("login.html")

@app.route("/<usr>")
def user(usr):
  return f"<h1>{usr}</h1>"


if __name__=="__main__":
  app.run(debug=True)