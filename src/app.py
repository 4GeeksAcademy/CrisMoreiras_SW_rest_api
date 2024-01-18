"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Character_fav, Planet_fav
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#METODOS USUARIO#

@app.route('/user', methods=['POST'])
def add_new_user():
    body = request.get_json()
    
    if (
        "username" not in body
        or "email" not in body
        or "password" not in body
    ):
        return jsonify({"error": "Datos usuario incompletos"}), 400
    
    new_user = User(
        username=body["username"],
        email=body["email"],
        password=body["password"],   
    )
    
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "msg": "Nuevo character añadido exitosamente"
    }

    return jsonify(response_body), 200

@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    results = list(map(lambda user: user.serialize(), all_users))
    return jsonify(results), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def one_user(user_id):
    one_user = User.query.get(user_id)
    return jsonify(one_user.serialize()), 200

#METODOS PERSONAJE#

@app.route('/character', methods=['POST'])
def add_new_character():
    body = request.get_json()
    
    if (
        "name" not in body
        or "gender" not in body
        or "specie" not in body
    ):
        return jsonify({"error": "Datos personaje incompletos"}), 400
    
    new_character = Character(
        name=body["name"],
        gender=body["gender"],
        specie=body["specie"]
    )
    
    db.session.add(new_character)
    db.session.commit()

    response_body = {
        "msg": "Nuevo character añadido exitosamente"
    }

    return jsonify(response_body), 200

@app.route('/character', methods=['GET'])
def get_character():
    all_characters = Character.query.all()
    results = list(map(lambda character: character.serialize() ,all_characters))
    return jsonify(results), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def one_character(character_id):
    character = Character.query.get(character_id)
    return jsonify(character.serialize()), 200

#METODOS PLANETA#

@app.route('/planet', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    results = list(map(lambda planet: planet.serialize(), all_planets))
    return jsonify(results), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200

######POST USER FAVORITE CHARACTER############

@app.route('/character_fav', methods=['POST'])
def add_new_character_fav():
    request_body_fav_character = request.get_json()


    if (
        "character_id" not in request_body_fav_character
        or "user_id" not in request_body_fav_character
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    
    new_fav_character = Character_fav(
        character_id=request_body_fav_character["character_id"],
        user_id=request_body_fav_character["user_id"]
    )
    
    db.session.add(new_fav_character)
    db.session.commit()

    response_body = {
        "msg": "Nuevo character_fav añadido exitosamente"
    }

    return jsonify(response_body), 200

################################# GET CHARACTER FAV BY USER ID ########################

@app.route('/user/<int:user_id>/character_fav', methods=['GET'])
def get_user_favorites(user_id):
    user_favorites = Character_fav.query.filter_by(user_id=user_id).all()

    results = map(lambda favorites: favorites.serialize(), user_favorites)
    favorites_list = list(results)
    return jsonify(favorites_list), 200

######POST USER FAVORITE PLANET############

@app.route('/planet_fav', methods=['POST'])
def add_new_planet_fav():
    request_body_fav_planet = request.get_json()


    if (
        "planet_id" not in request_body_fav_planet
        or "user_id" not in request_body_fav_planet
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    
    new_fav_planet = Planet_fav(
        planet_id=request_body_fav_planet["planet_id"],
        user_id=request_body_fav_planet["user_id"]
    )
    
    db.session.add(new_fav_planet)
    db.session.commit()

    response_body = {
        "msg": "Nuevo planeta_fav añadido exitosamente"
    }

    return jsonify(response_body), 200

################################# GET planet FAV BY USER ID ########################

@app.route('/user/<int:user_id>/planet_fav', methods=['GET'])
def get_user_favorites_planet(user_id):
    user_favorites_planet = Planet_fav.query.filter_by(user_id=user_id).all()

    results = map(lambda favorites: favorites.serialize(), user_favorites_planet)
    favorites_list = list(results)
    return jsonify(favorites_list), 200













# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
