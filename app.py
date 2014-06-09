#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

import os
from os import environ as env
import bottle
from bottle import request, response, get, post, HTTPResponse
import requests
import itertools


bottle.debug(True)


NUMBER_OF_DATA = 10
TIMESPAN = 3
THRESHOLD = 0.9


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
        fh.write("=====try A=====")
        try:
            content = request.forms.get('content')[0:100]
            fh.write("=====A read=====")
            fh.write(content)
            fh.write("=====A done=====")
        except Exception, e:
            fh.write("=====A fail=====\n" + e.message + '\n\n')

        fh.write("=====try B=====")
        try:
            content = request.json
            fh.write("=====B read=====")
            content = str(content)
            fh.write("=====B str=====")
            fh.write(content)
            fh.write("=====B done=====")
        except Exception, e:
            fh.write("=====B fail=====\n" + e.message + '\n\n')


@get('/example_get/<doc_id>')
def example_get(doc_id):
    # yes, this is a sec–hole :) if you're bored: do whatever you like!
    doc_file = os.path.join("tmp", doc_id)
    with open(doc_file, "r") as fh:
        return fh.read()
    # noinspection PyUnreachableCode
    return HTTPResponse("No such file!", status=400)


def get_data(number_of_data, timespan):
    return [get_segment(timespan) for _ in range(number_of_data)]


def get_segment(timespan):
    post_payload = {'config': '1', 'timespan': timespan}
    post_request = requests.post("http://immense-refuge-2812.herokuapp.com/sample/learn", params=post_payload)
    if post_request.status_code != 200:
        raise Exception()
    get_request = requests.get("http://immense-refuge-2812.herokuapp.com/sample/learn?config=1")
    if get_request.status_code != 200:
        raise Exception()
    data = get_request.json()['series']
    return [x['type'] for x in data]


def get_types(data):
    return {tuple([x]) for subdata in data for x in subdata}


def generate_candidates(types):
    to_return = {
        t1 + (t2[-1],)
        for t1, t2 in itertools.product(types, types)
        if t1[:-1] == t2[:-1]
    }
    return to_return


def find_frequent_sequences(candidates, data, threshold):
    threshold *= len(data)
    to_return = {
        c for c in candidates
        if sum([exists_in(c, d) for d in data]) > threshold
    }
    return to_return


def exists_in(sequence, data):
    for d in data:
        if d == sequence[0]:
            sequence = sequence[1:]
            if len(sequence) == 0:
                return True
    return False


def update_set(to_return, sequences):
    for s in sequences:
        for i in range(len(s)):
            try:
                to_return.remove(s[:i] + s[i + 1:])
            except KeyError:
                pass
    to_return.update(sequences)
    return to_return


def get_sequences(types, data, threshold):
    to_return = set()
    sequences = types
    while(len(sequences)) > 0:
        candidates = generate_candidates(sequences)
        sequences = find_frequent_sequences(candidates, data, threshold)
        to_return = update_set(to_return, sequences)
    return to_return


bottle.run(host='0.0.0.0', port=argv[1])
# data = get_data(NUMBER_OF_DATA, TIMESPAN)
# print(data)
# types = get_types(data)
##print(types)
#
# print(get_sequences(types, data, THRESHOLD))