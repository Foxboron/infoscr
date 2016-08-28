import subprocess
import threading
import time
import uuid

from queue import PriorityQueue
from os import listdir
from flask import Flask, jsonify, session, request
from collections import deque
from functools import wraps


SCENE = "./scenes/"
PAUSE_TIME = 5
CHARACTER_TIME = 0.001

USE_AUTH = True
AUTH={}
STATE = {}


def run_program(file):
    with subprocess.Popen([file], stdout=subprocess.PIPE) as proc:
        output = proc.stdout.read().decode("utf-8")
    return output


def get_scene(scene):
    out = run_program(SCENE+scene)
    return {"scene": scene,
            "text": out}

def new_session():
    state = deque()
    for i in listdir(SCENE):
        state.append(get_scene(i))
    return state


def Token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        session_state = None
        if request.headers.get("Session",False):
            sess = request.headers["Session"]
            if sess in STATE.keys():
                session_state = STATE[sess]
            else:
                session_state = {"id": sess,
                                 "state": new_session()}
                STATE[sess] = session_state
        else:
            sess = uuid.uuid4()
            session_state = {"id": sess,
                             "state": new_session()}
            STATE[sess] = session_state
        return func(session_state, *args, **kwargs)
    return check_token


app = Flask(__name__)


@app.route('/msg', methods=['POST'])
def add_important():
    for k,v in STATE.items():
        v["state"].appendleft({"scene": "notification",
                      "text": request.json["msg"]})
    return ""


@app.route('/settings', methods=['GET'])
@Token
def get_settings(session):
    return jsonify({'character_time': CHARACTER_TIME,
                    'pause_time': PAUSE_TIME,
                    'id': session['id']})


@app.route('/scenes', methods=['GET'])
def get_scenes():
    scenes = listdir("./scenes")
    return jsonify({'scenes': scenes})


@app.route('/scene/', methods=['GET'])
@Token
def get_next_scene(state):
    print(state)
    ret = state["state"].popleft()
    ret["id"] = state["id"]
    return jsonify(ret)


if __name__ == '__main__':
    app.run()
