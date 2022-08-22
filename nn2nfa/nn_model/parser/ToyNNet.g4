grammar ToyNNet;

// GRAMMAR RULES

toy_nnet : NEWLINE* nnet_input (NEWLINE+ layer)+ NEWLINE* EOF;
nnet_input : INPUTKEY '=' NUMBER ;
layer : (neuron ';')* neuron ;
neuron : '(' weights ',' NUMBER ',' activation ')' ;
weights : '[' (NUMBER ',')* NUMBER ']' ;
activation : RELU | ID ;

// LEXER RULES

fragment R : ('R'|'r') ;
fragment E : ('E'|'e') ;
fragment L : ('L'|'l') ;
fragment U : ('U'|'u') ;

fragment I : ('I'|'i') ;
fragment D : ('D'|'d') ;

fragment DIGIT : [0-9] ;

NUMBER : '-'? DIGIT+ ('.' DIGIT+)? ;

// activation functions
RELU : R E L U ;
ID : I D ;

// keywords
INPUTKEY : 'input_size' ;

COMMENT : '#' ~[\r\n]* (NEWLINE | EOF) -> skip ;
WHITESPACE : (' ' | '\t') -> skip ;
NEWLINE   : '\r\n' | '\n' | '\r';
