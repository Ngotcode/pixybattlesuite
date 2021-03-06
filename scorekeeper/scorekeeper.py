"""

scorekeeper.py

service that keeps score and makes it available for display


"""

# ------------------------- imports -------------------------
# stdlib
import time

# flask
from flask import Flask, request
from flask_restplus import Resource, Api

# local
from shared import constants as const


# ------------------------- data store -------------------------
# data is entirely transient; just store in-memory in one big dictionary

gamedata = const.getdefaultdata()
gamedata["metadatatime"] = time.time()
gamedata["scoretime"] = time.time()
gamedata["statetime"] = time.time()

# timer stuff is special
timermax = const.defaultgamelength
timermaxtime = time.time()
starttime = 0
starttimetime = time.time()


# ------------------------- server -------------------------
# app creation; would you normally put this in a function?
app = Flask(__name__)
api = Api(app)


# test endpoint
@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


@api.route("/state")
class GameState(Resource):
    def get(self):
        return gamedata

    def post(self):
        data = request.get_json()
        gamedata.update(request.get_json())
        gamedata["statetime"] = time.time()
        return gamedata

@api.route("/metadata")
class GameMetaData(Resource):
    def get(self):
        return gamedata

    def put(self):
        gamedata.update(request.get_json())
        gamedata["metadatatime"] = time.time()
        return gamedata

@api.route("/score")
class GameScore(Resource):
    def get(self):
        return gamedata

    def put(self):
        gamedata.update(request.get_json())
        gamedata["scoretime"] = time.time()
        return gamedata

@api.route("/timer/max")
class TimerMax(Resource):
    def get(self):
        return {"timermax": timermax, "timermaxtime": timermaxtime}

    def put(self):
        global timermax, timermaxtime
        data = request.get_json()
        timermax = data["timermax"]
        timermaxtime = time.time()
        return {"timermax": timermax, "timermaxtime": timermaxtime}

@api.route("/timer/start")
class TimerStart(Resource):
    def get(self):
        return {"starttime": starttime, "starttimetime": starttimetime}

    def put(self):
        global starttime, starttimetime
        data = request.get_json()
        starttime = data["starttime"]
        starttimetime = time.time()
        return {"starttime": starttime, "starttimetime": starttimetime}

@api.route("/data")
class GameData(Resource):
    def get(self):
        return gamedata

def main():
    app.run(debug=True)

# ------------------------- script starts here -------------------------
if __name__ == '__main__':
    main()




