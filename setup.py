import sys
import os
import re
import json

def main():
	# Number of arguments validation
	if len(sys.argv) == 3:
		filename = sys.argv[1]
		openMode = sys.argv[2]
	else:
		print("Usage: py setup.py <filename.json> <openMode>")
		exit()

	# Input validation
	if openMode not in ["new", "write", "append"]:
		print("Invalid openMode. Valid openModes are:")
		print("new: Creates a new file with the specified filename")
		print("write: Overwrites the contents of an existing file")
		#print("append: Appends data to content of an existing file") # not sure what to do about this one yet
		exit()

	# File existence validation
	if openMode != "new":
		if not os.path.isfile(filename):
			print("File not found: {filename}")
			exit()
	else:
		if os.path.isfile(filename):
			print("File already exists: {filename}")
			exit()

	# Gather the data, cleaning as we go
	rawStates = input("Enter state names in the form a, b, ...:\n")
	states = [x.strip() for x in rawStates.split(",")]

	rawSymbols = input("Enter transition symbols in the form 1, 2, ...:\n")
	symbols = [x.strip() for x in rawSymbols.split(",")]

	print("Now, you will enter the transitions for each state and symbol")
	transitions = dict()
	for state in states:
		transitions[state] = dict()

		for symbol in symbols:
			transition = ""
			while transition not in states:
				transition = input(f"State {state} with symbol {symbol} moves to: ")
			
			transitions[state][symbol] = transition

	initialState = ""
	while initialState not in states:
		initialState = input("Enter the intitial state: ")

	rawFinalStates = input("Enter the final states in the form a, b, ...:\n")
	finalStates = [x.strip() for x in rawFinalStates.split(",")]

	if len(eliminatedStates := set(finalStates) - set(states)) != 0:
		print(f"(States {eliminatedStates} not given as possible states and so were ignored)")
		finalStates = list(set(finalStates) - eliminatedStates)

	completeDFA = {
		"states": states,
		"input_symbols": symbols,
		"transitions": transitions,
		"initial_state": initialState,
		"final_states": finalStates
	}
	print("Your final DFA information:")
	print(json.dumps(completeDFA, indent=4))

	edit = ""
	while edit.lower() not in ["y","n"]:
		edit = input("Edit info? (y/n): ")

	if edit.lower() == "y":
		print("Too bad, I'm writing it in anyways HAHAHAHA")
	else:
		print("Writing file...")

	if openMode in ["new", "write"]:
		with open(filename, "w") as f:
			f.write(json.dumps(completeDFA))
	# Leaving this open-ended in case of future writing modes


if __name__ == "__main__":
	main()