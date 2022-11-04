from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"details": "Invalid data"}, 400))

    task_chosen = Task.query.get(task_id)

    if not task_chosen:
        return abort(make_response({"msg": f"Could not find the task with id = {task_id}"}, 404))
    
    return task_chosen


@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201


@task_bp.route('', methods=['GET'])
def get_or_sort_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()  
    else:
        tasks = Task.query.all() 
        # tasks is a list of Task objects. Model.query.all() return a list of objects.
        # task.to_dict() return a dictionary, as defined in to_dict method in Task(a class). Task is a db model we created.

    result = []
    for task in tasks:
        result.append(task.to_dict())
    
    return jsonify(result), 200

###### Solution 2 using lambda and sorted function ##########
# @task_bp.route('', methods=['GET'])
# def get_or_sort_tasks():
#     tasks = Task.query.all() 
#     result = []
#     for task in tasks:
#         result.append(task.to_dict())
#     sort_query = request.args.get("sort")
#     if sort_query == "asc":
#         result = sorted(result, key=lambda x: x['title'])
#     elif sort_query == "desc":
#         result = sorted(result, key=lambda x: x['title'], reverse=True)   
#     return jsonify(result), 200


@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    task_chosen = get_task_from_id(task_id)

    return jsonify({"task":task_chosen.to_dict()}), 200


@task_bp.route('/<task_id>', methods=['PUT'])
def update_one_task(task_id):
    update_task = get_task_from_id(task_id)

    request_body = request.get_json()

    update_task.title = request_body["title"]
    update_task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": update_task.to_dict()}), 200


@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    delete_task = get_task_from_id(task_id)

    db.session.delete(delete_task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{delete_task.title}" successfully deleted'}), 200






    
    







