import Manim
from automata.fa.dfa import DFA
import sys
import json

def main():
	if sys.argc == 2:
		dfaFilename = sys.argv[1]
	else:
		println("Usage: py main.py <DFA.json>")
		exit()

	with open(dfaFilename, "r") as f:
		rawJson = json.loads(f.read())

	# TODO: Input validation. Ensure all things coming in from the json file are correctly typed and formatted

	dfa1 = DFA(
		states = rawJson["states"],
		input_symbols = rawJson["input_symbols"],
		transitions = rawJson["transitions"],
		initial_state = rawJson["initial_state"],
		final_states = set(rawJson["final_states"])
	)



if __name__ == "__main__":
	main()