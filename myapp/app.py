#!flask/bin/python
from re import UNICODE
from flask import Flask, json, jsonify, abort, make_response, request

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Do Cloud Lab Assignment',
        'description': u'Clone a repository from github with docker and run it.', 
        'done': True
    },
    {
        'id': 2,
        'title': u'Learn Flask',
        'description': u'Learning Flask ', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/author',methods=['GET'])
def author():
    return jsonify({'Author':{'Name':'Adithya Narayan','Registeration Number':'19BBS0068','Slot':'CBS3005 L25+26'}})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
	#'description':request.json['description'],
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != UNICODE:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not UNICODE:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

@app.route('/test1')
def test1():
    return "Success"

@app.route('/addition/<int:a>/<int:b>')
def addition(a,b):
    return make_response(jsonify({'result':a+b}))
