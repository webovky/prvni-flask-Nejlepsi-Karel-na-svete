from pickle import GET
from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools
import string
import random
import re

# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
app.secret_key = b"x6\x87j@\xd3\x88\x0e8\xe8pM\x13\r\xafa\x8b\xdbp\x8a\x1f\xd41\xb8"


slova = ("Super", "Perfekt", "Úža", "Flask")

from mysqlite import SQLite


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


@app.route("/abc/")
def abc():
    if "uživatel" not in session:
        flash("Nejsi příhlášen, tato stránka vyžaduje přihlášení.", "error")
        return redirect(url_for("login", page=request.full_path))
    return render_template("abc.html", slova=slova)


@app.route("/banan/", methods=["GET", "POST"])
def banan():
    if "uživatel" not in session:
        flash("Nejsi příhlášen, tato stránka vyžaduje přihlášení.", "error")
        return redirect(url_for("login", page=request.full_path))

    hmotnost = request.args.get("hmotnost")

    výška = request.args.get("výška")

    print(hmotnost, výška)
    if hmotnost and výška != None:
        bmi = int(hmotnost) / ((int(výška) / 100) ** 2)
    else:
        bmi = 0
    return render_template("banan.html", bmi=bmi)


@app.route("/text/")
def text():
    return """

<h1>Text</h1>

<p>toto je text</p>

"""


@app.route("/login/", methods=["GET"])
def login():
    jmeno = request.args.get("jmeno")
    heslo = request.args.get("heslo")
    print(jmeno, heslo)
    if request.method == "GET":
        return render_template("login.html")


@app.route("/login/", methods=["POST"])
def login_post():
    jmeno = request.form.get("jmeno")
    heslo = request.form.get("heslo")
    page = request.args.get("page")

    with SQLite("SQLlite.db") as cur:
        cur.execute("select passwd FROM user WHERE login = ?", [jmeno])
        ans = cur.fetchall()

    if ans and ans[0][0] == heslo:
        flash("Jsi přihlášen!", "message")
        session["uživatel"] = jmeno
        if page:
            return redirect(page)
    else:
        flash("Nespávné přihlašovací udaje", "error")
    if page:
        return redirect(url_for("login", page=page))
    return redirect(url_for("login"))
    # stejne jako funkce get, jen jiný zápis


@app.route("/logout/", methods=["GET"])
def logout():
    session.pop("uživatel", None)
    return redirect(url_for("login"))


@app.route("/registr/", methods=["GET"])
def registr():
    jmeno = request.args.get("jmeno")
    heslo = request.args.get("heslo")
    heslo2 = request.form.get("heslo2")

    print(jmeno, heslo, heslo2)
    if request.method == "GET":
        return render_template("registr.html")


@app.route("/registr/", methods=["POST"])
def registr_post():
    jmeno = request.form.get("jmeno")
    heslo = request.form.get("heslo")
    heslo2 = request.form.get("heslo2")
    page = request.args.get("page")

    with SQLite("SQLlite.db") as cur:
        cur.execute("INSERT INTO user = (?, ?)", [jmeno, heslo])
        ans = cur.fetchall()
    if heslo == heslo2:

        if ans and ans[0][0] == heslo:
            flash("Jsi přihlášen!", "message")
            session["uživatel"] = jmeno
        if page:
            return redirect(page)
        else:
            flash("Nespávné přihlašovací udaje", "error")
    if page:
        return redirect(url_for("login", page=page))
    return redirect(url_for("pomerance"))


@app.route("/zkracovac/")
def zkracovac():
    new = request.args.get("new")
    if "uživatel" in session:
        with SQLite("SQLlite.db") as cur:
            res = cur.execute(
                "SELECT zkratka, adresa FROM adresy WHERE user =?", [session["uživatel"]]
            )
            zkratky = res.fetchall()
            if zkratky == None:
                zkratky = []

    else:
        zkratky = []
    return render_template("zkracovac.html", new=new, zkratky=zkratky)


@app.route("/zkracovac/", methods=["POST"])
def zkracovac_post():
    url = request.form.get("url")
    if url and re.match("https?://.+", url):
        zkratka = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        flash("adresa ulozena")
        with SQLite("SQLlite.db") as cur:
            if "uživatel" in session:

                cur.execute(
                    "INSERT INTO adresy (zkratka, adresa, user) VALUES (?, ?, ?)",
                    [zkratka, url, session["uživatel"]],
                )

            else:
                cur.execute(
                    "INSERT INTO adresy (zkratka, adresa) VALUES (?, ?)", [zkratka, url]
                )

            return redirect(url_for("zkracovac", new=zkratka))
    else:
        flash("ADRESA NEN9 ADRESA")

    return redirect(url_for("zkracovac"))


@app.route("/zkracovac/<zkratka>", methods=["GET"])
def dezkracovac(zkratka):
    print(zkratka)
    with SQLite("SQLlite.db") as cur:
        if "uživatel" in session:
            res = cur.execute("SELECT adresa FROM adresy WHERE zkratka=?", [zkratka])
            odpoved = res.fetchall()[0][0]
        if odpoved:
            print(odpoved)
            return redirect(odpoved)
        else:
            flash("({})neni adresa".format(zkratka))
    return redirect(odpoved)
