from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools

# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
app.secret_key = b"x6\x87j@\xd3\x88\x0e8\xe8pM\x13\r\xafa\x8b\xdbp\x8a\x1f\xd41\xb8"


slova = ("Super", "Perfekt", "Úža", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")


@app.route("/info/")
def info():
    return render_template("info.html")

@app.route("/pomerance/" , methods = ['GET', 'POST'])
def pomerance():
    if 'uzivatel' not in session:
        flash('jsi ty vubec normalni? nejsi prihlaseny ', 'error')
        return redirect(url_for('login'))

    hmotnost = request.args.get('hmotnost')
    vyska = request.args.get('vyska')

    print(hmotnost, vyska)
    if hmotnost  and vyska :
        try:
            metry = int(vyska)/100
            bmi = int(hmotnost)/metry**2
        except (ZeroDivisionError, ValueError):
            bmi = None
    else:
        bmi = None

    print(bmi)
    return render_template("pomerance.html", bmi=bmi)


@app.route("/abc/")
def abc():
    return render_template("abc.html", slova=slova)


@app.route("/text/")
def text():
    return """

<h1>Text</h1>

<p>toto je text</p>

"""
@app.route("/login/", methods = ['GET'])
def login():
    jmeno = request.args.get('jmeno')
    heslo = request.args.get('heslo')
    return render_template("login.html")

@app.route("/login/", methods = ['POST'])
def login_post():
    jmeno = request.form.get('jmeno')
    heslo = request.form.get('heslo')
    if jmeno and heslo:
        session['uzivatel'] = jmeno


    return redirect(url_for('login'))

@app.route("/logout/", methods = ['GET', 'POST'])
def logout():
    session.pop('uzivatel', None)
    return redirect(url_for('index'))