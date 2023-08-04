from flask import Flask, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_socketio import send, SocketIO
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    display_name = StringField(label="Display Name", 
                               validators=[DataRequired(), Length(max=15, message="15 characters max")], 
                               render_kw={"autofocus": True, "autocomplete": "off"})
    submit = SubmitField(label="Log In")

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
Bootstrap(app)
socketio = SocketIO(app)

message_list = []

@app.route("/", methods=["GET", "POST"])
def home():

    login_form = LoginForm()
    if login_form.validate_on_submit():

        session["name"] = login_form.display_name.data
        return redirect(url_for("chat"))

    return render_template("login.html", form=login_form)

@app.route("/chat")
def chat():

    display_name = session.get("name")
    return render_template("chat.html", messages=message_list, display_name=display_name)

@socketio.on("message")
def handle_message(data):

    content = {
        "name": session.get("name"),
        "message": data["data"],
        "sid": request.sid,
    }

    send(content, broadcast=True)
    message_list.append(content)

if __name__ == "__main__":
    socketio.run(app, debug=True)