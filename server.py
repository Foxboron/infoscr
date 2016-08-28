import subprocess

from queue import PriorityQueue
from os import listdir
from flask import Flask, jsonify

STATE = PriorityQueue()

app = Flask(__name__)

def run_program(file):
    with subprocess.Popen([file], stdout=subprocess.PIPE) as proc:
        output = proc.stdout.read().decode("utf-8")
    return output

def populate_state():
    for i in listdir("./scenes"):
        STATE.put((10, i))

def get_scene(scene):
    out = run_program("./scenes/"+scene)
    return jsonify({"scene": scene,
                    "text": out})



@app.route('/settings', methods=['GET'])
def get_settings():
    return jsonify({'character_time': 0.001,
                    'pause_time': 3})


@app.route('/scenes', methods=['GET'])
def get_scenes():
    scenes = listdir("./scenes")
    return jsonify({'scenes': scenes})


@app.route('/scene/<scene>', methods=['GET'])
def get_specefic_scene(scene):
    return get_scene(scene)


@app.route('/scene', methods=['GET'])
def get_next_scene():
    if STATE.empty():
        populate_state()
    _, scene = STATE.get()
    return get_scene(scene)


if __name__ == '__main__':
    app.run(debug=True)
