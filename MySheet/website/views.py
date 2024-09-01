from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import *
from . import db
import os

def read_file_contents(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
    else:
        return ""
    
def IDToName(id):
    sheet = Sheet.query.get(id)
    return sheet.name

def IDToEmail(id):
    user = User.query.get(id)
    return user.email

def EmailTOID(email):
    user = User.query.filter_by(email=email).first()
    return user.id

def decAc(p):
    if p == "viewer":
        return 1
    elif p == "editor":
        return 0
    
def AcDec(p):
    if p == 1:
        return "Viewer"
    elif p == 0:
        return "Editor"

def checkAccess(user,note):
    access = Access.query.filter_by(sheet_id=note.id, user_id=user.id).first()
    if user.id == note.owner_id:
        return "owner"
    elif access.access_type == 0:
        return "editor"
    elif access.access_type == 1:
        return "viewer"
    else:
        return None
    

routes = Blueprint('routes', __name__)

@routes.route("/")
@login_required
def home():
    owned_items = Sheet.query.filter_by(owner_id = current_user.id).all()
    shared_items = Access.query.filter_by(user_id = current_user.id).all()
    return render_template("home.html", owned_items=owned_items[::-1], user=current_user, shared_items=shared_items[::-1],IDToName=IDToName, AcDec=AcDec)

@routes.route("/sheet/<id>", methods=["POST", "GET"])
@login_required
def sheets(id):
    if request.method=="POST":
        item = Sheet.query.get(id)
        access = checkAccess(current_user, item)
        if access in ["owner", "editor"]:
            note = request.form.get("note")
            with open(f"./website/notes/{id}.html", "w") as f:
                f.write(note)
            return redirect("/")

    item = Sheet.query.get(id)
    access = checkAccess(current_user, item)
    if access != None:
        content = read_file_contents(f"./website/notes/{id}.html")
        if access in ["owner", "editor"]:
            if access == "owner":
                owner=True
            else:
                owner = False
            return render_template("sheets.html", user=current_user, sheet=item, content=content, owner=owner)
        else:
            return render_template("view.html", user=current_user, sheet=item, content=content)
    else:
        return redirect("/")


@routes.route("/new-sheet", methods=["POST"])
@login_required
def newSheet():
    name = request.form.get("sheet-name")
    sheet = Sheet(name = name, owner_id = current_user.id)
    db.session.add(sheet)
    db.session.commit()
    item = Sheet.query.filter_by(name = name, owner_id = current_user.id).first()
    return redirect(f"/sheet/{item.id}")

@routes.route("/delete/<id>")
@login_required
def deleteSheet(id):
    item = Sheet.query.get(id)
    access = checkAccess(current_user, item)
    if access == "owner":
        os.remove(f"./website/notes/{id}.html")
        db.session.delete(item)
        db.session.commit()
    return redirect("/")

@routes.route("/search")
@login_required
def search():
    query = request.args.get('q')
    owned_items = Sheet.query.filter_by(owner_id = current_user.id).all()
    shared_items = Access.query.filter_by(user_id = current_user.id).all()
    filtered = []
    for note in owned_items+shared_items:
        if query in note.name:
            filtered.append(note)
    return render_template("search.html", filtered=filtered, query=query, user=current_user, IDToName=IDToName, IDToEmail=IDToEmail)

@routes.route("/access/<id>", methods=['POST'])
@login_required
def shareAccess(id):
    item = Sheet.query.get(id)
    access = checkAccess(current_user, item)
    if access == "owner":
        access = Access(owner_id=current_user.id, sheet_id=id, access_type=decAc(request.form.get("type")), user_id=EmailTOID(request.form.get("email")))
        db.session.add(access)
        db.session.commit()
    return redirect(f"/sheet/{id}")