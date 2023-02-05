import os
from pathlib import Path

from flask import (
    Flask,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from models import User
from forms import LoginForm

os.chdir(os.path.dirname(__file__))

APP_DIR = Path(".").cwd()
DATA_STORAGE_PATH = Path("users")

app = Flask(
    __name__,
    static_url_path="",
    template_folder=str(APP_DIR / "src"),
    static_folder=str(APP_DIR / "src"),
)
app.config["SECRET_KEY"] = b"aboba\n\xec]/"
CORS(app)
app.jinja_env.globals.update(Path=Path)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(User.get(User.login == form.login.data), remember=True)
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/index")
@app.route("/")
def index():
    if current_user.is_authenticated:
        return str(current_user.get_id())
    else:
        return 'bad'


@app.route("/check-permission")
@login_required
def check_permission():
    return 'ok'


@app.route("/files/<path:path>")
def send_files(path):
    return send_from_directory(APP_DIR / "src", path)


if __name__ == "__main__":
    app.run(port=8000)
