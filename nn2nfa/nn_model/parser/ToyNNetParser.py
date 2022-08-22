# Generated from ToyNNet.g4 by ANTLR 4.10.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,14,73,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,5,
        0,14,8,0,10,0,12,0,17,9,0,1,0,1,0,4,0,21,8,0,11,0,12,0,22,1,0,4,
        0,26,8,0,11,0,12,0,27,1,0,5,0,31,8,0,10,0,12,0,34,9,0,1,0,1,0,1,
        1,1,1,1,1,1,1,1,2,1,2,1,2,5,2,45,8,2,10,2,12,2,48,9,2,1,2,1,2,1,
        3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,5,4,63,8,4,10,4,12,4,66,
        9,4,1,4,1,4,1,4,1,5,1,5,1,5,0,0,6,0,2,4,6,8,10,0,1,1,0,9,10,72,0,
        15,1,0,0,0,2,37,1,0,0,0,4,46,1,0,0,0,6,51,1,0,0,0,8,59,1,0,0,0,10,
        70,1,0,0,0,12,14,5,14,0,0,13,12,1,0,0,0,14,17,1,0,0,0,15,13,1,0,
        0,0,15,16,1,0,0,0,16,18,1,0,0,0,17,15,1,0,0,0,18,25,3,2,1,0,19,21,
        5,14,0,0,20,19,1,0,0,0,21,22,1,0,0,0,22,20,1,0,0,0,22,23,1,0,0,0,
        23,24,1,0,0,0,24,26,3,4,2,0,25,20,1,0,0,0,26,27,1,0,0,0,27,25,1,
        0,0,0,27,28,1,0,0,0,28,32,1,0,0,0,29,31,5,14,0,0,30,29,1,0,0,0,31,
        34,1,0,0,0,32,30,1,0,0,0,32,33,1,0,0,0,33,35,1,0,0,0,34,32,1,0,0,
        0,35,36,5,0,0,1,36,1,1,0,0,0,37,38,5,11,0,0,38,39,5,1,0,0,39,40,
        5,8,0,0,40,3,1,0,0,0,41,42,3,6,3,0,42,43,5,2,0,0,43,45,1,0,0,0,44,
        41,1,0,0,0,45,48,1,0,0,0,46,44,1,0,0,0,46,47,1,0,0,0,47,49,1,0,0,
        0,48,46,1,0,0,0,49,50,3,6,3,0,50,5,1,0,0,0,51,52,5,3,0,0,52,53,3,
        8,4,0,53,54,5,4,0,0,54,55,5,8,0,0,55,56,5,4,0,0,56,57,3,10,5,0,57,
        58,5,5,0,0,58,7,1,0,0,0,59,64,5,6,0,0,60,61,5,8,0,0,61,63,5,4,0,
        0,62,60,1,0,0,0,63,66,1,0,0,0,64,62,1,0,0,0,64,65,1,0,0,0,65,67,
        1,0,0,0,66,64,1,0,0,0,67,68,5,8,0,0,68,69,5,7,0,0,69,9,1,0,0,0,70,
        71,7,0,0,0,71,11,1,0,0,0,6,15,22,27,32,46,64
    ]

