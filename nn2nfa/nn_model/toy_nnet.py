"""Toy Neural Network Module

This module offers a class for toy-like neural networks (ToyNNet). It is designed to handle small neural networks
using relu and identity activations.
It also offers the possibility to read-in toynnets from a *.txt file. The parsing is implemented using ANTLRv4.

"""
from antlr4 import *
from .parser.ToyNNetLexer import ToyNNetLexer
from .parser.ToyNNetParser import ToyNNetParser
from .parser.ToyNNetListener import ToyNNetListener

import numpy as np


class _ToyNNetGenerator(ToyNNetListener):
    """ Generator to read in toy neural networks from *.txt

        Inherits from ToyNNetListener class to traverse syntax tree of the parsed
        *.txt file. For an example of such file see 'assets\toy_nnetwork_example.txt'.
        The method 'enterX' is called when a node X is entered respectively 'exitX' is
        called when a node X is exited. The grammar for this parser can be found in 'ToyNNet.g4'.

        Attributes:
            network_input_size (int): Input dimension of the generated network.
            network_weights (list of (list of (list of float))): Weights of the generated network.
            network_bias (list of (list of float): Bias of the generated network.
            network_activations (list of (list of string)): Activation functions of the generated network
    """

    def __init__(self):
        # initialize attributes
        self.network_input_size = 0
        self.network_weights = []
        self.network_bias = []
        self.network_activations = []

        # initialize private attributes (used for error handling)
        self._previous_layer_size = 0
        self._layer_count = 0
        self._node_count = 0

    def exitNnet_input(self, ctx):
        # remember specified input size of the neural network
        self.network_input_size = int(ctx.NUMBER().getText())
        # set input size as layer 0 size
        self._previous_layer_size = self.network_input_size

    def enterLayer(self, ctx: ToyNNetParser.LayerContext):
        # add empty lists to attiributes to add new layer
        self.network_weights.append([])
        self.network_bias.append([])
        self.network_activations.append([])
        self._layer_count = self._layer_count + 1

    def enterNeuron(self, ctx: ToyNNetParser.NeuronContext):
        # increase node count by one (for adressing the right node in error handling)
        self._node_count = self._node_count + 1

    def exitNeuron(self, ctx: ToyNNetParser.NeuronContext):
        # remember all weights of current neuron
        neuron_weights_list = []
        for weight in ctx.weights().NUMBER():
            # for each weight of the currently considered neuron
            neuron_weights_list.append(float(weight.getText()))

        # check for missmatch in weight size
        if self._previous_layer_size != len(neuron_weights_list):
            # if the amount of weights of this neuron does not fit the output size of previous layer
            raise ValueError('The number of weights in node ' + str(self._node_count)
                             + ' of layer ' + str(self._layer_count) + ' is not correct. It has '
                             + str(len(neuron_weights_list)) + ' weights but ' + (str(self._previous_layer_size))
                             + ' are expected.')

        # append weights, bias and activation to current layer
        self.network_weights[-1].append(neuron_weights_list)
        self.network_bias[-1].append(float(ctx.NUMBER().getText()))
        self.network_activations[-1].append(ctx.activation().getText())

    def exitLayer(self, ctx: ToyNNetParser.LayerContext):
        # remember layer size for error handling
        self._previous_layer_size = len(self.network_weights[-1])
        # reset node count
        self._node_count = 0


