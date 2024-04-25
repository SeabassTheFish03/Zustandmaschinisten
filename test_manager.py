from fa_manager import *

import json
from manim import *

from turingTape import TuringTape
from automata.base.exceptions import RejectionException

class TestScene(Scene):
    def construct(self):
        with open("fa_vault/simple.json", "r") as f:
            rawJson = json.loads(f.read())

        # dfa = DFA_Manager.from_json(rawJson, "bac")
        # nfa = NFA_Manager.from_dfa(dfa.auto, "bac")

        # self.add(nfa.mobj)

        # while (nxt := nfa.peek()) is not None:
        #     self.play(nfa.mobj.transition_animation(nfa.current_state, nxt))
        #     nfa.next(nxt)
        #     self.wait(1)

        with open("turing.json", "r") as f:
            turing = TM_Manager.from_json(f.read(), "000111")
        self.add(turing.mobj)
        try:
            for animation in turing.animate():
                self.play(animation)
                self.wait(0.5)
        except RejectionException as e:
            self.wait(2)
            self.clear()
            self.play(Create(Text("Input Rejected")))
            self.wait(2)
            

if __name__ == "__main__":
    with tempconfig({"quality": "high_quality", "preview": True}):
        scene = TestScene()
        scene.render()
