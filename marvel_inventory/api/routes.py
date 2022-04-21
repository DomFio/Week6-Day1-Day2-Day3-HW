from flask import Blueprint, request, jsonify
from flask_login import current_user
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, User, Marvel, marvel_schema, marvels_schema


api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return{'some': 'value'}

# Create marvel endpoint
@api.route('/marvel', methods = ['POST'])
@token_required
def create_marvel(current_user_token):
    name = request.json['name']
    origin_summary = request.json['origin_summary']
    super_power = request.json['super_power']
    age = request.json['age']
    villans = request.json['villans']
    weakness = request.json['weakness']
    movies = request.json['movies']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    marvel = Marvel(name, origin_summary, super_power, age, villans, weakness, movies, user_token = user_token)

    db.session.add(marvel)
    db.session.commit()

    response = marvel_schema.dump(marvel)
    return jsonify(response)

# Retrieve all marvel endpoints
@api.route('/marvel', methods = ['GET'])
@token_required
def get_marvels(current_user_token):
    owner = current_user_token.token
    marvel = Marvel.query.filter_by(user_token = owner).all()
    response = marvels_schema.dump(marvel)
    return jsonify(response)

#Retreive One marvel endpoint
@api.route('/marvel/<id>', methods = ['GET'])
@token_required
def get_marvel(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        marvel = Marvel.query.get(id)
        response = marvel_schema.dump(marvel)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# Update marvel endpoint
@api.route('/marvel/<id>', methods = ['POST', 'PUT'])
@token_required
def update_marvel(current_user_token, id):
    marvel = Marvel.query.get(id) #grab marvel instance

    marvel.name = request.json['name']
    marvel.origin_summary = request.json['origin_summary']
    marvel.super_power = request.json['super_power']
    marvel.age = request.json['age']
    marvel.villans = request.json['villans']
    marvel.weakness = request.json['weakness']
    marvel.movies = request.json['movies']
    marvel.user_token = current_user_token.token

    db.session.commit()
    response = marvel_schema.dump(marvel)
    return jsonify(response)


#Delete marvel endpoint
@api.route('/marvel/<id>', methods = ['DELETE'])
@token_required
def delete_marvel(current_user_token, id):
    marvel = Marvel.query.get(id)
    db.session.delete(marvel)
    db.session.commit()
    response = marvel_schema.dump(marvel)
    return jsonify(response)