class ToyNNetwork:
    """ Represents a simple but fully specified neural network.

    The purpose of this class is representing rather small neural networks for structural
    investigations or testing purposes. Typically, an object of this class should be generated
    using the 'generate_from_file' method specified below.

    Attributes:
         input_size (int): Input dimension of the network.
         weights (list of (list of (list of float))): Weights of the network.
         bias (list of (list of float): Bias of the network.
         activations (list of (list of string)): Activation functions of the network
         output_size (int): Output dimension of the network.
    """

    def __init__(self, input_size, weights, bias, activations):
        self.input_size = input_size
        self.weights = weights
        self.bias = bias
        self.activations = activations
        self.output_size = len(weights[-1])

    def compute_layer_output(self, input, layer):
        """ Computes the networks output for given input.

        Args:
            input (list of float): list of inputs, size must equal self.input_size.
            layer (int): number of layer to get output from.

        Returns:
            Output as a list of floats

        """

        # check if input has correct size
        if len(input) != self.input_size:
            raise ValueError ('Input for neural network has wrong size. Expected '
                              + str(self.input_size) + ' elements but got ' + str(len(input)) + '.')

        # check if layer does exist
        if layer < 0 or layer > len(self.weights):
            raise ValueError ('Layer ' + str(layer) + ' does not exist. Maximum layer is '
                              + str(len(self.weights)) + '.')

        # compute output layerwise
        layer_input = layer_output = np.array(input).T[:,None]
        layer_count = 0
        for weights, bias, activations in zip(self.weights,self.bias, self.activations):

            # break if desired output layer is reached
            if layer_count == layer:
               break

            # compute weighted sum
            np_weights = np.array(weights)
            np_bias = np.array(bias)
            layer_output = np.matmul(np_weights,layer_input) + np_bias[:,None]
            layer_input = layer_output

            # apply activations
            for activation_idx,activation in enumerate(activations):
                if activation.lower() == 'id':
                    pass
                elif activation.lower() == 'relu':
                    layer_output[activation_idx,] = max(0, layer_output[activation_idx,])

            layer_count = layer_count + 1

        output_as_list = list(layer_output.T.flatten())

        return output_as_list

    def compute_neuron_output(self, input, layer, neuron):
        layer_output = self.compute_layer_output(input,layer)

        if 0 <= neuron <= len(layer_output):
            return layer_output[neuron]
        else:
            raise ValueError('Neuron ' + str(neuron) + ' does not exist in layer '
                             + str(layer) + '. Layer size is ' + str(len(layer_output)))

    def compute_output(self, input):
        return self.compute_layer_output(input, len(self.weights))

    """
    Helper Functions for further processing of network
    """

    def get_layer_count(self) -> int:
        return len(self.weights)

    def get_neuron_count(self, layer_index: int) -> int:
        return len(self.weights[layer_index])

    def get_neuron_weights(self, layer_index, neuron_index) -> list:
        return self.weights[layer_index][neuron_index]

    def get_neuron_bias(self, layer_index, neuron_index) -> float:
        return self.bias[layer_index][neuron_index]

    def get_neuron_activation(self, layer_index, neuron_index) -> str:
        return self.activations[layer_index][neuron_index]

    def __str__(self):
        return 'Input Size: ' + str(self.input_size) + '\n' \
               + 'Weights:\n' + str(self.weights) + '\n' \
               + 'Bias:\n' + str(self.bias) + '\n' \
               + 'Activations:\n' + str(self.activations) + '\n' \
               + 'Output Size: ' + str(self.output_size)

    def __repr__(self):
        return "ToyNNet()"


def generate_from_file(filepath):
    """Generates a ToyNNet object from .txt file

    To see an example of a toy neural network .txt file see 'assets\toy_nnet_example.txt'.
    If you want to understand more about the parsing procedure see any (good) ANTLRv4 tutorial.

    Args:
        filepath (str): Path to file which specifies the toy neural network.

    Returns:
        ToyNNet: Toy neural network as a ToyNNet object.

    Raises:
        ValueError: If there is anything wrong with this file (syntactical errors)
        then an error message is raised. (see _ToyNNetGenerator for this)

    """

    # parsing procedure
    input_stream = FileStream(filepath)
    lexer = ToyNNetLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ToyNNetParser(token_stream)
    toynetwork_tree = parser.toy_nnet()
    network_generator = _ToyNNetGenerator()
    walker = ParseTreeWalker()
    walker.walk(network_generator, toynetwork_tree)

    return ToyNNetwork(network_generator.network_input_size, network_generator.network_weights,
                       network_generator.network_bias, network_generator.network_activations)

def write_to_file(toynnet: ToyNNetwork, filepath: str):
    """Writes a ToyNNet in the .toynnet format.

    Args:
        filepath: Path to file where toynnet should be written
    """

    file = open(filepath, 'w')
    input_str = f"input_size={toynnet.input_size}\n"
    network_str = ""
    for layer_weights, layer_bias, layer_activations in zip(toynnet.weights,toynnet.bias, toynnet.activations):
        layer_str = ""
        for neuron_weights, neuron_bias, neuron_activation in zip(layer_weights, layer_bias, layer_activations):
            layer_str = layer_str + f'({neuron_weights}, {neuron_bias}, {neuron_activation});'
        layer_str = f"{layer_str[:-1]}\n"
        network_str = network_str + f"{layer_str}\n"

    file.write(input_str+network_str)
    file.close()
