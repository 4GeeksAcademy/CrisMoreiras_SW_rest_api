from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class User2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    user_name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    character_fav = db.relationship('Character', lazy=True)
    
       
    def __repr__(self):
        return '<User2 %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "user_name": self.user_name,
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    specie = db.Column(db.String(250), nullable=False)
    planet = db.Column(db.String(250), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user2.id'),
        nullable=False)
    
       
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "specie": self.specie,
            "planet": self.planet,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    rotation = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(250), nullable=False) 
    
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation": self.rotation,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }
    
    #FAVORITOS#
    
class Character_fav(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user2_id = db.Column(db.Integer, db.ForeignKey("user2.id"), nullable=False)
    user2_relatioship = db.relationship(User2)
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    character_relatioship = db.relationship(Character)
    
    def __repr__(self):
        return '<Character_fav %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "user2_id": self.user2_id,
            
        }
     