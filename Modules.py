from db import db
from sqlalchemy import String,  Integer, func, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class Clients(db.Model):
    __tablename__ = 'clients'
    id = db.Column('client_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    password = db.Column(db.String(50))  


    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        


class Workspaces(db.Model):
    __tablename__ = 'workspaces'
    id = db.Column('workspace_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.now())


    def __init__(self, name):
        self.name = name
        # self.created_at = created_at


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Reservations(db.Model):
    __tablename__ = 'reservations'

    id = db.Column('reservation_id', db.Integer, primary_key = True)
    Workspace_id = Column(Integer, ForeignKey('workspaces.workspace_id'))
    client_id = Column(Integer, ForeignKey('clients.client_id'))

    created_at = db.Column(db.DateTime, default=db.func.now())
 
    workspaces = relationship(
        Workspaces,
        backref=backref('reservations',
                         uselist=True,
                         cascade='delete,all'))

    workspaces = relationship(
        Workspaces,
        backref=backref('clients',
                         uselist=True,
                         cascade='delete,all'))


    def __init__(self, client_id, Workspace_id):
        self.client_id = client_id
        self.Workspace_id = Workspace_id


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()