__all__ = {
    "LabeledEdgeDiGraph"
}

import numpy as np

from manim.mobject.graph import DiGraph
from manim.mobject.geometry.labeled import LabeledLine
from manim.mobject.mobject import override_animate
from manim.animation.creation import Create
from copy import copy, deepcopy

class LabeledEdgeDiGraph(DiGraph):
    def _populate_edge_dict(self, edges, edge_type):
        print("Populate Edge Dict")

        if edge_type.__name__ != "LabeledLine":
            raise Exception("Unsupported edge type: " + edge_type.__name__ + ". Must use LabeledLine")

        tmp_edge_conf = deepcopy(self._edge_config)

        self.edges = dict()
        for (u, v) in edges:
            if (v, u) in edges:
                vec1 = self[v].get_center() - self[u].get_center()
                vec2 = np.cross(vec1, np.array([0, 0, 1]))

                length = np.linalg.norm(vec2)
                offset = 0.1*vec2/length
            else:
                offset = np.array([0, 0, 0])

            self.edges[(u, v)] = edge_type(
                label = tmp_edge_conf[(u, v)].pop("label", "_populate_edge_dict fail"),
                start = self[u],
                end = self[v],
                z_index = -1,
                **tmp_edge_conf[(u, v)]
            ).shift(offset)

        for (u, v), edge in self.edges.items():
            edge.add_tip(**self._tip_config[(u, v)])

    def update_edges(self, graph):
        print("Update edge")
        tmp_edge_conf = deepcopy(self._edge_config)

        for (u, v), edge in graph.edges.items():
            if (v, u) in self.edges:
                vec1 = self[v].get_center() - self[u].get_center()
                vec2 = np.cross(vec1, np.array([0, 0, 1]))

                length = np.linalg.norm(vec2)
                offset = 0.1*vec2/length
            else:
                offset = np.array([0, 0, 0])

            edge_type = type(edge)
            tip = edge.pop_tips()[0]
            new_edge = edge_type(
                label = tmp_edge_conf[(u, v)].pop("label", "update_edges fail"),
                start = self[u],
                end = self[v],
                **tmp_edge_conf[(u, v)]
            ).shift(offset)
            edge.become(new_edge)
            edge.add_tip(tip)

    def __repr__(self):
        return f"Directed Graph with labeled edges with {len(self.vertices)} vertices and {len(self.edges)} edges"
