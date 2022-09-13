# Translating DNN to Finite Automata

This repository represents the implementation of the verification procedure propesed in the paper 
*Verifying and Interpreting Neural Networks Using Finite Automata*.

## Overview
This repository represents a proof-of-concept implementation, including two core contributions: 
- **Part A**: It shows the feasability of a (slightly-optimized) translation from 
[Binarized Neural Networks](https://proceedings.neurips.cc/paper/2016/file/d8330f857a17c53d217014ee776bfd50-Paper.pdf)
(BNN) to Nondeterministic Finite Automata (NFA) capturing the input-output behaviour of the BNN over all integer 
inputs.
- **Part B**: It shows that the approach proposed in the paper can be used to verfiy Adversarial Robustness Properties 
(ARP) and Output Reachability Properties (ORP).

Both contributions are best-understood by running and investigating the example experiments (see Experiment A and
B below).

## Installation
Use the package manager pip to install the requirements using
```
pip install -r requirements.txt
```
The project assumes that Python 3.10 is used. After this you can use the project by starting any of the
skripts given in `.\skripts\ `. For further infos on these skripts read down below.

## Experiment A: Limits of the Translation from BNN to NFA

TODO

## Experiment B: Verifying ARP and ORP