import sys
import json
import copy

from abc import ABC, abstractmethod

from automata.fa.dfa import DFA

from labeledEdgeDiGraph import LabeledEdgeDiGraph

class Automaton_Manager(ABC):
    @abstractmethod
    def from_json(self, rawStr):
        pass

    @abstractmethod
    def from_mobj(self, mobj):
        pass

    @abstractmethod
    def next_state(self, symbol):
        pass

class DFA_Manager(Automaton_Manager):
    def __init__(self, auto, mobj):
        self.auto = auto
        self.mobj = mobj

        self.dfa = self.auto

    @classmethod
    def from_json(cls, rawStr):
        if isinstance(rawStr, str):
            try:
                rawJson = json.loads(rawStr)
            except json.decoder.JSONDecodeError as e:
                print(f"Malformed JSON: {e}", file=sys.stderr)
                raise SystemExit(1)

        elif isinstance(rawStr, dict):
            rawJson = rawStr
        else:
            print(f"Given input of type {type(rawStr)}, expected str or dict")
            raise SystemExit(1)

        auto_type = rawJson["type"]
        if auto_type != "dfa":
            print(f"The json indicates this automaton is of type {auto_type}. Expected dfa.")
            raise SystemExit(1)
        else:
            allow_part = rawJson.get("allow_partial", False)
            
            auto = DFA(
                states        = set(rawJson["states"]),
                input_symbols = rawJson["input_symbols"],
                transitions   = rawJson["transitions"],
                initial_state = rawJson["initial_state"],
                final_states  = set(rawJson["final_states"]),
                allow_partial = allow_part,
            )

            vertex_config = {vertex: {"flags": []} for vertex in rawJson["states"]}
            vertex_config[rawJson["initial_state"]]["flags"].append("i")
            
            for vertex in rawJson["final_states"]:
                vertex_config[vertex]["flags"].append("f")

            edges, edge_config = cls._json_to_mobj_edges(rawJson)
            mobj = LabeledEdgeDiGraph(
                vertices      = rawJson["states"],
                edges         = edges,
                labels        = True,
                layout        = "kamada_kawai",
                vertex_config = vertex_config,
                edge_config   = edge_config
            )

            return cls(auto, mobj)

    @classmethod
    def from_mobj(cls, mobj):
        input_symbols = set()
        initial_state = None
        final_states = set()

        for (u, v) in mobj._edge_config:
            input_symbols.add(mobj._edge_config[(u, v)]["label"])

        for v in mobj.vertices:
            if "i" in mobj.flags[v]:
                initial_state = v
            
            if "f" in mobj.flags[v]:
                final_states.add(v)

        auto = DFA(
            states        = set(mobj.vertices),
            input_symbols = input_symbols,
            transitions   = cls._mobj_edges_to_auto_transitions(mobj.edges, mobj._edge_config),
            initial_state = initial_state,
            final_states  = final_states,
            allow_partial = True,
        )

        return cls(auto, mobj)

    @classmethod
    def from_dfa(cls, dfa):
        vertex_config = {v: {"flags": []} for v in dfa.states}

        vertex_config[dfa.initial_state]["flags"].append("i")

        for v in dfa.final_states:
            vertex_config[v]["flags"].append("f")

        edges, edge_config = cls._auto_transitions_to_mobj_edges(dfa.transitions)

        mobj = LabeledEdgeDiGraph(
            vertices = dfa.states,
            edges = edges,
            labels = True,
            layout = "kamada_kawai",
            vertex_config = vertex_config,
            edge_config = edge_config,
        )

        return cls(dfa, mobj)

    @staticmethod
    def _mobj_edges_to_auto_transitions(edges, edge_config):
        transitions = dict()
        for (start, end) in edges:
            if start not in transitions:
                transitions[start] = dict()

            symbol = edge_config[(start, end)]["label"]
            transitions[start][symbol] = end
        return transitions

    @staticmethod
    def _auto_transitions_to_mobj_edges(transitions):
        edges = list()
        edge_config = dict()

        for start in transitions:
            for symbol in transitions[start]:
                end = transitions[start][symbol]
                edges.append((start, end))

                if (start, end) not in edge_config:
                    edge_config[(start, end)] = dict()

                edge_config[(start, end)]["label"] = symbol
        return edges, edge_config

    @staticmethod
    def _json_to_mobj_edges(rawJson):
        print(rawJson)
        new_transitions = copy.deepcopy(rawJson["transitions"])
        edges = list()
        edge_config = dict()
        for start in new_transitions:
            for symbol in new_transitions[start]:
                end = new_transitions[start][symbol]

                edges.append((start, end))

                if (start, end) not in edge_config:
                    edge_config[(start, end)] = dict()
                edge_config[(start, end)]["label"] = symbol
        return edges, edge_config

    def next_state(self):
        pass
