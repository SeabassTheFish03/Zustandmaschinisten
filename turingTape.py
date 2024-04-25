from manim import *

class TuringTape:
    def __init__(self, input_string):
        self.string = input_string
        self.index = 0
        self.boxes = VGroup()

        if self.string == "": self.string = "_"

    def get_mobject(self):
        out = VGroup()

        starter = MathTex(self.string[0])
        starter_box = SurroundingRectangle(starter, color="white")

        most_recent = VGroup(starter, starter_box)
        for char in self.string[1:]:
            out.add(most_recent)
            new_char = MathTex(str(char))
            new_box = SurroundingRectangle(new_char, color="white").set_height(most_recent.get_height())

            new_group = VGroup(new_char, new_box).next_to(most_recent, RIGHT, buff=0)
            most_recent = new_group
        out.add(most_recent)

        self.boxes = out
        self.boxes.add_updater(self.update_mobj)
        self.boxes.update()
        return self.boxes

    def update_mobj(self, ctx):
        for i in range(len(self.boxes)):
            if i == self.index:
                self.boxes[i].set_color("yellow")
            else:
                self.boxes[i].set_color("white")
