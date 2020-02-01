from flask import Flask, request
from flask_restplus import Resource, Api, reqparse, fields, marshal_with_field
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='myProject')

TODOS = {
    'todo1' : {'task' : 'build an API'}
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message = "TODO {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204
    @api.param('task','newTask')
    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task' : args['task']}
        TODOS[todo_id] = task
        return task, 201

class TodoList(Resource):
    def get(self):
        return TODOS
    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task' : args['task']}
        return TODOS[todo_id], 201


class ExampleCheck(Resource):
    test_object = {
        '_id_inspire12' : {
            'user_id' : 'inspire12',
            'user_name' : 'flask_user',
            'board' :
            [{
                'content_id' : 1,
                'title' : 'hi'
            },
                {
                    'content_id' : 2,
                    'title' : 'one_more_hi'
                }
            ]
        }
    }
    def get(self):
        return test_object


api.add_resource(ExampleCheck, '/example') #@api.resource('/example')
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)

