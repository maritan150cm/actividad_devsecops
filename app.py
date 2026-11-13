from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Aplicación DevSecOps funcionando súper"

@app.route("/hello")
def hello():
    name = request.args.get("name", "Mundito")
    return f"Hola hola hola, {name}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)