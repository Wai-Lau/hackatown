import json
import md5
import random
import datetime
from flask import Flask, render_template, request


app = Flask(__name__)
hash_data = {}
success = json.dumps({'success':True}), 200, {'ContentType':'application/json'}
fail = json.dumps({'success':False}), 500, {'ContentType':'application/json'}
api_key = 'AIzaSyAl-P2j3M-a-IjP7Vfkp_ChinCQMTsb__0'

@app.route('/group/<key>')
def group(key):
    if key not in hash_data:
        return render_template("main.html", message="")
    markers = hash_data[key]
    return render_template("map.html", message="",
                           api_key=api_key,
                           markers=markers,
                           key=key)

@app.route('/')
def main():
    return render_template("main.html", message="")

@app.route('/add_marker/<key>', methods=['POST'])
def add_marker(key):
    lat_lng_json = request.get_json()['latLng']
    name = request.get_json()['name']
    hash_data[key][name] = {'position':json.loads(lat_lng_json)}
    return success

@app.route('/remove_marker/<key>', methods=['POST'])
def remove_marker(key):
    name = request.get_json()['name']
    print(name)
    print([n for n in hash_data[key]])
    if key in hash_data and name in hash_data[key]:
        del hash_data[key][name]
        return success
    return fail

@app.route('/create_group')
def create_group():
    # Create group hash here
    now = datetime.datetime.now()
    rand = random.random()
    m = md5.new()
    m.update(str(now)+str(rand))
    key = m.hexdigest().encode('utf-8').strip()
    hash_data[key] = {}
    return json.dumps({'success':True, 'key': key}), 200, {'ContentType':'application/json'}

@app.route('/check_dirty/<key>', methods=['POST'])
def check_dirty(key):
    keys = request.get_json()['keys']
    clean = True
    for k in keys:
        if k not in hash_data[key]:
            clean = False
            break
    if clean:
        for n in hash_data[key]:
            if n not in keys:
                clean = False
                break
    if clean:
        return success
    return fail
