from manim import *
from labeledEdgeDiGraph import LabeledEdgeDiGraph
from automata.fa.dfa import DFA
import sys
import json
import numpy as np
import queue

# Unit Vector and Angle Between from:
# https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

class DFAScene(Scene):
    def __init__(self, rawJson):
        super().__init__()
        self.dfa = JSONToDFA(rawJson)
        self.rawJson = rawJson

        self.vertices = self.rawJson["states"]
        self.loops, self.edges = self.sift_self_transitions()

        vertex_config = {
            "fill_opacity": 1
        }
        for vertex in self.vertices:
            if self.rawJson["initial_state"] == vertex:
                if vertex in self.rawJson["final_states"]:
                    fill_color = "yellow"
                else:
                    fill_color = "green"
            elif vertex in self.rawJson["final_states"]:
                fill_color = "red"
            else:
                fill_color = "white"
            vertex_config[vertex] = {"fill_color": fill_color}
        
        edge_config = dict()
        for (u, v) in self.edges:
            if (u, v) not in edge_config:
                edge_config[(u, v)] = dict()
            transition_name = list(self.rawJson["transitions"][u].keys())[list(self.rawJson["transitions"][u].values()).index(v)]
            edge_config[(u, v)]["label"] = transition_name

        # TODO: Figure out how to use CurvedArrow
        self.g = LabeledEdgeDiGraph(
            self.vertices,
            self.edges,
            labels=True,
            label_fill_color=BLACK,
            layout="kamada_kawai",
            vertex_type=Dot,
            vertex_config=vertex_config,
            edge_config=edge_config,
            edge_type=LabeledLine,
        )

        self.loop_arcs = dict()
        loop_arcs = VGroup()
        for loop in self.loops:
            node = self.g[loop[0]]

            relative_pos = self.g.get_center() - node.get_center()

            between = angle_between(RIGHT, relative_pos)
            mult = 1

            if between < PI/4:
                offset = UP
                start = node.get_bottom()
                end = node.get_top()
            elif between >= PI/4 and between < 3*PI/4:
                if relative_pos[1] > 0:
                    start = node.get_left()
                    end = node.get_right()
                else:
                    start = node.get_right()
                    end = node.get_left()
                mult = -1
            elif between >= 3*PI/4:
                start = node.get_top()
                end = node.get_bottom()

            self_loop = CurvedArrow(
                start_point=start,
                end_point=end,
                fill_color=WHITE,
                angle=-4*PI/3*mult,
                stroke_width=5
            ).scale(0.7)

            self_loop.move_to(node.get_center())
            self_loop.shift(unit_vector(node.get_center())*0.4)
            self.loop_arcs[loop[0]] = self_loop

        self.loop_group = VGroup()
        self.loop_group.add(*self.loop_arcs.values())
        self.g.add(self.loop_group)

    def sift_self_transitions(self):
        self_transitions = []
        not_self_transitions = []

        for transition in self.rawJson["transitions"]:
            for destination in self.rawJson["transitions"][transition]:
                if self.rawJson["transitions"][transition][destination] == transition:
                    self_transitions.append(tuple((transition, transition)))
                else:
                    not_self_transitions.append(tuple((transition, self.rawJson["transitions"][transition][destination])))

        return self_transitions, not_self_transitions

    def construct(self):
        # TODO: Figure out how to make it with labels (will need a subclass)
        self.play(Create(self.g))
        self.wait()

class WatchItHappen(DFAScene):
    def __init__(self, rawJson, input_string):
        super().__init__(rawJson)
        self.input_string = input_string

    def construct(self):
        super().construct()
        sequence = []
        current_state = self.rawJson["initial_state"]
        for char in self.input_string:
            if char in self.rawJson["transitions"][current_state]:
                next_state = self.rawJson["transitions"][current_state][char]

                if next_state != current_state:
                    sequence.append(self.g.edges[(current_state, next_state)])
                else:
                    sequence.append(self.loop_arcs[current_state])

                current_state = next_state
            else: break

        to_show = [arrow.copy().set(color=RED, stroke_width=10) for arrow in sequence]

        substring = self.input_string
        floater = Tex(substring, color=BLACK, fill_color=YELLOW)

        for arrow in to_show:
            char = substring[0]
            substring = substring[1:]
            self.play(
                Create(arrow),
                Transform(floater, Tex(str(substring), color=BLACK, fill_color=YELLOW)),
                MoveAlongPath(floater, arrow),
                rate_func=linear,
                running_time=1
            )
            self.remove(arrow)

        self.wait()

class DisplayTransitionTable(Scene):
    def __init__(self, rawJson, input_string=""):
        super().__init__()
        self.rawJson = rawJson
        self.input_string = input_string

        top_row = []
        for sym in self.rawJson["input_symbols"]:
            top_row.append(sym)

        state_rows = []
        for state in self.rawJson["states"]:
            new_row = []
            for sym in self.rawJson["input_symbols"]:
                new_row.append(self.rawJson["transitions"][state][sym])
            state_rows.append(new_row)

        self.table = Table(
            state_rows,
            col_labels = [Tex(x) for x in top_row],
            row_labels = [Tex(x) for x in self.rawJson["states"]],
            top_left_entry = None,
            include_outer_lines=True,
        )

    def construct(self):
        self.add(self.table)

