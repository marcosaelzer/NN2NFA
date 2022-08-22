from nn2nfa.nn_model import generate_from_file, ToyNNetwork

# specify path to file containing simple neural network
nnet_filepath = "../assets/toy_nnet_example.txt"

# parse simple neural network as ToyNNetwork
nnet : ToyNNetwork = generate_from_file(nnet_filepath)

# print neural network
print(nnet)