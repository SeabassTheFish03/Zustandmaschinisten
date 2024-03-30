__all__ = {
    "LabeledEdgeDiGraph"
}

import numpy as np

from manim.mobject.graph import DiGraph
from manim.mobject.geometry.arc import CurvedArrow, Dot, Annulus
from manim.mobject.geometry.labeled import LabeledLine
from manim.mobject.geometry.line import Arrow
from manim.mobject.geometry.shape_matchers import BackgroundRectangle, SurroundingRectangle
from manim.mobject.mobject import override_animate
from manim.mobject.text.tex_mobject import MathTex
from manim.mobject.types.vectorized_mobject import VGroup, VDict

from copy import copy, deepcopy

from utils import *

class LabeledEdgeDiGraph(DiGraph):
    def __init__(
        self,
        vertices,
        edges,
        labels = dict(),
        label_fill_color = "black",
        layout = "kamada_kawai",
        layout_scale = 2,
        layout_config = None,
        vertex_type = Dot,
        vertex_config = None,
        vertex_mobjects = None,
        edge_type = LabeledLine,
        partitions = None,
        root_vertex = None,
        edge_config = None,
    ):

        if vertex_mobjects is None:
            vertex_mobjects = dict()
        else:
            self.common_vertex_config = dict()
            if vertex_config is not None:
                self.flags = {v: vertex_config[v].pop("flags") for v in vertex_config}

                for key, value in vertex_config.items():
                    if key not in vertices:
                        self.common_vertex_config[key] = value



        super().__init__(
            vertices,
            edges,
            labels,
            label_fill_color,
            layout,
            layout_scale,
            layout_config,
            vertex_type,
            vertex_config,
            vertex_mobjects,
            edge_type,
            partitions,
            root_vertex,
            edge_config,
        )
        self.layout_scale = layout_scale
        
        self.vertices = {v: VDict({"base": deepcopy(vertex), "accessories": VGroup()}) for (v, vertex) in enumerate(self.vertices)}
        print(self.vertices)

        self._redraw_vertices()

    def get_vcenter(self):
        return np.average(np.array([vertex["base"].get_center() for vertex in self.vertices.values()]), axis=0)

    def _populate_edge_dict(self, edges, edge_type):
        if edge_type.__name__ != "LabeledLine":
            raise TypeError("Unsupported edge type: " + edge_type.__name__ + ". Must use LabeledLine")

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
                    **tmp_edge_conf[(u, v)]
                ).shift(offset)
            else:
                edge_label = tmp_edge_conf[(u, u)].pop("label", "_populate_edge_dict fail")

                between = angle_between(self[u].get_center() - self.get_vcenter(), np.array([1, 0, 0]))

                loop = CurvedArrow(
                    start_point = self[u].get_top(),
                    end_point = self[u].get_bottom(),
                    angle = -4,
                    z_index = -1,
                    **tmp_edge_conf[(u, u)]
                )
                label_mobject = MathTex(
                    edge_label,
                    fill_color="white",
                    font_size=40,
                ).move_to(loop.get_center()).shift(np.array([0.5, 0, 0])).rotate(-1*between)

                label_background = BackgroundRectangle(
                    label_mobject,
                    buff=0.05,
                    color="black",
                    fill_opacity=1,
                    stroke_width=0.5,
                )
                label_frame = SurroundingRectangle(
                    label_mobject,
                    buff = 0.05,
                    color="white",
                    stroke_width=0.5
                )
                self.edges[(u, u)] = VGroup(loop, label_frame, label_background, label_mobject).rotate(between, about_point=self[u].get_center())

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
                    vec1 = self.vertices[v]["base"].get_center() - self.vertices[u]["base"].get_center()
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
                    start = self.vertices[u]["base"],
                    end = self.vertices[v]["base"],
                    **tmp_edge_conf[(u, v)]
                ).shift(offset)
                
                edge.become(new_edge)
                edge.add_tip(tip)
            else:
                edge_label = tmp_edge_conf[(u, u)].pop("label", "update_edges fail")

                between = angle_between(self.vertices[u]["base"].get_center() - self.get_vcenter(), np.array([1, 0, 0]))

                loop = CurvedArrow(
                    start_point = self.vertices[u]["base"].get_top(),
                    end_point = self.vertices[u]["base"].get_bottom(),
                    angle = -4,
                    z_index = -1,
                    **tmp_edge_conf[(u, u)]
                )
                label_mobject = MathTex(
                    edge_label,
                    fill_color="white",
                    font_size=40,
                ).move_to(loop.get_center()).shift(np.array([0.5, 0, 0])).rotate(-1*between)
                
                label_background = BackgroundRectangle(
                    label_mobject,
                    buff=0.05,
                    color="black",
                    fill_opacity=1,
                    stroke_width=0.5,
                ).rotate(-1*between)
                label_frame = SurroundingRectangle(
                    label_mobject,
                    buff = 0.05,
                    color="white",
                    stroke_width=0.5
                ).rotate(-1*between)
                edge.become(VGroup(loop, label_frame, label_background, label_mobject).rotate(between, about_point=self.vertices[u]["base"].get_center()))

    def _redraw_vertices(self):
        for v in self.vertices:
            if "f" in self.flags[v]:
                ring = Annulus(
                    inner_radius = self.vertices[v]["base"].width + 0.1,
                    outer_radius = self.vertices[v]["base"].width + 0.2,
                    z_index = -1,
                    fill_color="white"
                ).move_to(self.vertices[v]["base"].get_center()).scale(1/self.layout_scale)

                self.vertices[v]["accessories"].add(ring)

            if "i" in self.flags[v]:
                ray = self.vertices[v].get_center() - self.get_vcenter()
                start_arrow = Arrow(
                    start=ray*2,
                    end=ray*1.05,
                    fill_color="white",
                    stroke_width=20
                )
                self.vertices[v]["accessories"].add(start_arrow)

            if "c" in self.flags[v]:
                self.vertices[v]["base"].set_color("yellow")

    def add_flag(self, state, flag):
        if state in self.vertices:
            self.flags[state].append(flag)
        self._redraw_vertices()

    def remove_flag(self, state, flag):
        if state in self.vertices:
            if flag in self.flags[state]:
                self.flags[state].remove(flag)
        self._redraw_vertices()


    def __repr__(self):
        return f"Directed Graph with labeled edges with {len(self.vertices)} vertices and {len(self.edges)} edges"
