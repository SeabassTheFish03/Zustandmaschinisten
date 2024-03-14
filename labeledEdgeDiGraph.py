__all__ = {
    "LabeledEdgeDiGraph"
}

import numpy as np

from manim.mobject.graph import DiGraph
from manim.mobject.geometry.labeled import LabeledLine
from manim.mobject.geometry.arc import CurvedArrow, Dot, Annulus
from manim.mobject.text.tex_mobject import MathTex
from manim.mobject.types.vectorized_mobject import VGroup
from copy import copy, deepcopy

class LabeledEdgeDiGraph(DiGraph):
    def _create_vertex(
        self,
        vertex,
        position = None,
        label = False,
        label_fill_color = "black",
        vertex_type = Dot,
        vertex_config = None,
        vertex_mobject= None,
    ):
        vert, pos, v_conf, v_mobj = super()._create_vertex(
            vertex,
            position,
            label,
            label_fill_color,
            vertex_type,
            vertex_config,
            vertex_mobject,
        )

        flags = v_conf.pop("flags")
        if "f" in flags:
            v_mobj = VGroup(v_mobj,
                Annulus(
                    inner_radius = 2.1,
                    outer_radius = 2.2,
                    z_index = -1,
                    fill_color="yellow"
                ).move_to(v_mobj)
            )
        return vert, pos, v_conf, v_mobj
    def _populate_edge_dict(self, edges, edge_type):
        if edge_type.__name__ != "LabeledLine":
            raise Exception("Unsupported edge type: " + edge_type.__name__ + ". Must use LabeledLine")

        tmp_edge_conf = deepcopy(self._edge_config)

        self.edges = dict()
        for (u, v) in edges:
            if u != v:
                if (v, u) in edges:
                    vec1 = self[v].get_center() - self[u].get_center()
                    vec2 = np.cross(vec1, np.array([0, 0, 1]))

                    length = np.linalg.norm(vec2)
                    offset = 0.1*vec2/length
                else:
                    offset = np.array([0, 0, 0])

                edge_label = tmp_edge_conf[(u, v)].pop("label", "_populate_edge_dict fail") 
                if edge_label == "":
                    edge_label = "\\epsilon"
                self.edges[(u, v)] = edge_type(
                    label = edge_label,
                    start = self[u],
                    end = self[v],
                    z_index = -1,
                    **tmp_edge_conf[(u, v)]
                ).shift(offset)
            else:
                edge_label = tmp_edge_conf[(u, u)].pop("label", "_populate_edge_dict fail")
                loop = CurvedArrow(
                    start_point = self[u].get_top(),
                    end_point = self[u].get_bottom(),
                    radius = self[u].height*3,
                    z_index = -1,
                    **tmp_edge_conf[(u, u)]
                )
                label_mobject = MathTex(
                    edge_label
                ).move_to(loop)
                self.edges[(u, u)] = VGroup(loop, label_mobject)

        for (u, v), edge in self.edges.items():
            try:
                if isinstance(edge, LabeledLine):
                    edge.add_tip(**self._tip_config[(u, v)])
            except TypeError:
                print(self._tip_config)
                exit()

    def update_edges(self, graph):
        tmp_edge_conf = deepcopy(self._edge_config)

        for (u, v), edge in graph.edges.items():
            if u != v:
                # Handling arrows going both ways
                if (v, u) in self.edges:
                    vec1 = self[v].get_center() - self[u].get_center()
                    vec2 = np.cross(vec1, np.array([0, 0, 1]))

                    length = np.linalg.norm(vec2)
                    offset = 0.1*vec2/length
                else:
                    offset = np.array([0, 0, 0])

                # Housekeeping
                edge_type = type(edge)
                tip = edge.pop_tips()[0]
                edge_label = tmp_edge_conf[(u, v)].pop("label", "update_edges fail") 
                if edge_label == "":
                    edge_label = "\\epsilon" # Little hack because I know this is going to become a TeX string
                
                new_edge = edge_type(
                    label = edge_label,
                    start = self[u],
                    end = self[v],
                    **tmp_edge_conf[(u, v)]
                ).shift(offset)
                
                edge.become(new_edge)
                edge.add_tip(tip)
            else:
                edge_label = tmp_edge_conf[(u, u)].pop("label", "update_edges fail")
                
                loop = CurvedArrow(
                    start_point = self[u].get_top(),
                    end_point = self[u].get_bottom(),
                    angle = 4,
                    z_index = 1,
                    **tmp_edge_conf[(u, u)]
                )
                label_mobject = MathTex(
                    edge_label
                ).move_to(loop.get_right())
                edge.become(VGroup(loop, label_mobject))

    def __repr__(self):
        return f"Directed Graph with labeled edges with {len(self.vertices)} vertices and {len(self.edges)} edges"
