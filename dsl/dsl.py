import json

from dsl_errors import MalformedCommandError, TypeNotRecognizedError
from fa_manager import DFA_Manager, NFA_Manager, TM_Manager


def read_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        triageLine(line)


def load_from_file(filename, varname, env):
    with open(filename, "r") as f:
        rawJson = json.loads(f.read())

    if rawJson["type"].lower() == "dfa":
        created = DFA_Manager.from_json(rawJson)
    elif rawJson["type"].lower() == "nfa":
        created = NFA_Manager.from_json(rawJson)
    elif rawJson["type"].lower() == "tm":
        created = TM_Manager.from_json(rawJson)
    else:
        raise TypeNotRecognizedError(
            f'JSON claims type {rawJson["type"]}, which is not a valid type.'
        )

    env[varname] = created


def triageLine(line, env):
    if line.startswith("LOAD "):
        tokens = line.split(" ")

        if tokens[-2] != "AS":
            raise MalformedCommandError()

        filename = " ".join(tokens[1:-2])
        filename.removeprefix('\"')
        filename.removesuffix('\"')

        varname = tokens[-1]

        load_from_file(filename, varname, env)


if __name__ == "__main__":
    env = dict()

    triageLine("LOAD \"hell yeah brother\" AS hyb", env)
