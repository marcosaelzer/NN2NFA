from typing import List

from nn2nfa.nn_model import generate_from_file, ToyNNetwork
from nn2nfa.out_reach_properties.out_reach_property import OutReachProperty, Inequality
from nn2nfa.utils import check_if_nn_and_out_reach_property_match
# specify path to file containing simple neural network

nnet_filepath = "../assets/toy_nnet_example.txt"

# parse simple neural network as ToyNNetwork
nnet : ToyNNetwork = generate_from_file(nnet_filepath)

# create output reachability property
input_specification: List[Inequality] = [Inequality([0.1,2.0, -3.0],0,True), Inequality([None,None,1.0],3.0,True)]
output_specification: List[Inequality] = [Inequality([None,None,1.0,None,5,None],0.0,False)]
out_reach_property: OutReachProperty = OutReachProperty(input_specification,output_specification)

# print neural network
print('Neural Network')
print(nnet)
print()

# print out_reach_property
print('Output Reachability Property')
print(out_reach_property)
print()

# check if property is well-defined for nnet
print(f"Neural Network and Property match: {check_if_nn_and_out_reach_property_match(nnet, out_reach_property)}")