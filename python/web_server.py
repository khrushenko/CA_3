import json
from bottle import *
import bottle
# from file_server import *
import file_server

result = ''


# Returns static file. Used for getting JavaScript files from /scripts folder
@bottle.get('/scripts/:filename#.*#')
def send_static_javascript(filename):
    return static_file(filename, root='../scripts/')


# Returns static file. Used for getting CSS files from /styles folder
@bottle.get('/styles/:filename#.*#')
def send_static_css(filename):
    return static_file(filename, root='../styles/')


# Returns worker page
@bottle.get('/')
def index():
    return static_file('index.html', root='../HTML/')


# CREATE
@post('/create')
def bottle_create():
    name = request.forms.get('name')
    about = request.forms.get('about')
    state = request.forms.get('state')
    global result
    result = file_server.add(name, about, state)
    if result == file_server.result_OK:
        result = 'Added successfully'


# READ
@get('/read')
def bottle_read():
    return json.dumps(file_server.read())
    # return file_server.read()


# UPDATE
@post('/update')
def bottle_update():
    name = request.forms.get('name')
    field = request.forms.get('field')
    value = request.forms.get('value')
    global result
    result = file_server.update(name, field, value)
    if result == file_server.result_OK:
        result = 'Changed successfully'


# DELETE
@post('/delete')
def bottle_delete():
    global result
    result = file_server.delete(request.body.read())
    if result == file_server.result_OK:
        result = 'Deleted successfully'


# Returns result of the last operation
@get('/result')
def bottle_result():
    # print(result)
    if result == file_server.error_file_exists:
        return json.dumps({'color': 'red', 'result': result})
    return json.dumps({'color': 'green', 'result': result})


if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)