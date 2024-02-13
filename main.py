from manim import *
from automata.fa.dfa import DFA
import sys
import json
import numpy as np

# Unit Vector and Angle Between from:
# https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
	v1_u = unit_vector(v1)
	v2_u = unit_vector(v2)
	return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

class DFAScene(Scene):
	def __init__(self, rawJson):
		super().__init__()
		self.dfa = JSONToDFA(rawJson)
		self.rawJson = rawJson

	def sift_self_transitions(self):
		self_transitions = []
		not_self_transitions = []

		for transition in self.rawJson["transitions"]:
			for destination in self.rawJson["transitions"][transition]:
				if self.rawJson["transitions"][transition][destination] == transition:
					self_transitions.append(tuple((transition, transition)))
				else:
					not_self_transitions.append(tuple((transition, self.rawJson["transitions"][transition][destination])))

		return self_transitions, not_self_transitions

	def construct(self):
		edge_config = {
            "stroke_width": 2,
            "tip_config": {
                "tip_length": 0.15,
            },
            (3, 4): {
                "color": RED,
                "tip_config": {"tip_length": 0.25, "tip_width": 0.25}
            },
        }

		vertices = self.rawJson["states"]
		loops, edges = self.sift_self_transitions()

		vertex_config = {
			"radius": 0.3,
			"stroke_color": "green",
			"fill_color": "white",
			"fill_opacity": 1
		}

		g = DiGraph(
			vertices,
			edges,
			#labels=True,
			label_fill_color=BLACK,
			layout="kamada_kawai",
			vertex_type=Circle,
			vertex_config=vertex_config
		)

		label = MathTex("A DFA")
		label.next_to(g, 2*DOWN)

		loop_arcs = VGroup()
		for loop in loops:
			node_pos = g[loop[0]].get_center()
			relative_pos = g.get_center() - node_pos

			between = angle_between(RIGHT, relative_pos)

			if between >= 0 and between < PI/2:
				offset = UP
			elif between >= PI/2 and between < PI:
				offset = LEFT
			elif between >= PI and between < 3*PI/2:
				offset = DOWN
			else:
				offset = RIGHT

			self_loop = CurvedArrow(
				start_point=relative_pos,
				end_point=relative_pos+offset,
				fill_color=WHITE,
				angle=4*PI/3,
				stroke_width=5,
			).scale(0.5)

			#self_loop.next_to(g[loop[0]], unit_vector(relative_pos)*1.2)
			loop_arcs.add(self_loop)

		self.play(Create(g))
		self.play(Create(label))
		self.play(Create(loop_arcs))
		self.wait()

# This function just makes the edge list for displaying the dfa. It loses the input character
def JSONtoManimEdges(rawJson): 
	edges = []
	for start in rawJson["transitions"]:
		for symbol in rawJson["transitions"][start]:
			newEdge = tuple((start, rawJson["transitions"][start][symbol]))
			edges.append(newEdge)
	return edges

def JSONToDFA(rawJson):
	return DFA(
		states = set(rawJson["states"]),
		input_symbols = rawJson["input_symbols"],
		transitions = rawJson["transitions"],
		initial_state = rawJson["initial_state"],
		final_states = set(rawJson["final_states"])
	)

def main():
	if len(sys.argv) == 3 or len(sys.argv) == 4:
		dfaFilename = sys.argv[1]
		inString = sys.argv[2]
		if len(sys.argv) == 4:
			picture_quality = sys.argv[3]
		else:
			picture_quality = "low_quality"
	else:
		print("Usage: py main.py <DFA.json> <input_string> [picture_quality (default low)]")
		exit()

	with open(dfaFilename, "r") as f:
		rawJson = json.loads(f.read())

	# TODO: Input validation. Ensure all things coming in from the json file are correctly typed and formatted
	# TODO: Error handling and prettifying.
	# 	Try to decipher what could go wrong with the DFA lib and translate to readable errors

	with tempconfig({"quality": picture_quality, "preview": True}):
		scene = DFAScene(rawJson)
		scene.render()

if __name__ == "__main__":
	main()