class ToyNNetParser ( Parser ):

    grammarFileName = "ToyNNet.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'='", "';'", "'('", "','", "')'", "'['", 
                     "']'", "<INVALID>", "<INVALID>", "<INVALID>", "'input_size'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "NUMBER", "RELU", "ID", "INPUTKEY", "COMMENT", "WHITESPACE", 
                      "NEWLINE" ]

    RULE_toy_nnet = 0
    RULE_nnet_input = 1
    RULE_layer = 2
    RULE_neuron = 3
    RULE_weights = 4
    RULE_activation = 5

    ruleNames =  [ "toy_nnet", "nnet_input", "layer", "neuron", "weights", 
                   "activation" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    NUMBER=8
    RELU=9
    ID=10
    INPUTKEY=11
    COMMENT=12
    WHITESPACE=13
    NEWLINE=14

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Toy_nnetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def nnet_input(self):
            return self.getTypedRuleContext(ToyNNetParser.Nnet_inputContext,0)


        def EOF(self):
            return self.getToken(ToyNNetParser.EOF, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(ToyNNetParser.NEWLINE)
            else:
                return self.getToken(ToyNNetParser.NEWLINE, i)

        def layer(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ToyNNetParser.LayerContext)
            else:
                return self.getTypedRuleContext(ToyNNetParser.LayerContext,i)


        def getRuleIndex(self):
            return ToyNNetParser.RULE_toy_nnet

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterToy_nnet" ):
                listener.enterToy_nnet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitToy_nnet" ):
                listener.exitToy_nnet(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitToy_nnet" ):
                return visitor.visitToy_nnet(self)
            else:
                return visitor.visitChildren(self)




    def toy_nnet(self):

        localctx = ToyNNetParser.Toy_nnetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_toy_nnet)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ToyNNetParser.NEWLINE:
                self.state = 12
                self.match(ToyNNetParser.NEWLINE)
                self.state = 17
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 18
            self.nnet_input()
            self.state = 25 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 20 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while True:
                        self.state = 19
                        self.match(ToyNNetParser.NEWLINE)
                        self.state = 22 
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if not (_la==ToyNNetParser.NEWLINE):
                            break

                    self.state = 24
                    self.layer()

                else:
                    raise NoViableAltException(self)
                self.state = 27 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

            self.state = 32
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==ToyNNetParser.NEWLINE:
                self.state = 29
                self.match(ToyNNetParser.NEWLINE)
                self.state = 34
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 35
            self.match(ToyNNetParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Nnet_inputContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INPUTKEY(self):
            return self.getToken(ToyNNetParser.INPUTKEY, 0)

        def NUMBER(self):
            return self.getToken(ToyNNetParser.NUMBER, 0)

        def getRuleIndex(self):
            return ToyNNetParser.RULE_nnet_input

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNnet_input" ):
                listener.enterNnet_input(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNnet_input" ):
                listener.exitNnet_input(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNnet_input" ):
                return visitor.visitNnet_input(self)
            else:
                return visitor.visitChildren(self)




    def nnet_input(self):

        localctx = ToyNNetParser.Nnet_inputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_nnet_input)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.match(ToyNNetParser.INPUTKEY)
            self.state = 38
            self.match(ToyNNetParser.T__0)
            self.state = 39
            self.match(ToyNNetParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LayerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def neuron(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ToyNNetParser.NeuronContext)
            else:
                return self.getTypedRuleContext(ToyNNetParser.NeuronContext,i)


        def getRuleIndex(self):
            return ToyNNetParser.RULE_layer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLayer" ):
                listener.enterLayer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLayer" ):
                listener.exitLayer(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLayer" ):
                return visitor.visitLayer(self)
            else:
                return visitor.visitChildren(self)




    def layer(self):

        localctx = ToyNNetParser.LayerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_layer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 41
                    self.neuron()
                    self.state = 42
                    self.match(ToyNNetParser.T__1) 
                self.state = 48
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

            self.state = 49
            self.neuron()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NeuronContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def weights(self):
            return self.getTypedRuleContext(ToyNNetParser.WeightsContext,0)


        def NUMBER(self):
            return self.getToken(ToyNNetParser.NUMBER, 0)

        def activation(self):
            return self.getTypedRuleContext(ToyNNetParser.ActivationContext,0)


        def getRuleIndex(self):
            return ToyNNetParser.RULE_neuron

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNeuron" ):
                listener.enterNeuron(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNeuron" ):
                listener.exitNeuron(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNeuron" ):
                return visitor.visitNeuron(self)
            else:
                return visitor.visitChildren(self)




    def neuron(self):

        localctx = ToyNNetParser.NeuronContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_neuron)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.match(ToyNNetParser.T__2)
            self.state = 52
            self.weights()
            self.state = 53
            self.match(ToyNNetParser.T__3)
            self.state = 54
            self.match(ToyNNetParser.NUMBER)
            self.state = 55
            self.match(ToyNNetParser.T__3)
            self.state = 56
            self.activation()
            self.state = 57
            self.match(ToyNNetParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WeightsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self, i:int=None):
            if i is None:
                return self.getTokens(ToyNNetParser.NUMBER)
            else:
                return self.getToken(ToyNNetParser.NUMBER, i)

        def getRuleIndex(self):
            return ToyNNetParser.RULE_weights

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWeights" ):
                listener.enterWeights(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWeights" ):
                listener.exitWeights(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWeights" ):
                return visitor.visitWeights(self)
            else:
                return visitor.visitChildren(self)




    def weights(self):

        localctx = ToyNNetParser.WeightsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_weights)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(ToyNNetParser.T__5)
            self.state = 64
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 60
                    self.match(ToyNNetParser.NUMBER)
                    self.state = 61
                    self.match(ToyNNetParser.T__3) 
                self.state = 66
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 67
            self.match(ToyNNetParser.NUMBER)
            self.state = 68
            self.match(ToyNNetParser.T__6)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ActivationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RELU(self):
            return self.getToken(ToyNNetParser.RELU, 0)

        def ID(self):
            return self.getToken(ToyNNetParser.ID, 0)

        def getRuleIndex(self):
            return ToyNNetParser.RULE_activation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterActivation" ):
                listener.enterActivation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitActivation" ):
                listener.exitActivation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitActivation" ):
                return visitor.visitActivation(self)
            else:
                return visitor.visitChildren(self)




    def activation(self):

        localctx = ToyNNetParser.ActivationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_activation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 70
            _la = self._input.LA(1)
            if not(_la==ToyNNetParser.RELU or _la==ToyNNetParser.ID):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





