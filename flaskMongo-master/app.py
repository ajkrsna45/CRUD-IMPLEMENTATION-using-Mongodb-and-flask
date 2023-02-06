from flask import Flask, jsonify, request, redirect
from flask.helpers import url_for
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/favInfo'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)

@app.route('/', methods = ['GET'])
def retrieveAll():
    holder = list()
    currentCollection = mongo.db.favInfo
    for i in currentCollection.find():
        holder.append({'name':i['name'], 'paasword' : i['favPassword'], 'role' : i['favRole']})
    return jsonify(holder)

@app.route('/<name>', methods = ['GET'])
@cross_origin()
def retrieveFromName(name):
    currentCollection = mongo.db.favInfo
    data = currentCollection.find_one({"name" : name})
    return jsonify({'name' : data['name'], 'password' : data['favPassword'], 'role' : data['favRole']})

@app.route('/postData', methods = ['POST'])
def postData():
    currentCollection = mongo.db.favInfo
    name = request.json['name']
    genre = request.json['password']
    game = request.json['role']
    currentCollection.insert({'name' : name, 'favPassword' : password, 'favRole' : role})
    return jsonify({'name' : name, 'password' : password, 'role' : role})

@app.route('/deleteData/<name>', methods = ['DELETE'])
def deleteData(name):
    currentCollection = mongo.db.favInfo
    currentCollection.delete_one({'name' : name})
    return redirect(url_for('retrieveAll'))

@app.route('/update/<name>', methods = ['PUT'])
def updateData(name):
    currentCollection = mongo.db.favInfo
    updatedName = request.json['name']
    currentCollection.update_one({'name':name}, {"$set" : {'name' : updatedName}})
    return redirect(url_for('retrieveAll'))

if __name__ == '__main__':
    app.run(debug = True)
