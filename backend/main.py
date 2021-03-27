from flask import Flask
from flask_restful import Api, Resource, reqparse 
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
api = Api(app)

# Database
password = os.environ.get('PASSWORD')

client = pymongo.MongoClient("mongodb+srv://suntex:{password}@venus.klg4w.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(password=password))
db = client["Venus"]
shelters = db["Shelters"]
resources = db["Resources"]


 # Paths 
materialsGetParser = reqparse.RequestParser()
materialsGetParser.add_argument("materialName", type=str, help="Name of the material")

materialsPutParser = reqparse.RequestParser()
materialsGetParser.add_argument("materialName", type=str, help="Name of the material")
materialsGetParser.add_argument("amount", type=int, help="Amount of the material")

materialsPostParser = reqparse.RequestParser()
materialsGetParser.add_argument("materialName", type=str, help="Name of the material")

# Classes
# class Material:
#     def __init__(self,name):
#         self.name = name
#         self.quantity = 0
# class UserMaterials: 
#     def __init__(self,_id):
#         self._id = _id
#         self.materials = { "water": 0, "food":0, "oxygen": 0, "happiness": 0, "population": 0}

# class Room:
#     def __init__(self,name):
#         self.name = name
        
# class ShelterOperation:
#     def __init__(self,id):
#         print("lol")
#         #constructor 
#     def run():
#         print("filler code")
#         #do the operation's function 
# class Shelter:
#     def __init__(self,name,id):
#         self.name = name
#         self.id = id
#         self.rooms = []

userMaterialBase = {
    "_id":0,
    "materials": { "water": 0, "food":0, "oxygen": 0, "happiness": 0, "population": 0}
}

class Materials(Resource):
    def get(self,userid):
        data = resources.find_one({"_id":userid})
        if data is None:
            return {"message":"Meh","status":"404 RESOURCE NOT FOUND"}
        return {"message":"Yeah","status":"200 OK", "data":data}
    def post(self,userid):
        # Creating an id from the database 
        # Create a dictionary based of a base 
        # Add the dictionary into the database 
        documentsNum = resources.find().count()
        userMaterials = userMaterialBase
        userMaterials["_id"] = documentsNum
        resources.insert_one(
            userMaterials
        )
        return {"message":"Operation Successful", "status":"200 OK"}
    def put(self,userid):
        return "yeah okay"

class Shelters(Resource):
    def get(self,shelterid,operation):
        dataFromDB = collection.find_one({"_id":userid})
        return {"message":"Yeah","status":"200 OK", "data":dataFromDB}
    def post(self,userid):
        return "nice"
    def put(self,userid):
        return "yeah okay"

# Resources Endpoints
api.add_resource(Materials,"/api/Materials/<int:userid>")
# api.add_resource(Materials,"/api/Materials/<int:userid>/<string:resourcename>")
# api.add_resource(Materials,"/api/Materials/<int:userid>/<string:resourcename>/<int:num>")
# Shelter end points 
#api.add_resource(Shelters,"/api/Shelters/<int:shelterid>/<string:operation>")
#api.add_resource(Shelters,"/api/Shelters/<int:shelterid>")
api.add_resource(Shelters,"/api/Shelters")


if __name__ == "__main__":
    app.run(debug=True)