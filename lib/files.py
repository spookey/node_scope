from os import path
from codecs import open as c_open
from json import loads, dumps


def readfile(location):
    if path.exists(location):
        with c_open(location, 'r') as fl:
            return fl.read()


def readjson(location):
    res = readfile(location)
    if res:
        return loads(res)


def writefile(location, content):
    with c_open(location, 'w') as fl:
        return fl.write(content)


def writejson(location, content):
    return writefile(location, dumps(content, indent=2))
