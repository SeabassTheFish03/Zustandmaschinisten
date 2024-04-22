from fa_manager import *

import json
from manim import *

from turingTape import TuringTape

class TestScene(Scene):
    def construct(self):
        with open("fa_vault/simple.json", "r") as f:
            rawJson = json.loads(f.read())

        dfa = DFA_Manager.from_json(rawJson, "bac")
        nfa = NFA_Manager.from_dfa(dfa.auto, "bac")

        self.add(nfa.mobj)

        # while (nxt := nfa.peek()) is not None:
        #     self.play(nfa.mobj.transition_animation(nfa.current_state, nxt))
        #     nfa.next(nxt)
        #     self.wait(1)

        turing = TuringTape("bac")
        self.add(turing.get_mobject())
            

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        scene = TestScene()
        scene.render()
