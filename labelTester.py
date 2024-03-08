from manim import *
from labeledEdgeDiGraph import LabeledEdgeDiGraph

class EdgeTester(Scene):
    def construct(self):
        vertices = ["q0", "q1"]
        edges = [("q0", "q1")]

        graph = LabeledEdgeDiGraph(
            vertices,
            edges,
            labels=True,
            label_fill_color=BLACK,
            layout="kamada_kawai",
            vertex_type=Dot,
            edge_type=LabeledLine,
            edge_config={
                ("q0", "q1"): {
                    "label": "a",
                    "color": "red",
                }
            }
        )

        self.play(Create(graph))
        self.wait()

if __name__ == "__main__":
    with tempconfig({"quality": "low_quality", "preview": True}):
        scene = EdgeTester()
        scene.render()



