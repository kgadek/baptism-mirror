#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

import os
from os import environ as env
import bottle
from bottle import request, response, get, post, HTTPResponse
import requests


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


def get_data(number_of_data, timespan):
    data = []
    for _ in range(number_of_data):
        post_payload = {'config': '1', 'timespan': timespan}
        post_request = requests.post("http://immense-refuge-2812.herokuapp.com/sample/learn", params=post_payload)
        if post_request.status_code == 200:
            get_request = requests.get("http://immense-refuge-2812.herokuapp.com/sample/learn?config=1")
            if get_request.status_code == 200:
                new_data = get_request.json()['series']
                for x in new_data:
                    x.pop('name')
                data.append(new_data)
    return data


bottle.run(host='0.0.0.0', port=argv[1])
#print(get_data(10, 10))