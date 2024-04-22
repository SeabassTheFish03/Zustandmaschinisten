from manim import *

class TuringTape:
    def __init__(self, input_string):
        self.string = input_string

    def get_mobject(self):
        out = VGroup()

        starter = MathTex(self.string[0])
        starter_box = SurroundingRectangle(starter, color="white", buff=MED_LARGE_BUFF)

        most_recent = VGroup(starter, starter_box)
        for char in self.string[1:]:
            out.add(most_recent)
            new_char = MathTex(str(char))
            new_box = SurroundingRectangle(new_char, color="white", buff=MED_LARGE_BUFF).set_height(most_recent.get_height())

            new_group = VGroup(new_char, new_box).next_to(most_recent, RIGHT, buff=0)
            most_recent = new_group
        out.add(most_recent)

        return out
