from manim import *
from automata.fa.dfa import DFA
import sys
import json

class DFAScene(Scene):
	def __init__(self, rawJson):
		super().__init__()
		self.dfa = JSONToDFA(rawJson)
		self.rawJson = rawJson

	def construct(self):
		edge_config = {
            "stroke_width": 2,
            "tip_config": {
                "tip_shape": ArrowSquareTip,
                "tip_length": 0.15,
            },
            (3, 4): {
                "color": RED,
                "tip_config": {"tip_length": 0.25, "tip_width": 0.25}
            },
        }

		vertices = self.rawJson["states"]
		edges = JSONtoManimEdges(self.rawJson)
		vertex_config = {
			"radius": 0.3,
			"stroke_color": "green",
			"fill_color": "white",
			"fill_opacity": 1
		}

		g = DiGraph(
			vertices,
			edges,
			labels=False,
			layout="kamada_kawai",
			edge_config=edge_config,
			vertex_type=Circle,
			vertex_config=vertex_config
		).scale(1.4)

		self.play(Create(g))
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