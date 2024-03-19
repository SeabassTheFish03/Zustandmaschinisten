import numpy as np
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA


import json
# Unit Vector and Angle Between from:
# https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

# This function just makes the edge list for displaying the dfa. It loses the input character
def JSONtoManimEdges(rawJson): 
    rawJson["transitions"] = merge_duplicate_edges(rawJson)
    edges = []
    edge_config = dict()
    for start in rawJson["transitions"]:
        for symbol in rawJson["transitions"][start]:
            for end in rawJson["transitions"][start][symbol]:
                newEdge = tuple((start, end))
                edges.append(newEdge)
                
                if (start, end) not in edge_config:
                    edge_config[(start, end)] = dict()
                edge_config[(start, end)]["label"] = symbol
    return edges, edge_config

def NFAtoManimEdges(nfa):
    edges = []
    edge_config = dict()
    transitions = merge_duplicate_edges({"transitions": nfa.transitions})
    for start in transitions:
        for symbol in transitions[start]:
            for end in transitions[start][symbol]:
                edges.append((start, end))

                if (start, end) not in edge_config:
                    edge_config[(start, end)] = dict()
                edge_config[(start, end)]["label"] = symbol
    return edges, edge_config

def DFAtoManimEdges(dfa):
    edges = []
    edge_config = dict()
    for start in dfa.transitions:
        for symbol in dfa.transitions[start]:
            end = dfa.transitions[start][symbol]
            edges.append((start, end))

            if (start, end) not in edge_config:
                edge_config[(start, end)] = dict()
            edge_config[(start, end)]["label"] = symbol
    return edges, edge_config

def JSONToDFA(rawJson):
    return DFA(
        states = set(rawJson["states"]),
        input_symbols = rawJson["input_symbols"],
        transitions = rawJson["transitions"],
        initial_state = rawJson["initial_state"],
        final_states = set(rawJson["final_states"]),
        allow_partial=True,
    )
def JSONToNFA(rawJson):
    return NFA(
        states = set(rawJson["states"]),
        input_symbols = rawJson["input_symbols"],
        transitions = rawJson["transitions"],
        initial_state = rawJson["initial_state"],
        final_states = set(rawJson["final_states"])
    )
def FAToMobj(fa):
    from labeledEdgeDiGraph import LabeledEdgeDiGraph

    vertex_config = {v: {"flags": []} for v in fa.states}

    vertex_config[fa.initial_state]["flags"].append("i")

    for v in fa.final_states:
        vertex_config[v]["flags"].append("f")

    if isinstance(fa, NFA):
        edges, edge_config = NFAtoManimEdges(fa)
    elif isinstance(fa, DFA):
        edges, edge_config = DFAtoManimEdges(fa)

    return LabeledEdgeDiGraph(
        vertices = fa.states,
        edges = edges,
        labels = True,
        layout = "spectral",
        vertex_config = vertex_config,
        edge_config = edge_config,
    )

def merge_duplicate_edges(rawJson):
    new_transitions = dict()

    for start in rawJson["transitions"]:
        finishes = list()
        new_transitions[start] = dict()

        for symbol in rawJson["transitions"][start]:
            for end in rawJson["transitions"][start][symbol]:
                finishes.append([symbol, [end]])
        finishes.sort(key=lambda x: x[1])

        compiled = [finishes[0]]
        for finish in finishes[1:]:
            if finish[1] == compiled[-1][1]:
                compiled[-1][0] = ", ".join([compiled[-1][0], finish[0]])
            else:
                compiled.append(finish)
        
        for new_edge in compiled:
            new_transitions[start][new_edge[0]] = new_edge[1]

    return new_transitions

if __name__ == "__main__":
    with open("official_nfa.json", "r") as f:
        print(JSONtoManimEdges(json.loads(f.read())))
