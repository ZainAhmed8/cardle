from flask import Flask, request, jsonify
from pymongo import PyMongo
from bson.objectid import ObjectId
import random

app = Flask(__name__)

@app.route('/get_car_of_the_day', methods=['GET'])
def get_car_of_the_day():
    car_collection = mongo.db.cars
    car_count = car_collection.count_documents({})
    random_index = random.randint(0, car_count - 1)
    car_of_the_day = car_collection.find().skip(random_index).limit(1)[0]
    car_of_the_day['_id'] = str(car_of_the_day['_id'])
    return jsonify(car_of_the_day)

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    data = request.json
    guess = {
        'year': data.get('year'),
        'make': data.get('make'),
        'model': data.get('model'),
        'body_styles': data.get('body_styles'),
        'country': data.get('country'),
        'starting_msrp': data.get('starting_msrp'),
    }
    car_of_the_day_id = data.get('car_of_the_day_id')
    car_of_the_day = mongo.db.cars.find_one({'_id': ObjectId(car_of_the_day_id)})

    comparison = {}
    for key in guess:
        comparison[key] = guess[key] == car_of_the_day[key]

    if 'guesses' not in data:
        data['guesses'] = []
    data['guesses'].append(guess)

    result = {
        'comparison': comparison,
        'guesses_left': 10 - len(data['guesses']),
        'all_guesses': data['guesses'],
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

