from flask import Flask, render_template
from app import create_app


app = create_app()

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/graphs")
# def graphs():
#     print("Generating graphs...")
#     return "Test"

if __name__ == "__main__":
    app.run()
