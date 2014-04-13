#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

import os
from os import environ as env
import bottle
from bottle import request, response, get, post, HTTPResponse


bottle.debug(True)

@get('/')
def index():
    response.content_type = 'text/plain; charset=utf-8'
    ret =  'Hello world, I\'m %s!\n\n' % os.getpid()
    ret += 'Request vars:\n'
    for k, v in request.environ.iteritems():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    ret += '\n'
    ret += 'Environment vars:\n'

    for k, v in env.iteritems():
        if 'bottle.' in k:
            continue
        ret += '%s=%s\n' % (k, v)

    return ret


@post('/example_post/<doc_id>')
def example_post(doc_id):
    # yes, this is a sec–hole :) if you're bored: do whatever you like!
    doc_file = os.path.join("tmp", doc_id)

    with open(doc_file, "w") as fh:
        content = request.forms.get('content')[0:100]
        fh.write(content)


@get('/example_get/<doc_id>')
def example_get(doc_id):
    # yes, this is a sec–hole :) if you're bored: do whatever you like!
    doc_file = os.path.join("tmp", doc_id)
    with open(doc_file, "r") as fh:
        return fh.read()
    # noinspection PyUnreachableCode
    return HTTPResponse("No such file!", status=400)


bottle.run(host='0.0.0.0', port=argv[1])
