# Translating DNN to Finite Automata

Proof-of-Concept implementation of the DNN to finite automata translation proposed in the paper 
*Verifying and Interpreting Neural Networks Using Finite Automata*. 

## Overview
This repository represents a proof-of-concept implementation for translating neural networks with
linear layers and ReLU activations into equivalent finite automata. 
In particular, this project offers a set of tools to translate
[Binarized Neural Networks](https://proceedings.neurips.cc/paper/2016/file/d8330f857a17c53d217014ee776bfd50-Paper.pdf)
(BNN) to Nondeterministic Finite Automata (NFA) capturing the input-output behaviour of the BNN over all integer 
inputs.

## Installation
Use the package manager pip to install the requirements using
```
pip install -r requirements.txt
```
The project assumes that Python 3.10 is used. After this you can use the project by starting any of the
skripts given in `.\skripts\ `. For further infos on these skripts read down below.

## Benchmarks

A simple example script explaining our neural network format `.toynnet` is found in 
`.\skripts\introductory_example.py`.

The benchmarks presented in the paper can be generated by the script TODO
