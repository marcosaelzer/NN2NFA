from typing import List
import numpy as np

from nn2nfa.nn_model import ToyNNetwork


class BNNBuilder():

    def build_bnn_with_uniform_and_relu(self, input_size: int, layer_specs: List[int]) -> ToyNNetwork:
        """Returns a BNN with uniformly distributed weight and bias values taken from {-1,1} and
        ReLU activations

        Args:
            input_size: input dimension of the BNN
            layer_specs: len(layer_specs) defines the number of layer of the BNN and layer_specs[i]
            the number of nodes in layer i

        Returns:
            ToyNNetwork: BNN of with input_size input dimensions and len(layer_specs) layers
        """
        # define set of allowed parameters for bnn
        valid_bnn_parameters = [-1,1]

        # draw parameters uniformly
        num_weights = input_size * layer_specs[0] + sum([layer_specs[i-1] * layer_specs[i] for i in range(1,len(layer_specs))])
        num_bias = sum(layer_specs)
        parameters = np.random.choice([-1,1],num_weights + num_bias)

        # set parameters for first layer
        weights = [[list(np.random.choice(valid_bnn_parameters,input_size)) for _ in range(layer_specs[0])]]
        bias = [[np.random.choice(valid_bnn_parameters,1)[0] for _ in range(layer_specs[0])]]
        activations = [['relu' for _ in range(layer_specs[0])]]

        previous_spec = 0
        for layer_spec in layer_specs[1:]:
            # build NN components for layer
            weights.append([list(np.random.choice(valid_bnn_parameters,layer_specs[previous_spec])) for _ in range(layer_spec)])
            bias.append([np.random.choice(valid_bnn_parameters,1)[0] for _ in range(layer_spec)])
            activations.append(['relu' for _ in range(layer_spec)])

            previous_spec += 1

        return ToyNNetwork(input_size, weights, bias, activations)