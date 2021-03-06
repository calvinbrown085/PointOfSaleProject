from flask import render_template, request, redirect, session, abort, jsonify
from passlib.apps import custom_app_context as pwd_context

loginHtml = """<!DOCTYPE html>
<html>
  <head>
    <title>Log In</title>
  </head>
  <body>
    <h2>Please Log In</h2>
    <form action="/login", method="post">
      username: <br>
      <input type="text" name="username"></input> <br>
      password: <br>
      <input type="password" name="password"></input>
      <input type="submit" name="login">
    </form>
  </body>
</html>"""

loginErrorHtml =  """<!DOCTYPE html>
<html>
  <head>
    <title>Log In</title>
  </head>
  <body>
    <h2>Please Log In</h2>
    <p> Incorrect Username or Password.
    Please check your credentials and try again.
    </p>
    <form action="/login", method="post">
      username: <br>
      <input type="text" name="username"></input> <br>
      password: <br>
      <input type="password" name="password"></input>
      <input type="submit" name="login">
    </form>
  </body>
</html>"""

logoutHtml = """<!DOCTYPE html>
<html>
  <head>
    <title>Logged Out</title>
  </head>
  <body>
    <h2>Logged Out</h2>
    <a href="/">home</a>
  </body>
</html>"""

def requireLogin():
    if (not session.get("logged_in")):
        return abort(401)
    elif (session.get("current_user") == "east"):
        print("east is active")

def requireManagerLogin(db):
    if (session.get("logged_in") and db.getManagerStatus()[0][0] == 0):
        return abort(401)

def requireAdminLogin(db):
    if (session.get("logged_in") and db.getManagerStatus()[0][0] < 2):
        return abort(404)

def logout():
    if (not session["logged_in"]):
        return redirect("/")
    else:
        session["current_user"] = None
        session["logged_in"] = False
        return logoutHtml

def login(db):
        if (request.method == "POST"):
            passwordHash = db.getPasswordForUser(request.form["username"])
            if (passwordHash == []):
                return loginErrorHtml
            else:
                if (pwd_context.verify(request.form["password"], passwordHash[0][0])):
                    session['logged_in'] = True
                    session["current_user"] = request.form["username"]
                    session["resultList"] = []
                    session["totalAmount"] = 0
                    session["managerSearchList"] = []
                    session["searchList"] = []
                    session["error"] = ""
                    if (db.getManagerStatus()[0][0] > 0):
                        return redirect("/managerPage")
                    else:
                        return redirect("/pos")
                else:
                    return loginErrorHtml
        else:
            return loginHtml
