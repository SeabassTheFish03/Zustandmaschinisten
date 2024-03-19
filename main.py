from manim import *
from labeledEdgeDiGraph import LabeledEdgeDiGraph
from utils import *
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from automata.base.exceptions import RejectionException
import sys
import json
import numpy as np
import queue

class DFAScene(Scene):
    def __init__(self, rawJson):
        super().__init__()
        self.dfa = JSONToDFA(rawJson)
        self.rawJson = rawJson

        self.vertices = self.rawJson["states"]
        self.edges = JSONtoManimEdges(self.rawJson)
        # self.loops, self.edges = self.sift_self_transitions()

        vertex_config = {
            "fill_opacity": 1,
            "fill_color": "white",
        }

        for vertex in self.vertices:
            vertex_config[vertex] = {"flags": []}
            if vertex in self.rawJson["final_states"]:
                vertex_config[vertex]["flags"].append("f")
            if vertex == self.rawJson["initial_state"]:
                vertex_config[vertex]["flags"].append("i")
        
        edge_conf = dict()
        for (u, v) in self.edges:
            if (u, v) not in edge_conf:
                edge_conf[(u, v)] = dict()
            transition_name = list(self.rawJson["transitions"][u].keys())[list(self.rawJson["transitions"][u].values()).index(v)]
            edge_conf[(u, v)]["label"] = transition_name

        # TODO: Figure out how to use CurvedArrow
        self.g = LabeledEdgeDiGraph(
            self.vertices,
            self.edges,
            labels=True,
            label_fill_color=BLACK,
            layout="kamada_kawai",
            vertex_type=Dot,
            #vertex_config=vertex_config,
            edge_type=LabeledLine,
            edge_config=edge_conf,
        )

        #TODO: Add start arrow
        #TODO: Add double circle final state

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
        self.play(Create(self.g), Create(self.loop_group))
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

class AnimateDFAWithTable(Scene):
    def __init__(self, rawJson, input_string):
        super().__init__()
        self.dfa = JSONToDFA(rawJson)
        self.input_string = input_string
        self.rawJson = rawJson

        self.fa_mobj = FAToMobj(self.dfa).shift(3*RIGHT)
        
        top_row = []
        for sym in self.rawJson["input_symbols"]:
            top_row.append(sym)

        state_rows = []
        for state in self.rawJson["states"]:
            new_row = []
            for sym in self.rawJson["input_symbols"]:
                new_row.append(self.rawJson["transitions"][state][sym])
            state_rows.append(new_row)

        self.table = MathTable(
            state_rows,
            col_labels = [MathTex(x) for x in top_row],
            row_labels = [MathTex(x) for x in self.rawJson["states"]],
            top_left_entry = None,
            include_outer_lines=True,
        ).shift(3*LEFT).scale(0.5)

        self.live_str_index = 0

    def construct(self):
        self.play(Create(self.fa_mobj), Create(self.table))

        previous_state = None
        prev_string = None
        prev_follower = None

        try:
            for new_state in self.dfa.read_input_stepwise(self.input_string, ignore_rejection=False):
                curr_string = Tex(self.input_string[self.live_str_index:], font_size=40, color="yellow").move_to(self.fa_mobj).shift(3*DOWN)

                trans_tup = (str(previous_state), str(new_state))
                
                tab_state_dex = list(self.rawJson["states"]).index(str(new_state)) + 2
                tab_trans_dex = list(self.rawJson["input_symbols"]).index(self.input_string[self.live_str_index]) + 2
                follower = self.table.get_cell((tab_state_dex, tab_trans_dex), color="yellow")

                if previous_state is None:
                    previous_state = new_state
                    prev_string = curr_string
                    prev_follower = follower
                    continue

                focus_edge = self.fa_mobj.edges[trans_tup]
                self.play(
                    ShowPassingFlash(focus_edge.copy().set_color("0x0000ff"), time_width=0.2),
                    ReplacementTransform(prev_string, curr_string),
                    ReplacementTransform(prev_follower, follower)
                )
                self.wait(0.5)

                previous_state = new_state
                prev_string = curr_string
                prev_follower = follower
                self.live_str_index += 1

        except RejectionException as e:
            reject_mobj = Text(str(e) + f"\nwith input string '{self.input_string}'", font_size=15, color="red").move_to(self.fa_mobj).shift(3*UP)
            self.play(Create(reject_mobj))
        else:
            accept_mobj = Tex(f"The DFA accepted the string '{self.input_string}'", font_size=24, color="green").move_to(self.fa_mobj).shift(3*UP)
            self.play(Create(accept_mobj))
        #
        # state_index = list(self.rawJson["states"]).index(self.rawJson["initial_state"]) + 2
        # trans_index = list(self.rawJson["input_symbols"]).index(self.input_string[0]) + 2
        # follower = self.table.get_cell((state_index, trans_index), color=YELLOW)
        # self.play(Create(follower))
        #
        # substring = self.input_string
        # floater = Tex(substring, color=BLACK, fill_color=YELLOW)
        # self.add(floater)
        #
        # current_state = self.rawJson["initial_state"]
        # next_state = self.rawJson["transitions"][current_state][self.input_string[0]]
        # for char in self.input_string:
        #     char = substring[0]
        #     substring = substring[1:]
        #
        #     if char in self.rawJson["transitions"][current_state]:
        #         next_state = self.rawJson["transitions"][current_state][char]
        #         
        #         if next_state != current_state:
        #             arrow = self.g.edges[(current_state, next_state)]
        #         else:
        #             arrow = self.loop_arcs[current_state]
        #         path = arrow.copy().set(color=RED, stroke_width=10)
        #
        #         state_index = list(self.rawJson["states"]).index(current_state) + 2
        #         trans_index = list(self.rawJson["input_symbols"]).index(char) + 2
        #
        #         new_follower = self.table.get_cell((state_index, trans_index), color=YELLOW)
        #
        #         self.play(
        #             Transform(follower, new_follower),
        #             Create(path),
        #             Transform(floater, Tex(str(substring), color=BLACK, fill_color=YELLOW)),
        #             MoveAlongPath(floater, path),
        #         )
        #         self.remove(path)
        #
        #         current_state = next_state
        #     else: break
        self.wait()

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
        scene = AnimateDFAWithTable(rawJson, inString)
        scene.render()

if __name__ == "__main__":
    main()
