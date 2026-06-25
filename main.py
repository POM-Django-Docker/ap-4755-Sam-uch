import json
from http.server import HTTPServer, BaseHTTPRequestHandler

USERS_LIST = [
    {
        "id": 1,
        "username": "theUser",
        "firstName": "John",
        "lastName": "James",
        "email": "john@email.com",
        "password": "12345",
    }
]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_response(self, status_code=200, body=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body if body else {}).encode('utf-8'))

    def _pars_body(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        return json.loads(self.rfile.read(content_length).decode('utf-8'))  # <--- Gets the data itself

    def do_GET(self):
        global USERS_LIST

        if self.path == '/reset':
            USERS_LIST = [
                {
                    "id": 1,
                    "username": "theUser",
                    "firstName": "John",
                    "lastName": "James",
                    "email": "john@email.com",
                    "password": "12345",
                }
            ]
            self._set_response(200, USERS_LIST)

        elif self.path == '/users':
            self._set_response(200, USERS_LIST)

        elif self.path.startswith('/user/'):
            username = self.path[len('/user/'):]
            user = next((u for u in USERS_LIST if u['username'] == username), None)
            if user:
                self._set_response(200, user)
            else:
                self._set_response(400, {'error': 'User not found'})

    def do_POST(self):
        global USERS_LIST

        try:
            body = self._pars_body()
        except Exception:
            self._set_response(400, {})
            return

        def is_valid(user):
            keys = {'id', 'username', 'firstName', 'lastName', 'email', 'password'}
            return (isinstance(user, dict) and set(user.keys()) == keys and
                    isinstance(user['id'], int) and
                    all(isinstance(user[k], str) for k in keys - {'id'}))

        if self.path == '/user':
            if not is_valid(body):
                self._set_response(400, {})
                return
            if any(u['id'] == body['id'] for u in USERS_LIST):
                self._set_response(400, {})
                return
            USERS_LIST.append(body)
            self._set_response(201, body)

        elif self.path == '/user/createWithList':
            if not isinstance(body, list) or not all(is_valid(u) for u in body):
                self._set_response(400, {})
                return
            existing_ids = {u['id'] for u in USERS_LIST}
            if any(u['id'] in existing_ids for u in body):
                self._set_response(400, {})
                return
            USERS_LIST.extend(body)
            self._set_response(201, body)


    def do_PUT(self):
        global USERS_LIST

        try:
            body = self._pars_body()
        except Exception:
            self._set_response(400, {'error': 'not valid request data'})
            return

        if self.path.startswith('/user/'):
            try:
                user_id = int(self.path[len('/user/'):])
            except ValueError:
                self._set_response(400, {'error': 'not valid request data'})
                return

            keys = {'username', 'firstName', 'lastName', 'email', 'password'}
            if not (isinstance(body, dict) and set(body.keys()) == keys and
                    all(isinstance(body[k], str) for k in keys)):
                self._set_response(400, {'error': 'not valid request data'})
                return

            user_index = next((i for i, u in enumerate(USERS_LIST) if u['id'] == user_id), None)
            if user_index is None:
                self._set_response(404, {'error': 'User not found'})
                return

            USERS_LIST[user_index].update(body)
            self._set_response(200, USERS_LIST[user_index])

    def do_DELETE(self):
        global USERS_LIST

        if self.path.startswith('/user/'):
            try:
                user_id = int(self.path[len('/user/'):])
            except ValueError:
                self._set_response(404, {'error': 'User not found'})
                return

            user_index = next((i for i, u in enumerate(USERS_LIST) if u['id'] == user_id), None)
            if user_index is None:
                self._set_response(404, {'error': 'User not found'})
                return

            USERS_LIST.pop(user_index)
            self._set_response(200, {})


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, host='0.0.0.0', port=8000):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
