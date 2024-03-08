__all__ = {
    "LabeledEdgeDiGraph"
}

from manim.mobject.graph import DiGraph
from manim.mobject.geometry.labeled import LabeledLine
from manim.mobject.mobject import override_animate
from manim.animation.creation import Create
from copy import copy, deepcopy

class LabeledEdgeDiGraph(DiGraph):
    def _add_edge(self, edge, edge_type, edge_config):
        if edge_config is None:
            edge_config = self.default_edge_config.copy()

        if edge_type.__name__ != "LabeledLine":
            raise Exception("Unsupported edge type: " + edge_type.__name__ + ". Must use LabeledLine")

        added_mobjects = []
        for vertex in edge:
            if vertex not in self.vertices:
                added_mobjects.append(self._add_vertex(vertex))

        u, v = edge

        self._graph.add_edge(u, v)

        # Dict merge? Ripped straight from GenericGraph so idk
        base_edge_config = self.default_edge_config.copy()
        base_edge_config.update(edge_config)
        edge_config = base_edge_config
        self._edge_config[(u, v)] = edge_config.copy()

        edge_mobject = edge_type(
            label   = edge_config[(u, v)].pop("label", "_add_edge fail"),
            start   = self[u],
            end     = self[v],
            z_index = -1,
            **edge_config    
        )
        self.edges[(u, v)] = edge_mobject

        self.add(edge_mobject)
        added_mobjects.append(edge_mobject)
        return self.get_group_class()(*added_mobjects)

    def _populate_edge_dict(self, edges, edge_type):
        if edge_type.__name__ != "LabeledLine":
            raise Exception("Unsupported edge type: " + edge_type.__name__ + ". Must use LabeledLine")

        tmp_edge_conf = deepcopy(self._edge_config)

        self.edges = {
            (u, v): edge_type(
                label   = tmp_edge_conf[(u, v)].pop("label", "_populate_edge_dict fail"),
                start   = self[u],
                end     = self[v],
                z_index = -1,
                **tmp_edge_conf[(u, v)]
            )
            for (u, v) in edges
        }

        for (u, v), edge in self.edges.items():
            edge.add_tip(**self._tip_config[(u, v)])

    def update_edges(self, graph):
        tmp_edge_conf = deepcopy(self._edge_config)

        for (u, v), edge in graph.edges.items():
            edge_type = type(edge)
            tip = edge.pop_tips()[0]
            new_edge = edge_type(
                label = tmp_edge_conf[(u, v)].pop("label", "update_edges fail"),
                start = self[u],
                end = self[v],
                **tmp_edge_conf[(u, v)]
            )
            edge.become(new_edge)
            edge.add_tip(tip)

    def __repr__(self):
        return f"Directed Graph with labeled edges with {len(self.vertices)} vertices and {len(self.edges)} edges"
