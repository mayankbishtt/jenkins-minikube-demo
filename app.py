from flask import Flask

app = Flask(__name__)

print("Application Started")

@app.route("/")
def home():

    x = 10

    return "Hello from Jenkins and Kubernetes"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)