class AnimateTransitionTable(DisplayTransitionTable):
    def construct(self):
        sequence = []
        current_state = self.rawJson["initial_state"]
        for char in self.input_string:
            if char in self.rawJson["transitions"][current_state]:
                next_state = self.rawJson["transitions"][current_state][char]

                sequence.append((current_state, next_state))

                current_state = next_state
            else: break

        self.play(Create(self.table))

        state_index = list(self.rawJson["states"]).index(self.rawJson["initial_state"]) + 2
        trans_index = list(self.rawJson["input_symbols"]).index(self.input_string[0]) + 2
        follower = self.table.get_cell((state_index, trans_index), color=YELLOW)
        self.play(Create(follower))

        substring = self.input_string
        floater = Tex(substring, color=BLACK, fill_color=YELLOW)
        self.add(floater)

        current_state = self.rawJson["initial_state"]
        next_state = self.rawJson["transitions"][current_state][self.input_string[0]]
        for char in self.input_string:
            char = substring[0]
            substring = substring[1:]

            if char in self.rawJson["transitions"][current_state]:
                if next_state != current_state:
                    arrow = self.g.edges[(current_state, next_state)]
                else:
                    arrow = self.loop_arcs[current_state]
                path = arrow.copy().set(color=RED, stroke_width=10)

                state_index = list(self.rawJson["states"]).index(current_state) + 2
                trans_index = list(self.rawJson["input_symbols"]).index(char) + 2

                new_follower = self.table.get_cell((state_index, trans_index), color=YELLOW)
                next_state = self.rawJson["transitions"][current_state][char]

                self.play(
                    Transform(follower, new_follower),
                    Create(path),
                    Transform(floater, Tex(str(substring), color=BLACK, fill_color=YELLOW)),
                    MoveAlongPath(floater, path),
                )
                self.remove(path)
                current_state = next_state
            else: break

        self.wait()

class AnimateDFAWithTable(WatchItHappen):
    def __init__(self, rawJson, input_string):
        super().__init__(rawJson, input_string)
        self.input_string = input_string

        top_row = []
        for sym in self.rawJson["input_symbols"]:
            top_row.append(sym)

        state_rows = []
        for state in self.rawJson["states"]:
            new_row = []
            for sym in self.rawJson["input_symbols"]:
                new_row.append(self.rawJson["transitions"][state][sym])
            state_rows.append(new_row)

        self.table = Table(
            state_rows,
            col_labels = [Tex(x) for x in top_row],
            row_labels = [Tex(x) for x in self.rawJson["states"]],
            top_left_entry = None,
            include_outer_lines=True,
        )

    def construct(self):
        self.g.shift(RIGHT)
        self.table.shift(3*LEFT).scale(0.5)

        self.play(Create(self.g), Create(self.table))

        state_index = list(self.rawJson["states"]).index(self.rawJson["initial_state"]) + 2
        trans_index = list(self.rawJson["input_symbols"]).index(self.input_string[0]) + 2
        follower = self.table.get_cell((state_index, trans_index), color=YELLOW)
        self.play(Create(follower))

        substring = self.input_string
        floater = Tex(substring, color=BLACK, fill_color=YELLOW)
        self.add(floater)

        current_state = self.rawJson["initial_state"]
        next_state = self.rawJson["transitions"][current_state][self.input_string[0]]
        for char in self.input_string:
            char = substring[0]
            substring = substring[1:]

            if char in self.rawJson["transitions"][current_state]:
                next_state = self.rawJson["transitions"][current_state][char]
                
                if next_state != current_state:
                    arrow = self.g.edges[(current_state, next_state)]
                else:
                    arrow = self.loop_arcs[current_state]
                path = arrow.copy().set(color=RED, stroke_width=10)

                state_index = list(self.rawJson["states"]).index(current_state) + 2
                trans_index = list(self.rawJson["input_symbols"]).index(char) + 2

                new_follower = self.table.get_cell((state_index, trans_index), color=YELLOW)

                self.play(
                    Transform(follower, new_follower),
                    Create(path),
                    Transform(floater, Tex(str(substring), color=BLACK, fill_color=YELLOW)),
                    MoveAlongPath(floater, path),
                )
                self.remove(path)

                current_state = next_state
            else: break

        self.wait()


# This function just makes the edge list for displaying the dfa. It loses the input character
def JSONtoManimEdges(rawJson): 
    edges = []
    for start in rawJson["transitions"]:
        for symbol in rawJson["transitions"][start]:
            newEdge = tuple((start, rawJson["transitions"][start][symbol]))
            edges.append(newEdge)
    return edges

def JSONToDFA(rawJson):
    return DFA(
        states = set(rawJson["states"]),
        input_symbols = rawJson["input_symbols"],
        transitions = rawJson["transitions"],
        initial_state = rawJson["initial_state"],
        final_states = set(rawJson["final_states"])
    )

def main():
    if len(sys.argv) == 3 or len(sys.argv) == 4:
        dfaFilename = sys.argv[1]
        inString = sys.argv[2]
        if len(sys.argv) == 4:
            picture_quality = sys.argv[3]
        else:
            picture_quality = "low_quality"
    else:
        print("Usage: py main.py <DFA.json> <input_string> [picture_quality (default low)]")
        exit()

    with open(dfaFilename, "r") as f:
        rawJson = json.loads(f.read())

    # TODO: Input validation. Ensure all things coming in from the json file are correctly typed and formatted
    # TODO: Error handling and prettifying.
    #   Try to decipher what could go wrong with the DFA lib and translate to readable errors

    with tempconfig({"quality": picture_quality, "preview": True}):
        scene = DFAScene(rawJson)
        scene.render()

if __name__ == "__main__":
    main()
