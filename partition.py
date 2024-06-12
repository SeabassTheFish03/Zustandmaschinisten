from manim import *

import json

def json_to_edges(rawJson):
    edges = list()
    for k in rawJson["edges"]:
        v = rawJson["edges"][k]
        for end in v:
            edges.append((k, end))

    return edges

class ShowGraph(Scene):
    def construct(self):
        self.camera.background_color = "white"

        with open("np-complete.json", "r") as f:
            rawJson = json.loads(f.read())
            
        g = Graph(
            vertices=rawJson["vertices"],
            edges=set(json_to_edges(rawJson)),
            layout="kamada_kawai",
            label_fill_color="black",
            labels=True,
            layout_scale=4,
            vertex_config={
                "stroke_width":2,
                "stroke_color":"black",
                "radius": 0.35,
            },
            edge_config={
                "stroke_color": "black",
                "stroke_width": 2,
            }
        )

        self.add(g.shift(DOWN/2))


if __name__ == "__main__":
    with tempconfig({"quality": "high_quality", "preview": True}):
        scene = ShowGraph()
        scene.render()
