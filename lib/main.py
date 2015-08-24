from lib.config import load
from lib.retrieve import query


def main():
    conf = load()
    mesh = query(conf['connection'])

    print(mesh)
