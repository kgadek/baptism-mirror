#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from sys import argv
import itertools

import os
from os import environ as env
import bottle
from bottle import request, response, get, post
import requests


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


@post('/push')
def pushed_ztis_data():
    old_data = []
    # noinspection PyBroadException
    try:
        with open("res.txt", "rb") as fh:
            old_data = pickle.load(fh)
    except:
        pass
    data = request.json
    types = get_types(data)
    res = get_sequences(types, data, THRESHOLD)
    old_data.append(res)
    with open("res.txt", "wb") as fh:
        pickle.dump(old_data, fh)


@get('/results')
def results():
    old_data = []
    try:
        with open("res.txt", "rb") as fh:
            old_data = pickle.load(fh)
    except:
        pass
    return str(old_data)







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
    print "DEBUG", "get_request.json() =", get_request.json()
    data = get_request.json()['series']
    print "DEBUG", "data =", data
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
# print "GETDATA"
# print data
# types = get_types(data)
# #print(types)
# print "get_sequences"
# print get_sequences(types, data, THRESHOLD)