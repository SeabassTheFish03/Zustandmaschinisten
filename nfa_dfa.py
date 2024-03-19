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

        self.mobj = FAToMobj(self.nfa).shift(3*RIGHT)

        self.checklist = BulletedList(
            "Create NFA",
            "Remove $\\epsilon$ transitions",
            "Remove nondeterminism",
            "Minify",
            font_size = 44,
        ).shift(3*LEFT)

    def anim_init(self):
        return [Create(self.checklist), Create(self.mobj)]

    def anim_remove_ep(self):
        self.nfa = self.nfa.eliminate_lambda()
        new_mobj = FAToMobj(self.nfa).shift(3*RIGHT)

        anims = [Indicate(self.checklist[1]), FadeTransform(self.mobj, new_mobj)]
        self.mobj = new_mobj
        
        return anims

    def anim_remove_ambig(self):
        self.nfa = DFA.from_nfa(self.nfa, minify=False)
        new_transitions = {
            "q" + str(start): {
                symbol: "q" + str(self.nfa.transitions[start][symbol]) for symbol in self.nfa.transitions[start]
            } for start in self.nfa.transitions
        }
        self.nfa = DFA(
            states = set(["q" + str(state) for state in self.nfa.states]),
            input_symbols=set(self.nfa.input_symbols),
            transitions=new_transitions,
            initial_state="q" + str(self.nfa.initial_state),
            final_states = set(["q" + str(state) for state in self.nfa.final_states]),
            allow_partial=True
        )
        new_mobj = FAToMobj(self.nfa).shift(3*RIGHT)

        anims = [Indicate(self.checklist[2]), FadeTransform(self.mobj, new_mobj)]
        self.mobj = new_mobj

        return anims

    def anim_minify(self):
        self.nfa = self.nfa.minify()
        new_transitions = {
            "q" + str(start): {
                symbol: "q" + str(self.nfa.transitions[start][symbol]) for symbol in self.nfa.transitions[start]
            } for start in self.nfa.transitions
        }
        self.nfa = DFA(
            states = set(["q" + str(state) for state in self.nfa.states]),
            input_symbols=set(self.nfa.input_symbols),
            transitions=new_transitions,
            initial_state="q" + str(self.nfa.initial_state),
            final_states = set(["q" + str(state) for state in self.nfa.final_states]),
            allow_partial=True
        )
        new_mobj = FAToMobj(self.nfa).shift(3*RIGHT)

        anims = [Indicate(self.checklist[3]), FadeTransform(self.mobj, new_mobj)]
        self.mobj = new_mobj

        return anims

    def construct(self):
        self.play(*self.anim_init())
        self.play(Indicate(self.checklist[0]))
        self.wait(2)
        self.play(*self.anim_remove_ep())
        self.wait(2)
        self.play(*self.anim_remove_ambig())
        self.wait(2)
        self.play(*self.anim_minify())
        self.wait(2)

def main(args):
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        nfaFilename = sys.argv[1]
        if len(sys.argv) == 3:
            picture_quality = sys.argv[2]
        else:
            picture_quality = "low_quality"
    else:
        print("Usage: python nfa_dfa.py <NFA.json> [picture_quality (default low)]")
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
