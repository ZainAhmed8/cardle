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
        return '#50C878', 'equal'
    elif abs(value - target) <= exact_range:
        return '#50C878', 'equal'
    elif abs(value - target) <= near_range:
        if value < target:
            return '#E4D00A', 'up'
        else: 
            return '#E4D00A', 'down'
    else:
        if value < target:
            return '#808080', 'up'
        else: 
            return '#808080', 'down'

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
    # car_of_the_day_entry = mongo.db.car_of_the_day.find_one({})
    # if not car_of_the_day_entry:
    #    return jsonify({'error': 'Car of the day not set'}), 404

    car_of_the_day_id = '66afcf6373a71b92e6293a41'
    car_of_the_day = mongo.db.cardle_coll.find_one({'_id': ObjectId(car_of_the_day_id)})
    car_of_the_day['_id'] = str(car_of_the_day['_id'])
    return jsonify(car_of_the_day)

@app.route('/api/car_details', methods=['GET'])
def get_car_details():
    year = request.args.get('year')
    make = request.args.get('make')
    model = request.args.get('model')
    
    if not year or not make or not model:
        return jsonify({'error': 'Missing required parameters'}), 400

    car = mongo.db.cardle_coll.find_one({
        'year': int(year),
        'make': make,
        'model': model
    })

    if not car:
        return jsonify({'error': 'Car not found'}), 404

    car['_id'] = str(car['_id'])
    return jsonify(car)

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    data = request.json
    guess = {
        'year': data.get('year'),
        'make': data.get('make'),
        'model': data.get('model')
    }
    car_of_the_day_id = data.get('car_of_the_day_id')
    car_of_the_day = mongo.db.cardle_coll.find_one({'_id': ObjectId(car_of_the_day_id)})

    # Fetch the details of the guessed car from the database
    guessed_car = mongo.db.cardle_coll.find_one({
        'year': guess['year'],
        'make': guess['make'],
        'model': guess['model']
    })

    if not guessed_car:
        return jsonify({'error': 'Guessed car not found'}), 404

    comparison = {}
    is_correct = True
    for key in ['year', 'make', 'model', 'body_styles', 'country', 'starting_msrp']:
        if key in ['year', 'starting_msrp']:
            if key == 'year':
                exact_range = 0
                near_range = 3
            elif key == 'starting_msrp':
                exact_range = 10000
                near_range = 20000
            color, arrow = check_value(guessed_car[key], car_of_the_day[key], exact_range, near_range)
            comparison[key] = {'match': color, 'direction': arrow}
            if color != '#50C878':
                is_correct = False
        else:
            comparison[key] = {'match': '#50C878' if guessed_car[key] == car_of_the_day[key] else '#808080'}
            if color != '#50C878':
                is_correct = False

    result = {
        'comparison': comparison,
        'guesses_left': 10 - len(data.get('guesses', [])) - 1,
        'all_guesses': data.get('guesses', []) + [guess],
        'is_correct': is_correct
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

