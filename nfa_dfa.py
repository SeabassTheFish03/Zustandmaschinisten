import sys
import json

from manim import *
from labeledEdgeDiGraph import LabeledEdgeDiGraph
from utils import *

class NFA_DFA_Conversion(Scene):
    def __init__(self, rawJson):
        super().__init__()
        self.rawJson = rawJson

        self.nfa = JSONToNFA(rawJson)

        initial_edges, initial_edge_config = JSONtoManimEdges(rawJson)
        self.mobj = LabeledEdgeDiGraph(
            vertices = self.nfa.states,
            edges = initial_edges,
            labels = True,
            layout = "kamada_kawai",
            edge_config = initial_edge_config 
        ).shift(3*RIGHT)

        self.checklist = BulletedList(
            "Create NFA",
            "Remove epsilon transitions",
            "Remove nondeterminism",
            "Display final DFA",
            font_size = 44,
        ).shift(3*LEFT)

    def anim_init(self):
        return [Create(self.checklist), Create(self.mobj)]

    def anim_remove_ep(self):
        self.nfa = self.nfa.eliminate_lambda()
        new_edges, new_config = FAtoManimEdges(self.nfa)
        new_mobj = LabeledEdgeDiGraph(
            vertices = self.nfa.states,
            edges = new_edges,
            labels = True,
            layout = "kamada_kawai",
            edge_config = new_config 
        ).shift(3*RIGHT)

        return [Indicate(self.checklist[1]), FadeTransform(self.mobj, new_mobj)]

    def construct(self):
        self.play(*self.anim_init())
        self.play(Indicate(self.checklist[0]))
        self.wait(2)
        self.play(*self.anim_remove_ep())
        self.wait(2)

def main(args):
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        nfaFilename = sys.argv[1]
        if len(sys.argv) == 3:
            picture_quality = sys.argv[2]
        else:
            picture_quality = "low_quality"
    else:
        print("Usage: python main.py <NFA.json> [picture_quality (default low)]")
        exit(code=2)

    with open(nfaFilename, "r") as f:
        rawJson = json.loads(f.read())

    # TODO: Input validation. Ensure all things coming in from the json file are correctly typed and formatted
    # TODO: Error handling and prettifying.
    #   Try to decipher what could go wrong with the DFA lib and translate to readable errors

    with tempconfig({"quality": picture_quality, "preview": True}):
        scene = NFA_DFA_Conversion(rawJson)
        scene.render()

if __name__ == "__main__":
    main(sys.argv)
