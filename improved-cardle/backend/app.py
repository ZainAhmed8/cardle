from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://zainahmed8:9xohXdECeL337HLM@cardlecluster.0nj0jgx.mongodb.net/CardleMain"
mongo = PyMongo(app)
CORS(app)

def check_value(value, target, exact_range, near_range):
    if value == target:
        return 'green', 'equal'
    elif abs(value - target) <= exact_range:
        return 'yellow', 'equal'
    elif value < target:
        return 'gray', 'up'
    else:
        return 'gray', 'down'

@app.route('/api/years', methods=['GET'])
def get_years():
    years = mongo.db.cardle_coll.distinct("year")
    return jsonify(sorted(years))

@app.route('/api/makes', methods=['GET'])
def get_makes():
    year = request.args.get('year')
    makes = mongo.db.cardle_coll.distinct("make", {"year": int(year)})
    return jsonify(makes)

@app.route('/api/models', methods=['GET'])
def get_models():
    year = request.args.get('year')
    make = request.args.get('make')
    models = mongo.db.cardle_coll.distinct("model", {"make": make, "year": int(year)})
    return jsonify(models)

@app.route('/set_car_of_the_day', methods=['POST'])
def set_car_of_the_day():
    data = request.json
    car_of_the_day_id = data.get('car_of_the_day_id')
    car_of_the_day = mongo.db.cardle_coll.find_one({'_id': ObjectId(car_of_the_day_id)})

    if not car_of_the_day:
        return jsonify({'error': 'Car not found'}), 404

    car_of_the_day_entry = {
        'car_of_the_day_id': car_of_the_day_id,
        'date': datetime.datetime.now(datetime.timezone.utc)
    }

    mongo.db.car_of_the_day.replace_one({}, car_of_the_day_entry, upsert=True)
    return jsonify({'message': 'Car of the day set successfully'})

@app.route('/get_car_of_the_day', methods=['GET'])
def get_car_of_the_day():
    car_of_the_day_entry = mongo.db.car_of_the_day.find_one({})
    if not car_of_the_day_entry:
        return jsonify({'error': 'Car of the day not set'}), 404

    car_of_the_day_id = car_of_the_day_entry['car_of_the_day_id']
    car_of_the_day = mongo.db.cardle_coll.find_one({'_id': ObjectId(car_of_the_day_id)})
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
    car_of_the_day = mongo.db.cardle_coll.find_one({'_id': ObjectId(car_of_the_day_id)})

    comparison = {}
    for key in guess:
        if key in ['year', 'starting_msrp']:
            if key == 'year':
                exact_range = 0
                near_range = 3
            elif key == 'starting_msrp':
                exact_range = 5000
                near_range = 10000
            color, arrow = check_value(guess[key], car_of_the_day[key], exact_range, near_range)
            comparison[key] = {'match': color, 'direction': arrow}
        else:
            comparison[key] = {'match': 'green' if guess[key] == car_of_the_day[key] else 'gray'}

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

