from flask import *
from cryptography.fernet import Fernet
import SystemSettings
import hashlib
import time
from threading import Timer

app = Flask(__name__)


keyboardEnabled = None
keyboardDisabled = "checked"
mouseEnabled = None
mouseDisabled = "checked"
AwakeEnabled = None
AwakeDisabled = "checked"

authtoken = {"token":None,"validtill":None}


@app.route("/")
def index():
    url_for("static", filename="favicon.ico")
    return render_template("login.html")

@app.route("/systemsetting")
def systemsetting():
    if request.args["authtoken"]==authtoken["token"]:
        if authtoken["validtill"] >= round(time.time()):
            return render_template("systemstatus.html",keyboardEnabled=keyboardEnabled, keyboardDisabled=keyboardDisabled, mouseEnabled=mouseEnabled, mouseDisabled=mouseDisabled, AwakeEnabled=AwakeEnabled,AwakeDisabled=AwakeDisabled)
        else:
            return redirect("/Error/400")
    else:
        return redirect("/Error/401")

@app.route("/systemcommand/<command>")
def systemcommand(command):
    if command == "Sleep":
        Timer(5,setting.SystemSleep).start()
    elif command == "Hibernate":
        Timer(5,setting.SystemHibernate).start()
    elif command == "Shutdown":
        Timer(5,setting.SystemShutdown).start()
    elif command == "Restart":
        Timer(5,setting.SystemReboot).start()
    return redirect("/")

@app.route("/Error/<id>")
def Error(id):
    if id == "400":
        return render_template("Error.html",Error="Authtoken Expired")
    elif id == "401":
        return render_template("Error.html",Error="Incorrect Authtoken")
    else:
        return redirect("/")

@app.route("/login",methods=["POST"])
def login():
    global authtoken
    username = request.form["username"]
    password = request.form["password"]
    if username == "yashraj221b" and password == "lazaruz":
        authtoken["token"] = hashlib.sha256(Fernet.generate_key()).hexdigest()
        authtoken["validtill"] = round(time.time())+300
        return redirect("/systemsetting?authtoken="+authtoken["token"])
    return redirect("/")

@app.route("/password/<user>")
def password(user):
    combinations = ["yashraj221b","yashraj221b@","yashraj@221b"]
    if user in combinations:
        return Response('<div><p>username: yashraj221b</p><p>password: lazaruz</p></div>')

@app.route("/setstatus", methods=["POST"])
def setstatus():
    global keyboardEnabled,keyboardDisabled,mouseEnabled,mouseDisabled,AwakeEnabled,AwakeDisabled
    if request.form["Keyboard"] == "KeyboardEnabled":
        keyboardEnabled = "checked"
        keyboardDisabled = None
        setting.startKeyboard(True)

    elif request.form["Keyboard"] == "KeyboardDisabled":
        keyboardEnabled = None
        keyboardDisabled = "checked"
        setting.stopKeyboard()

    if request.form["Mouse"] == "MouseEnabled":
        mouseEnabled = "checked"
        mouseDisabled = None
        setting.startMouse(True)

    elif request.form["Mouse"] == "MouseDisabled":
        mouseEnabled = None
        mouseDisabled = "checked"
        setting.stopMouse()

    if request.form["Awake"] == "AwakeEnabled":
        AwakeEnabled = "checked"
        AwakeDisabled = None
        setting.SystemAwake(True)

    elif request.form["Awake"] == "AwakeDisabled":
        AwakeEnabled = None
        AwakeDisabled = "checked"
        setting.SystemAwake(False)


    return redirect("/systemsetting?authtoken="+authtoken["token"])

def changestatus(kbdEnabled,kbdDisabled,mseEnabled,mseDisabled):
    global keyboardEnabled,keyboardDisabled,mouseEnabled,mouseDisabled
    keyboardEnabled = kbdEnabled
    keyboardDisabled = kbdDisabled
    mouseEnabled = mseEnabled
    mouseDisabled = mseDisabled

setting = SystemSettings.SystemSettings(changestatus)
app.run(host="0.0.0.0",port=221,debug=True)
