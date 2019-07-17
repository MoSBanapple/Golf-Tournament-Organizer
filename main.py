# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
#from flask import Flask
import flask
from google.cloud import datastore
client = datastore.Client()
import json

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)

def getID():
    q = client.query(kind="Tournament")
    results = list(q.fetch())
    currentID = 0
    for t in results:
        if int(t["id"]) >= currentID:
            currentID = int(t["id"]) + 1
    return currentID


@app.route("/")
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'
    
    
@app.route("/tournaments", methods=['GET', 'POST'])
def tournaments():
    if flask.request.method == 'GET':
        q = client.query(kind="Tournament")
        results = list(q.fetch())
        dict = {"tournaments":results}
        return json.dumps(dict)
    elif flask.request.method == 'POST':
        name = flask.request.form.get("name")
        host = flask.request.form.get("host")
        date = flask.request.form.get("date")
        time = flask.request.form.get("time")
        fee = float(flask.request.form.get("fee"))
        courseid = int(flask.request.form.get("courseid"))
        scores = flask.request.form.getlist('scores')
        id = getID()
        ckey = client.key('Tournament', str(id))
        task = datastore.Entity(key=ckey)
        task.update({
            'name':name,
            'id':id,
            'host':host,
            'date':date,
            'time':time,
            'fee':fee,
            'courseid':courseid,
            'scores':scores
        })
        client.put(task)
        return json.dumps(task)
    return "should not get here"
    
@app.route("/tournaments/<torID>", methods=['GET','POST','PUT','DELETE'])
def tournamentSpec(torID):
    if flask.request.method == 'GET':
        key = client.key('Tournament', torID)
        task = client.get(key)
        return json.dumps(task)
    elif flask.request.method == 'PUT':
        name = flask.request.form.get("name")
        host = flask.request.form.get("host")
        date = flask.request.form.get("date")
        time = flask.request.form.get("time")
        fee = float(flask.request.form.get("fee"))
        courseid = int(flask.request.form.get("courseid"))
        scores = flask.request.form.getlist('scores')
        id = int(torID)
        ckey = client.key('Tournament', str(id))
        task = datastore.Entity(key=ckey)
        task.update({
            'name':name,
            'id':id,
            'host':host,
            'date':date,
            'time':time,
            'fee':fee,
            'courseid':courseid,
            'scores':scores
        })
        client.put(task)
        return json.dumps(task)
    elif flask.request.method == 'DELETE':
        key = client.key('Tournament', torID)
        client.delete(key)
        return "200 OK"
    return "should not get here"

@app.route("/users", methods=['GET', 'POST'])
def user():
    if flask.request.method == 'GET':
        q = client.query(kind="User")
        results = list(q.fetch())
        dict = {"users":results}
        return json.dumps(dict)
    elif flask.request.method == 'POST':
        name = flask.request.form.get("username")
        hosting = list(map(int, flask.request.form.getlist('hosting')))
        playing = list(map(int, flask.request.form.getlist('playing')))
        ckey = client.key('User', name)
        task = datastore.Entity(key=ckey)
        task.update({
            'username':name,
            'hosting':hosting,
            'playing':playing
        })
        client.put(task)
        return json.dumps(task)
    return "should not get here"
    
@app.route("/users/<name>", methods=['GET','POST','PUT','DELETE'])
def userSpec(name):
    if flask.request.method == 'GET':
        key = client.key('User', name)
        task = client.get(key)
        return json.dumps(task)
    elif flask.request.method == 'PUT':
        hosting = list(map(int, flask.request.form.getlist('hosting')))
        playing = list(map(int, flask.request.form.getlist('playing')))
        ckey = client.key('User', name)
        task = datastore.Entity(key=ckey)
        task.update({
            'username':name,
            'hosting':hosting,
            'playing':playing
        })
        client.put(task)
        return json.dumps(task)
    elif flask.request.method == 'DELETE':
        key = client.key('User', name)
        client.delete(key)
        return "200 OK"
    return "should not get here"

@app.route("/courses", methods=['GET', 'POST'])
def courses():
    if flask.request.method == 'GET':
        q = client.query(kind="Course")
        results = list(q.fetch())
        dict = {"courses":results}
        return json.dumps(dict)
    elif flask.request.method == 'POST':
        name = flask.request.form.get("name")
        id = int(flask.request.form.get("id"))
        location = flask.request.form.get("location")
        par = list(map(int, flask.request.form.getlist('par')))
        ckey = client.key('Course', str(id))
        task = datastore.Entity(key=ckey)
        task.update({
            'name':name,
            'id':id,
            'location':location,
            'par':par
        })
        client.put(task)
        return json.dumps(task)
    return "should not get here"

@app.route("/courses/<id>", methods=['GET','POST','PUT','DELETE'])
def courseSpec(id):
    if flask.request.method == 'GET':
        key = client.key('Course', id)
        task = client.get(key)
        return json.dumps(task)
    elif flask.request.method == 'PUT':
        name = flask.request.form.get("name")
        location = flask.request.form.get("location")
        par = list(map(int, flask.request.form.getlist('par')))
        ckey = client.key('Course', str(id))
        task = datastore.Entity(key=ckey)
        task.update({
            'name':name,
            'id':id,
            'location':location,
            'par':par
        })
        client.put(task)
        return json.dumps(task)
    elif flask.request.method == 'DELETE':
        key = client.key('Course', id)
        client.delete(key)
        return "200 OK"
    return "should not get here"

@app.route("/absent", methods=['GET','POST','PUT','DELETE'])
def absent():
    
    complete_key = client.key('Task', 'sample_task')
    task = datastore.Entity(key=complete_key)
    task.update({
        'paramA' : 4,
        'paramB' : 5,
        'listParam' : ["abc"]
    })
    client.put(task)
    
    """
    with client.transaction():
        key = client.key('Task', 'sample_task')
        task = client.get(key)
        dict = {}
        dict["test"] = task['listParam']
        return json.dumps(task)
    """
    q = client.query(kind="Task")
    results = list(q.fetch())
    dict = {"list":results}
    return str(flask.request.args.getlist("testArg"))

@app.route("/absent/<abs>")
def absent2(abs):
    testStr = "testy"
    if abs == testStr:
        return "ablong"
    return "absent " + abs
    

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
