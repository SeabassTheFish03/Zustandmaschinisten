import manim
from automata.fa.dfa import DFA
import sys
import json

def main():
	if len(sys.argv) == 3:
		dfaFilename = sys.argv[1]
	else:
		print("Usage: py main.py <DFA.json> <input_string>")
		exit()

	with open(dfaFilename, "r") as f:
		rawJson = json.loads(f.read())

	# TODO: Input validation. Ensure all things coming in from the json file are correctly typed and formatted
	# TODO: Create setup.py with ability to input DFA
	# TODO: Error handling and prettifying.
	# 	Try to decipher what could go wrong with the DFA lib and translate to readable errors

	dfa1 = DFA(
		states = set(rawJson["states"]),
		input_symbols = rawJson["input_symbols"],
		transitions = rawJson["transitions"],
		initial_state = rawJson["initial_state"],
		final_states = set(rawJson["final_states"])
	)

if __name__ == "__main__":
	main()