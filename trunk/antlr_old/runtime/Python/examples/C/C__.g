lexer grammar C;
options {
  language=Python;

}

T23 : 'typedef' ;
T24 : ';' ;
T25 : ',' ;
T26 : '=' ;
T27 : 'extern' ;
T28 : 'static' ;
T29 : 'auto' ;
T30 : 'register' ;
T31 : 'void' ;
T32 : 'char' ;
T33 : 'short' ;
T34 : 'int' ;
T35 : 'long' ;
T36 : 'float' ;
T37 : 'double' ;
T38 : 'signed' ;
T39 : 'unsigned' ;
T40 : '{' ;
T41 : '}' ;
T42 : 'struct' ;
T43 : 'union' ;
T44 : ':' ;
T45 : 'enum' ;
T46 : 'const' ;
T47 : 'volatile' ;
T48 : '(' ;
T49 : ')' ;
T50 : '[' ;
T51 : ']' ;
T52 : '*' ;
T53 : '...' ;
T54 : '+' ;
T55 : '-' ;
T56 : '/' ;
T57 : '%' ;
T58 : '++' ;
T59 : '--' ;
T60 : 'sizeof' ;
T61 : '.' ;
T62 : '->' ;
T63 : '&' ;
T64 : '~' ;
T65 : '!' ;
T66 : '*=' ;
T67 : '/=' ;
T68 : '%=' ;
T69 : '+=' ;
T70 : '-=' ;
T71 : '<<=' ;
T72 : '>>=' ;
T73 : '&=' ;
T74 : '^=' ;
T75 : '|=' ;
T76 : '?' ;
T77 : '||' ;
T78 : '&&' ;
T79 : '|' ;
T80 : '^' ;
T81 : '==' ;
T82 : '!=' ;
T83 : '<' ;
T84 : '>' ;
T85 : '<=' ;
T86 : '>=' ;
T87 : '<<' ;
T88 : '>>' ;
T89 : 'case' ;
T90 : 'default' ;
T91 : 'if' ;
T92 : 'else' ;
T93 : 'switch' ;
T94 : 'while' ;
T95 : 'do' ;
T96 : 'for' ;
T97 : 'goto' ;
T98 : 'continue' ;
T99 : 'break' ;
T100 : 'return' ;

// $ANTLR src "C.g" 466
IDENTIFIER
	:	LETTER (LETTER|'0'..'9')*
	;
	
// $ANTLR src "C.g" 470
fragment
LETTER
	:	'$'
	|	'A'..'Z'
	|	'a'..'z'
	|	'_'
	;

// $ANTLR src "C.g" 478
CHARACTER_LITERAL
    :   '\'' ( EscapeSequence | ~('\''|'\\') ) '\''
    ;

// $ANTLR src "C.g" 482
STRING_LITERAL
    :  '"' ( EscapeSequence | ~('\\'|'"') )* '"'
    ;

// $ANTLR src "C.g" 486
HEX_LITERAL : '0' ('x'|'X') HexDigit+ IntegerTypeSuffix? ;

// $ANTLR src "C.g" 488
DECIMAL_LITERAL : ('0' | '1'..'9' '0'..'9'*) IntegerTypeSuffix? ;

// $ANTLR src "C.g" 490
OCTAL_LITERAL : '0' ('0'..'7')+ IntegerTypeSuffix? ;

// $ANTLR src "C.g" 492
fragment
HexDigit : ('0'..'9'|'a'..'f'|'A'..'F') ;

// $ANTLR src "C.g" 495
fragment
IntegerTypeSuffix
	:	('u'|'U')? ('l'|'L')
	|	('u'|'U')  ('l'|'L')?
	;

// $ANTLR src "C.g" 501
FLOATING_POINT_LITERAL
    :   ('0'..'9')+ '.' ('0'..'9')* Exponent? FloatTypeSuffix?
    |   '.' ('0'..'9')+ Exponent? FloatTypeSuffix?
    |   ('0'..'9')+ Exponent FloatTypeSuffix?
    |   ('0'..'9')+ Exponent? FloatTypeSuffix
	;

// $ANTLR src "C.g" 508
fragment
Exponent : ('e'|'E') ('+'|'-')? ('0'..'9')+ ;

// $ANTLR src "C.g" 511
fragment
FloatTypeSuffix : ('f'|'F'|'d'|'D') ;

// $ANTLR src "C.g" 514
fragment
EscapeSequence
    :   '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
    |   OctalEscape
    ;

// $ANTLR src "C.g" 520
fragment
OctalEscape
    :   '\\' ('0'..'3') ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7') ('0'..'7')
    |   '\\' ('0'..'7')
    ;

// $ANTLR src "C.g" 527
fragment
UnicodeEscape
    :   '\\' 'u' HexDigit HexDigit HexDigit HexDigit
    ;

// $ANTLR src "C.g" 532
WS  :  (' '|'\r'|'\t'|'\u000C'|'\n') {$channel=HIDDEN;}
    ;

// $ANTLR src "C.g" 535
COMMENT
    :   '/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
    ;

// $ANTLR src "C.g" 539
LINE_COMMENT
    : '//' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    ;

// ignore #line info for now
// $ANTLR src "C.g" 544
LINE_COMMAND 
    : '#' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    ;
