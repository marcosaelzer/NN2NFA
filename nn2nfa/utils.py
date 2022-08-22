from nn2nfa.nn_model import ToyNNetwork
from nn2nfa.out_reach_properties.out_reach_property import OutReachProperty


def check_if_nn_and_out_reach_property_match(toy_nnet: ToyNNetwork, out_reach_property: OutReachProperty) -> bool:
    for idx, inequality in enumerate(out_reach_property.input_specification):
        if len(inequality.left_side) != toy_nnet.input_size:
            print(f"Warning: The size {len(inequality.left_side)} of the {idx}st inequality of the input specification "
                  f"does not match the input size {toy_nnet.input_size} of the neural network.")
            return False

    for idx, inequality in enumerate(out_reach_property.output_specification):
        if len(inequality.left_side) != toy_nnet.output_size:
            print(f"Warning: The size {len(inequality.left_side)} of the {idx}st inequality of the output specification "
                  f"does not match the output size {toy_nnet.output_size} of the neural network.")
            return False

    return True