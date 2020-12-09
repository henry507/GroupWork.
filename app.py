# Import helper libs
from Modules import Clients, Reservations, Workspaces
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import pandas as pd
import json

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TUAS.sqlite3"


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def hello():
    return "welcome to reservation"


@app.route("/Client", methods=["GET", "POST"])
def Create_Client():
    if request.method == "GET":
        clients = Clients.query.all()
        clients_list = []
        for client in clients:
            clients_list.append({'id' : client.id, 'name': client.name, 'email' : client.email})
        return jsonify({"clients_list": clients_list})


    elif request.method == "POST":
        params = request.get_json(force=True)
        name = params["name"]
        email = params["email"]
        password = params["pass"]

        if name == "" or email == "":
            return jsonify("name and email should be string")

        # check if client exist in database
        is_exist = Clients.query.filter_by(email=email).first()

        # create client object
        if not is_exist:
            clients_list = Clients(name, email, password)
            clients_list.save_to_db()
            return jsonify("Client created successfuly")
        else:
            return jsonify("Client already exists")


@app.route("/workspace", methods=["GET", "POST", "DELETE"])
def Create_Workspace():
    if request.method == "GET":
        workspaces = Workspaces.query.all()
        workspaces_list = []
        for workspace in workspaces:
            workspaces_list.append({'id':workspace.id, 'name':workspace.name})
        return jsonify({"workspaces_List": workspaces_list})


    elif request.method == "POST":
        params = request.get_json(force=True)
        name = params["name"]

        if name == "":
            return jsonify("name of Workspaces should be string and not empty")

        # check if Workspaces exist in database
        is_exist = Workspaces.query.filter_by(name=name).first()

        # create client object
        if not is_exist:
            workspace = Workspaces(name)
            workspace.save_to_db()
            return jsonify("workspace created successfuly")
        else:
            return jsonify("workspace already exists")

    elif request.method == "DELETE":
        params = request.get_json(force=True)
        name = params["name"]

        if name == "":
            return jsonify("name of Workspaces should be string")

        # check if Workspaces exist in database
        is_exist = Workspaces.query.filter_by(name=name).first()

        if is_exist:
            is_exist.delete_from_db()
            return jsonify("workspace deleted successfuly")
        else:
            return jsonify("workspace not exists")


@app.route("/reservations", methods=["GET", "POST", "DELETE"])
def Reservation():

    if request.method == "GET":
        reservations = Reservations.query.all()
        reservations_list = []
        for reservation in reservations:
            reservations_list.append({'id':reservation.id, 'Workspace_id':reservation.Workspace_id, 'client_id':reservation.client_id})
        return jsonify({"reservations_List": reservations_list})

    elif request.method == "POST":
        params = request.get_json(force=True)
        Workspace_id = params["Workspace_id"]
        client_id = params["client_id"]

        if Workspace_id == "" or client_id == "":
            return jsonify("Workspace_id and client_id should be numbers")

        # check if Workspaces exist in database
        workspace_exist = Workspaces.query.filter_by(id=Workspace_id).first()
        client_exist = Clients.query.filter_by(id=client_id).first()

        # create client object
        if workspace_exist and client_exist:

            # check if Workspaces exist in database
            reservation_exist = Reservations.query.filter_by(
                Workspace_id=Workspace_id
            ).first()

            if not reservation_exist:
                Reservation = Reservations(client_id, Workspace_id)
                Reservation.save_to_db()
                return jsonify("Reservations created successfuly")
            else:
                return jsonify("Workspace Already Reserved")

        else:
            if not workspace_exist:
                return jsonify("workspace not exist")
            else:
                return jsonify("client not Registered")

    elif request.method == "DELETE":
        params = request.get_json(force=True)
        Workspace_id = params["Workspace_id"]
        client_id = params["client_id"]

        if Workspace_id == "" or client_id == "":
            return jsonify("Workspace_id and client_id should be numbers")

        # check if Workspaces exist in database
        reservation_exist = Reservations.query.filter_by(Workspace_id=Workspace_id).first()

        if reservation_exist:
            reservation_exist.delete_from_db()
            return jsonify("workspace deleted successfuly")
        else:
            return jsonify("Reservations not exists")


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(debug=True)
