# /usr/bin/python
# -*- codeing: utf-8 -*-


# $ curl localhost/mp/publish_handler.py
# $ curl localhost/mp/publish_handler.py/index
def index(req):
    return 'publisher'

# $ curl localhost/mp/publish_handler.py/hello
def hello(req):
    return 'Hello world'