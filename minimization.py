from manim import *
from labeledEdgeDiGraph import LabeledEdgeDiGraph
from fa_manager import *

import json

class Minimize(Scene):
    def construct(self):
        with open("minimize2.json", "r") as f:
            rawJson = json.loads(f.read())

        dfa = DFA_Manager.from_json(rawJson, "ababb")

        # rows = list()
        # for state in rawJson["states"]:
        #     new_row = list()
        #     for state2 in rawJson["states"]:
        #         new_row.append(" ")
        #     rows.append(new_row)
        # table = Table(
        #     rows,
        #     col_labels = [Tex(x) for x in rawJson["states"]],
        #     row_labels = [Tex(x) for x in rawJson["states"]],
        #     top_left_entry = None,
        #     include_outer_lines=True
        # ).scale(0.6)
        #
        # self.play(Create(dfa.mobj.shift(RIGHT*3.5)), Create(table.shift(LEFT*3)))
        # self.wait(1)
        #
        # new_rows = list()
        # for i in range(len(rawJson["states"])):
        #     new_row = list()
        #     for j in range(len(rawJson["states"])):
        #         if j >= i:
        #             new_row.append("x")
        #         else:
        #             new_row.append(" ")
        #     new_rows.append(new_row)
        #
        # new_mobj = Table(
        #     new_rows,
        #     col_labels = [Tex(x) for x in rawJson["states"]],
        #     row_labels = [Tex(x) for x in rawJson["states"]],
        #     top_left_entry = None,
        #     include_outer_lines=True
        # ).scale(0.6).shift(LEFT*3)
        # 
        # self.play(ReplacementTransform(table, new_mobj))
        # self.wait(1)
        #
        # new_rows[4] = list("FF?Fxx")
        # new_rows[5] = list("????Fx")
        # mobj = Table(
        #     new_rows,
        #     col_labels = [Tex(x) for x in rawJson["states"]],
        #     row_labels = [Tex(x) for x in rawJson["states"]],
        #     top_left_entry = None,
        #     include_outer_lines=True
        # ).scale(0.6).shift(LEFT*3)
        #
        # self.play(ReplacementTransform(new_mobj, mobj))
        # self.wait(1)
        #
        # new_rows[1][0] = "?"
        # new_rows[2] = list("FFxxxx")
        # new_rows[3] = list("??Fxxx")
        # new_rows[5] = list("??F?Fx")
        #
        # new_mobj = Table(
        #     new_rows,
        #     col_labels = [Tex(x) for x in rawJson["states"]],
        #     row_labels = [Tex(x) for x in rawJson["states"]],
        #     top_left_entry = None,
        #     include_outer_lines=True
        # ).scale(0.6).shift(LEFT*3)
        #
        # self.play(ReplacementTransform(mobj, new_mobj))
        # self.wait(1)
        #
        # new_rows[1][0] = "F"
        # new_rows[3] = list("F?Fxxx")
        # new_rows[4] = list("FFFFxx")
        # new_rows[5] = list("FFF?Fx")
        #
        # mobj = Table(
        #     new_rows,
        #     col_labels = [Tex(x) for x in rawJson["states"]],
        #     row_labels = [Tex(x) for x in rawJson["states"]],
        #     top_left_entry = None,
        #     include_outer_lines=True
        # ).scale(0.6).shift(LEFT*3)
        #
        # self.play(ReplacementTransform(new_mobj, mobj))
        # self.wait(1)
        #
        # new_rows[3] = list("FFFxxx")
        # new_rows[5] = list("FFFFFx")
        #
        # new_mobj = Table(
        #     new_rows,
        #     col_labels = [Tex(x) for x in rawJson["states"]],
        #     row_labels = [Tex(x) for x in rawJson["states"]],
        #     top_left_entry = None,
        #     include_outer_lines=True
        # ).scale(0.6).shift(LEFT*3)
        #
        # self.play(ReplacementTransform(mobj, new_mobj))
        # self.wait(2)
        # self.clear()
        # self.play(Create(Text("The DFA was already minimized")))
        # self.wait()

        rows = list()
        for state in rawJson["states"]:
            new_row = list()
            for state2 in rawJson["states"]:
                new_row.append(" ")
            rows.append(new_row)
        table = Table(
            rows,
            col_labels = [Tex(x) for x in rawJson["states"]],
            row_labels = [Tex(x) for x in rawJson["states"]],
            top_left_entry = None,
            include_outer_lines=True
        ).scale(0.6)

        self.play(Create(dfa.mobj.shift(RIGHT*3.5)), Create(table.shift(LEFT*3)))
        self.wait(1)

        new_rows = list()
        for i in range(len(rawJson["states"])):
            new_row = list()
            for j in range(len(rawJson["states"])):
                if j >= i:
                    new_row.append("x")
                else:
                    new_row.append(" ")
            new_rows.append(new_row)

        new_mobj = Table(
            new_rows,
            col_labels = [Tex(x) for x in rawJson["states"]],
            row_labels = [Tex(x) for x in rawJson["states"]],
            top_left_entry = None,
            include_outer_lines=True
        ).scale(0.6).shift(LEFT*3)
        
        self.play(ReplacementTransform(table, new_mobj))
        self.wait(1)

        new_rows[2] = list("FFxxxx")
        new_rows[3] = list("??Fxxx")
        new_rows[5] = list("???F?x")
        mobj = Table(
            new_rows,
            col_labels = [Tex(x) for x in rawJson["states"]],
            row_labels = [Tex(x) for x in rawJson["states"]],
            top_left_entry = None,
            include_outer_lines=True
        ).scale(0.6).shift(LEFT*3)

        self.play(ReplacementTransform(new_mobj, mobj))
        self.wait(1)

        new_rows[4] = list("FF?Fxx")

        new_mobj = Table(
            new_rows,
            col_labels = [Tex(x) for x in rawJson["states"]],
            row_labels = [Tex(x) for x in rawJson["states"]],
            top_left_entry = None,
            include_outer_lines=True
        ).scale(0.6).shift(LEFT*3)

        self.play(ReplacementTransform(mobj, new_mobj))
        self.wait(1)

        new_rows[1][0] = "F"
        new_rows[3][0] = "F"
        new_rows[4][2] = "T"
        new_rows[5] = list("F?FTFx")

        mobj = Table(
            new_rows,
            col_labels = [Tex(x) for x in rawJson["states"]],
            row_labels = [Tex(x) for x in rawJson["states"]],
            top_left_entry = None,
            include_outer_lines=True
        ).scale(0.6).shift(LEFT*3)

        self.play(ReplacementTransform(new_mobj, mobj))
        self.wait(1)

        new_rows[3] = list("FTFxxx")
        new_rows[4] = list("FFTFxx")
        new_rows[5] = list("FTFTFx")

        new_mobj = Table(
            new_rows,
            col_labels = [Tex(x) for x in rawJson["states"]],
            row_labels = [Tex(x) for x in rawJson["states"]],
            top_left_entry = None,
            include_outer_lines=True
        ).scale(0.6).shift(LEFT*3)

        self.play(ReplacementTransform(mobj, new_mobj))
        self.wait(2)
        self.clear()
        new_dfa = DFA_Manager.from_dfa(dfa.auto.minify())
        self.play(Create(new_dfa.mobj))
        self.wait()
        self.play(Create(Text("The new, minimized DFA").shift(UP*3)))
        self.wait()

if __name__ == "__main__":
    with tempconfig({"quality": "high_quality", "preview": True}):
        scene = Minimize()
        scene.render()
