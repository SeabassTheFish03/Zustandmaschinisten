# Zustandmaschinisten
Creating a visualizer for finite state machines in Python using automata-lib and manim

Project Description: The visualizations of machines in the course notes are static. Therefore, any operations that we perform on them must be done sequentially, i.e., one operation at a time with a new figure each time. This project concerns creating a software library that will automatically generate videos for certain models and operations we encounter in CS474. You will be using the Python package Manim (https://www.manim.community/). This is a software package that, given Python code with specified animation function calls, will automatically generate a video. It supports many different shapes, graphs (in the math sense=vertices + edges), LaTeX, functions, and much more. This is the ideal tool to use for math visualization. 

Additionally, I would recommend that you use the Python package automata-lib (https://pypi.org/project/automata-lib/). It is a Python module that contains implementations of many of the basic computer models we use in CS474. For each, it also has methods to "step" through the computer's running on an input, one step at a time. However, this module is not visual.

Your project is essentially marrying Manim with automata-lib. This project is more free-form than most, so feel free to take creative liberties as long as they are reasonable. The goal is to eventually turn this into a software product that will be in use in future CS474 offerings and potentially other venues. An existing (but wholly unfinished) library that you may use is manim-automata by SeanNelsonIO: https://github.com/SeanNelsonIO/manim-automata. *Note*: installing manim may be troublesome, so make sure to budget time to do that. There is a bit of a learning curve with using manim, so also budget time for that. 

Phase 1 Projects:
a. Create manim visualizations of a DFA. In other words, I should be able to input a DFA using automata-lib, and to have an animation that constructs the DFA one state at a time with transitions (in some specified order). This is harder than it seems; how to implement a directed graph (as manim only recently added them at my request), add transition labels, states and final states, etc. You will have to read over the documentation to find out how to modify the base representation of Manim objects. A starting implementation is in the manim-automata github repo.
b. Create manim visualizations of a DFA running on an input string. What should be present are four screens that operate at the same time: (1) the DFA itself with a box around the current state, (2) a zoomed-in version of what state we are in, (3) the current input string along with what position in the string we are in, and (4) the transition table that highlights what state and symbol is currently being accessed.



















https://www.overleaf.com/project/65a7d2b18655642cac96a136
