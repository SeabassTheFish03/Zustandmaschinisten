# Finite State Machine with Input and Process Render (FSMIPR)
Creating a visualizer for Finite State Machines in Python using automata-lib and manim

Project Description: The visualizations of machines in the course notes are static. Therefore, any operations that we perform on them must be done sequentially, i.e., one operation at a time with a new figure each time. This project concerns creating a software library that will automatically generate videos for certain models and operations we encounter in CS474. You will be using the Python package Manim (https://www.manim.community/). This is a software package that, given Python code with specified animation function calls, will automatically generate a video. It supports many different shapes, graphs (in the math sense=vertices + edges), LaTeX, functions, and much more. This is the ideal tool to use for math visualization. 

Additionally, I would recommend that you use the Python package automata-lib (https://pypi.org/project/automata-lib/). It is a Python module that contains implementations of many of the basic computer models we use in CS474. For each, it also has methods to "step" through the computer's running on an input, one step at a time. However, this module is not visual.

Your project is essentially marrying Manim with automata-lib. The goal is to eventually turn this into a software product that will be in use in future CS474 offerings and potentially other venues.

## To set up on your own device:
This project is set up using a Conda environment, and the order of dependency install is
`conda install -c conda-forge manim`
`conda install conda-forge::miktex`
`pip install automata-lib`

The order is important because pip and Conda don't play well together. To use them together, Conda must be used first and pip must be used second.


## To run the code:
Run using python, run the main file, the json file with the formal definition of the DFA, and the input string to run through the DFA.
'py main.py <"file.json"> <"inputString">'















https://www.overleaf.com/project/65a7d2b18655642cac96a136
