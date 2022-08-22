# Generated from ToyNNet.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from nn2nfa.nn_model.parser.ToyNNetParser import ToyNNetParser
else:
    from ToyNNetParser import ToyNNetParser

# This class defines a complete listener for a parse tree produced by ToyNNetParser.
class ToyNNetListener(ParseTreeListener):

    # Enter a parse tree produced by ToyNNetParser#toy_nnet.
    def enterToy_nnet(self, ctx:ToyNNetParser.Toy_nnetContext):
        pass

    # Exit a parse tree produced by ToyNNetParser#toy_nnet.
    def exitToy_nnet(self, ctx:ToyNNetParser.Toy_nnetContext):
        pass


    # Enter a parse tree produced by ToyNNetParser#nnet_input.
    def enterNnet_input(self, ctx:ToyNNetParser.Nnet_inputContext):
        pass

    # Exit a parse tree produced by ToyNNetParser#nnet_input.
    def exitNnet_input(self, ctx:ToyNNetParser.Nnet_inputContext):
        pass


    # Enter a parse tree produced by ToyNNetParser#layer.
    def enterLayer(self, ctx:ToyNNetParser.LayerContext):
        pass

    # Exit a parse tree produced by ToyNNetParser#layer.
    def exitLayer(self, ctx:ToyNNetParser.LayerContext):
        pass


    # Enter a parse tree produced by ToyNNetParser#neuron.
    def enterNeuron(self, ctx:ToyNNetParser.NeuronContext):
        pass

    # Exit a parse tree produced by ToyNNetParser#neuron.
    def exitNeuron(self, ctx:ToyNNetParser.NeuronContext):
        pass


    # Enter a parse tree produced by ToyNNetParser#weights.
    def enterWeights(self, ctx:ToyNNetParser.WeightsContext):
        pass

    # Exit a parse tree produced by ToyNNetParser#weights.
    def exitWeights(self, ctx:ToyNNetParser.WeightsContext):
        pass


    # Enter a parse tree produced by ToyNNetParser#activation.
    def enterActivation(self, ctx:ToyNNetParser.ActivationContext):
        pass

    # Exit a parse tree produced by ToyNNetParser#activation.
    def exitActivation(self, ctx:ToyNNetParser.ActivationContext):
        pass



del ToyNNetParser