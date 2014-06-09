#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pickle
from sys import argv
import logging
import itertools

import os
import os.path
from os import environ as env
import bottle
from bottle import request, response, get, post
import requests


bottle.debug(True)

NUMBER_OF_DATA = 10
TIMESPAN = 3
THRESHOLD = 0.9

logger = logging.getLogger('baptism')
logger.setLevel(logging.DEBUG)
fh_log = logging.FileHandler('logger.log')
fh_log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '<pre>'
    '<code style="padding: 0.5em 0 0.5em 1em; border-radius: 6px; border-width: 1px 1px 1px 6px;'
    'border-color: #eee #eee #eee #aa1e2d; border-style: solid; font-family: monospace;">'
    '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'
    '</code>'
    '</pre>')
fh_log.setFormatter(formatter)
logger.addHandler(fh_log)
logger.info('logger initialized')



@get('/logs')
def get_logs():
    logger.info('/logs')
    logger.debug('trying to open log file')
    out = ""
    for filename in ["dbg_aaa.txt", "dbg_bbb.txt", "dbg_ccc.txt", "dbg_ddd.txt", 'dbg_post.txt']:
        if os.path.isfile(filename):
            out += ("<pre>{0}</pre> exists!<br>".format(filename))
            with open(filename, 'r') as fh:
                out += ("<pre><code>{0}</code></pre>".format(fh.read()))
        else:
            out += (filename + "does not exist!<br>")
    with open('logger.log', 'r') as fh:
        logger.debug('opened successfully')
        out += "<h1>LOGS</h1>" + fh.read()
    return out


@get('/')
def index():
    logger.info('/')
    response.content_type = 'text/plain; charset=utf-8'
    ret = 'Hello world, I\'m %s!\n\n' % os.getpid()
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
    logger.info("/push")
    try:
        logger.debug('entering try block...')
        logger.debug('request.json =', request.json)
        logger.debug('aaa')

        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00001")
        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00002")
        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00003")
        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00004")
        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00005")
        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00011")
        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00012")
        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00013")
        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00014")
        logger.debug("aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa aaaa 00015")
        with open('dbg_aaa.txt', 'w') as fh:
            fh.write(str(type(request.json)))
        logger.debug("investigating: type(request.json) =", type(request.json))
        with open('dbg_bbb.txt', 'w') as fh:
            fh.write(str(str(request.json)))
        logger.debug("investigating: str(request.json) =", str(request.json))
        with open('dbg_ccc.txt', 'w') as fh:
            fh.write(str(list(request.json)))
        logger.debug("investigating: list(request.json) =", list(request.json))
        with open('dbg_ddd.txt', 'w') as fh:
            fh.write(str(dict(request.json)))
        logger.debug("investigating: dict(request.json) =", dict(request.json))
        logger.debug('request =', request)
        logger.debug('bbb')
        logger.debug("request.json['series'] =", request.json['series'])
        input_data = [[cell['type']
                       for cell in request.json['series']]]
        logger.debug("input_data =", input_data)
        input_types = get_types(input_data)
        logger.debug("input_types =", input_types)
        # output = get_sequences(input_types, input_data, THRESHOLD)
        output = [["popsutttte"]]
        logger.debug("output =", output)
        result = {"input": request.json['series'], "output": [list(cell)
                                                              for cell in list(output)],
                  "--gadekmolenda--temp": output}
        logger.debug("result =", result)
        logger.debug('performing POST request...')
        with open('dbg_post.txt', 'w') as fh:
            fh.write(str(result))
        # requests.post("http://integracja.herokuapp.com/rest/sequences",
        #               data=json.dumps(result),
        #               headers={'content-type': 'application/json'} )
        logger.debug('POST done')
    except Exception as e:
        logger.debug("except Exception as e")
        logger.exception(e)
    except BaseException as e:
        logger.debug("except BaseException as e")
        logger.exception(e)
    except:
        logger.debug("except")
        logger.debug("weird shit happend")
    logger.debug("I'm done")
    return "OKAY"


@get('/results')
def results():
    old_data = ["nothing_here"]
    try:
        with open("res.txt", "r") as fh:
            old_data = json.loads(fh.read())
    except Exception as e:
        return str(e)
    return str(old_data)


@get('/buba')
def buba():
    logger.info('/buba')
    logger.debug("so... let's begin")
    try:
        logger.debug("a = 'a'")
        a = 'a'
        logger.debug("a['stp']")
        a['stp']
    except Exception as e:
        logger.debug("except Exception as e")
        logger.exception(e)
    except BaseException as e:
        logger.debug("except BaseException as e")
        logger.exception(e)
    except:
        logger.debug("except")
        logger.debug("weird shit happend")
    logger.debug("done here")
    return "OKAY"


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
    while (len(sequences)) > 0:
        candidates = generate_candidates(sequences)
        sequences = find_frequent_sequences(candidates, data, threshold)
        to_return = update_set(to_return, sequences)
    return to_return

logger.info("starting bottle")
bottle.run(host='0.0.0.0', port=argv[1])

# data = get_data(NUMBER_OF_DATA, TIMESPAN)
# print "GETDATA"
# print data
# types = get_types(data)
# #print(types)
# print "get_sequences"
# res = get_sequences(types, data, THRESHOLD)
# print {"input": data, "output": [list(x) for x in res]}
