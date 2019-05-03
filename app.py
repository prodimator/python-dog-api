from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import json
import uuid

app = Flask(__name__)
filename = 'dogs.json'
api = Api(app)

@app.route('/dogs', methods=['GET', 'POST']) 
def dogs():
    if request.method == 'GET':
        data = getJsonData()
        if data is not None:
            return (json.dumps(data, indent=4), 200)
        else:
            return ("Could not get data", 400)

    if request.method == 'POST':
        
        # add args
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("owner")
        parser.add_argument("notes")
        args = parser.parse_args()

        # create object from args
        data = getJsonData()
        dog = {
            "uid": str(uuid.uuid4())[:4],
            "name": args['name'],
            "owner": args['owner'],
            "notes": args['notes']
        }

        #append new dog to list
        data += [dog]

        #write list to file
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            return ("Success", 200)

@app.route('/dogs/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def dogsID(id):
    if request.method == 'GET':
        data = getJsonData()
        for dog in data:
            if id == dog['uid']:
                return (json.dumps(dog, indent=4), 200)
        return ("Could not find dog", 400)

    if request.method == 'PUT':
        data = getJsonData()
        for dog in data:
            if id == dog['uid']:
                # add args
                parser = reqparse.RequestParser()
                parser.add_argument("name")
                parser.add_argument("owner")
                parser.add_argument("notes")
                args = parser.parse_args()
                
                newDog = {
                    "uid": dog['uid'],
                    "name": args['name'],
                    "owner": args['owner'],
                    "notes": args['notes']
                }

                index = data.index(dog)
                data[index] = newDog
                with open(filename, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                    return("Success", 200)
            else:
                return ("Dog not found.", 400)
    
    if request.method == 'DELETE':
        data = getJsonData()
        for dog in data:
            if id == dog['uid']:
                del data[dog['uid']-1]
                with open(filename, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                    return ("Success", 200)
            else:
                return ("Dog not found.", 400)


def getJsonData():
    # this is slightly more performance heavy, but it's easier and cleaner to update all of the json data this way
    # gets all of the data in the json file and returns it as an object
    try:
        with open(filename) as json_file:  
                data = json.load(json_file)
                json_file.close()
                return data
    except:
        print("Could not get JSON data. Please check the file.")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")