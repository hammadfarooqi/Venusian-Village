from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()
app = Flask(__name__)
api = Api(app)

# Database
password = os.environ.get('PASSWORD')

client = pymongo.MongoClient("mongodb+srv://suntex:{password}@venus.klg4w.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(password=password))
db = client["Venus"]
shelters = db["Shelters"]
resources = db["Resources"]
rooms = db["Rooms"]


 # Paths 
materialsGetParser = reqparse.RequestParser()
materialsGetParser.add_argument("materialName", type=str, help="Name of the material")

materialsPutParser = reqparse.RequestParser()
materialsPutParser.add_argument("materialName", type=str, help="Name of the material")
materialsPutParser.add_argument("amount", type=int, help="Amount of the material")

materialsPostParser = reqparse.RequestParser()
materialsPostParser.add_argument("materialName", type=str, help="Name of the material")


shelterPutParser = reqparse.RequestParser()
shelterPutParser.add_argument("room", type=str, help="Name of the material")

shelterRoomsPutParser = reqparse.RequestParser()
shelterRoomsPutParser.add_argument("value", type=inputs.boolean, help="Name of the material")

# Classes
# collection.insert_one(testObject)

# collection.insert_many( [data1,data2,data3] ) adds in many documents at once 
# collection.insert_one( {object} ) adds in many documents at once 

# collection.find(   {"_id":1}   )  object, key is the term youre searching for. Find something with an index of 1 
# find will ALWAYS return an array, even if it's size is one 
# .find_one( {object} ) will return one element, not an array. Returns first one 

# .delete_one will delete one document that fits a certain criteria and delete it 
# .delete_many will delete every document that fits a condition
# collection.delete_mamy({}) will clear the entire collection 

# collection.update_one({ query for document }, {"$set":{"name":"abhikaboy"}})
# collection.update_many({ query for document }, {"$set":{"name":"abhikaboy"}}
# $set, $inc, $push (arrays)

# collection.count_documents({ query }) returns the number of documents that fit the condition

userMaterialBase = {
    "_id":0,
    "materials": { "water": 25, "food":50, "oxygen": 50, "happiness": 0, "population": 10, "vbucks":7000}
}

class Room:
    def __init__(_id,name,resources,speed,errorChance):
        self._id = _id # id of room 
        self.name = name # name of room 
        self.resouces = resources # the resouces that are linked with the room 
        self.speed = speed # the amount of seconds needed to switch collectable from false to true
        self.errorChance = errorChance # decimal for the chance of something going wrong. 
        self.collectable = False # if the user can click on the room to harvest it
    def asDict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "resouces": self.resources,
            "speed": self.speed,
            "errorChange": self.errorChance,
            "collectable": self.collectable
        }
class Shelter:  
    def __init__(self,_id, name ,rooms ):
        self.id = _id # wow
        self.name = name
        self.rooms = rooms
    def asDict(self):
        rooms = []
        for room in self.rooms:
            rooms.append(room.asDict())
        return{
            "_id": self.id,
            "name": self.name,
            "rooms": rooms,
        }

class Login(Resource):
    def get(self,name):
        # find if name is already in shelters
        # if it is not; respond and say "create a post to make a shelter" and here is your id 
        # if it is, respond with "okay here is your id"
        print(name)
        query = shelters.find_one({"name":name})
        if query is None:
            documentsNum = shelters.find().count()
            # make a new shelter and return with id 
            newShelter = Shelter(documentsNum,name,[])
            print(newShelter.asDict())
            shelters.insert_one(newShelter.asDict())

            documentsNum = resources.find().count()
            userMaterials = userMaterialBase
            userMaterials["_id"] = documentsNum
            resources.insert_one(
            userMaterials
        )
            return {"message": "Youre Cracked", "status": "200 OK", "data":{"_id":newShelter.id}}
        else:
            # return with the id 
            return {"message": "Youre Cracked", "staus": "200 OK", "data":{"_id":query["_id"]}}
    def post(self,name):
        return
    def put(self,name):
        return
class Rooms(Resource):
    def get(self,name):
        data = rooms.find_one({"name":name})
        if data is None:
            return {"message":"Meh","status":"404 RESOURCE NOT FOUND"}
        return {"message": "Yay", "status": "200 OK", "data":data}

class Materials(Resource):
    def get(self,userid):
        data = resources.find_one({"_id":userid})
        # Guard clause 
        if data is None:
            return {"message":"Meh","status":"404 RESOURCE NOT FOUND"}
        args = materialsGetParser.parse_args()
        queryMaterial = args["materialName"]
        if queryMaterial is None:
            return {"message":"Yeah","status":"200 OK", "data":data}
        return {"message":"Yeah","status":"200 OK", "data":data["materials"][queryMaterial]}
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
        return {"message":"Operation Successful", "status":"201 CREATED"}
    def put(self,userid):
        # parse parameters, increment the document with associated ID and then return succesful
        args = materialsPutParser.parse_args()
        queryMaterial = args["materialName"]
        resources.update_one({"_id":userid},{"$inc":{"materials.{material}".format(material=queryMaterial):args["amount"]}})  
        return {"mesage":"Successful","status": "200 OK"}

class Shop(Resource):
    def get(self):
        return
    def post(self):
        return
class Shelters(Resource):
    def get(self,shelterid):
        query = shelters.find_one({"_id":shelterid})
        return {"message":"Yeah","status":"200 OK", "data":query}
    def post(self,shelterid): 
        return "nice"
    def put(self,shelterid):
        args = shelterPutParser.parse_args()
        room_data = json.loads(args["room"])
        print("printing room!")
        print(room_data)
        shelters.update_one({"_id":shelterid},{"$push":{"rooms":room_data}})
        return {"message":"Yeah ok","status":"200 OK"}
class ShelterRooms(Resource):
    def get(self,shelterid,name):
        query = shelters.find_one({"_id":shelterid})
        rooms = query["rooms"]
        print(rooms)
        queried_room = list(filter(lambda room: room["name"] == name, rooms))[0]
        return {"message" : "POGGERS", "status": "200 OK", "data":queried_room}
    def put(self,shelterid,name):
        args = shelterRoomsPutParser.parse_args()
        print(args)
        query = shelters.find_one({"_id":shelterid})
        rooms = query["rooms"]
        indexOfRoom = 0
        for room in rooms:
            if(room["name"] == name):
                break
            indexOfRoom += 1
        print(args["value"])
        print("rooms."+str(indexOfRoom)+".collectable")
        query = shelters.update_one({"_id":shelterid},{"$set":{"rooms."+str(indexOfRoom)+".collectable":args["value"]}})
        queried_room = list(filter(lambda room: room["name"] == name, rooms))[0]
        print(queried_room)
        return {"message": "ok","status": "200 OK"}
        

class Clear(Resource):
    def get(self):
        return {}
    def put(self):
        return {}
    def post(self):
        print(shelters)
        shelters.delete_many({})
        resources.delete_many({})
        return {"message":"Yeah ok","status":"200 OK"}
# Resources Endpoints
api.add_resource(Materials,"/api/Materials/<int:userid>")
api.add_resource(Shelters,"/api/Shelters/<int:shelterid>")
api.add_resource(Rooms,"/api/Rooms/<string:name>")
api.add_resource(ShelterRooms,"/api/ShelterRooms/<int:shelterid>/<string:name>")
api.add_resource(Login,"/api/Login/<string:name>")
api.add_resource(Clear,"/api/Clear")
#api.add_resource(Shelters,"/api/Shelters/")    


if __name__ == "__main__":
    app.run(debug=True)