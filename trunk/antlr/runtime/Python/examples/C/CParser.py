# $ANTLR 3.0.1 C.g 2008-07-31 13:59:56

from antlr3 import *
from antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
LINE_COMMENT=21
FloatTypeSuffix=16
IntegerTypeSuffix=14
LETTER=11
OCTAL_LITERAL=6
CHARACTER_LITERAL=8
Exponent=15
EOF=-1
HexDigit=13
STRING_LITERAL=9
WS=19
FLOATING_POINT_LITERAL=10
IDENTIFIER=4
UnicodeEscape=18
LINE_COMMAND=22
HEX_LITERAL=5
COMMENT=20
DECIMAL_LITERAL=7
EscapeSequence=12
OctalEscape=17

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "IDENTIFIER", "HEX_LITERAL", "OCTAL_LITERAL", "DECIMAL_LITERAL", "CHARACTER_LITERAL", 
    "STRING_LITERAL", "FLOATING_POINT_LITERAL", "LETTER", "EscapeSequence", 
    "HexDigit", "IntegerTypeSuffix", "Exponent", "FloatTypeSuffix", "OctalEscape", 
    "UnicodeEscape", "WS", "COMMENT", "LINE_COMMENT", "LINE_COMMAND", "'typedef'", 
    "';'", "','", "'='", "'extern'", "'static'", "'auto'", "'register'", 
    "'void'", "'char'", "'short'", "'int'", "'long'", "'float'", "'double'", 
    "'signed'", "'unsigned'", "'{'", "'}'", "'struct'", "'union'", "':'", 
    "'enum'", "'const'", "'volatile'", "'('", "')'", "'['", "']'", "'*'", 
    "'...'", "'+'", "'-'", "'/'", "'%'", "'++'", "'--'", "'sizeof'", "'.'", 
    "'->'", "'&'", "'~'", "'!'", "'*='", "'/='", "'%='", "'+='", "'-='", 
    "'<<='", "'>>='", "'&='", "'^='", "'|='", "'?'", "'||'", "'&&'", "'|'", 
    "'^'", "'=='", "'!='", "'<'", "'>'", "'<='", "'>='", "'<<'", "'>>'", 
    "'case'", "'default'", "'if'", "'else'", "'switch'", "'while'", "'do'", 
    "'for'", "'goto'", "'continue'", "'break'", "'return'"
]

class Symbols_scope(object):
    def __init__(self):
        self.types = None


class declaration_scope(object):
    def __init__(self):
        self.isTypedef = None


class CParser(Parser):
    grammarFileName = "C.g"
    tokenNames = tokenNames

    def __init__(self, input):
        Parser.__init__(self, input)
        self.ruleMemo = {}

        self.Symbols_stack = []

	self.declaration_stack = []



                


              
    def isTypeName(self, name):
        for scope in reversed(self.Symbols_stack):
            if name in scope.types:
                return True

        return False




    # $ANTLR start translation_unit
    # C.g:55:1: translation_unit : ( external_declaration )+ ;
    def translation_unit(self, ):
        self.Symbols_stack.append(Symbols_scope())

        translation_unit_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 1):
                    return 

                # C.g:60:2: ( ( external_declaration )+ )
                # C.g:60:4: ( external_declaration )+
                # C.g:60:4: ( external_declaration )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == IDENTIFIER or LA1_0 == 23 or (27 <= LA1_0 <= 39) or (42 <= LA1_0 <= 43) or (45 <= LA1_0 <= 48) or LA1_0 == 52) :
                        alt1 = 1


                    if alt1 == 1:
                        # C.g:0:0: external_declaration
                        self.following.append(self.FOLLOW_external_declaration_in_translation_unit77)
                        self.external_declaration()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt1 >= 1:
                            break #loop1

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(1, self.input)
                        raise eee

                    cnt1 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 1, translation_unit_StartIndex)

            self.Symbols_stack.pop()

            pass

        return 

    # $ANTLR end translation_unit


    # $ANTLR start external_declaration
    # C.g:63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );
    def external_declaration(self, ):

        external_declaration_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 2):
                    return 

                # C.g:79:2: ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration )
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((27 <= LA2_0 <= 30)) :
                    LA2_1 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 1, self.input)

                        raise nvae

                elif (LA2_0 == 31) :
                    LA2_2 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 2, self.input)

                        raise nvae

                elif (LA2_0 == 32) :
                    LA2_3 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 3, self.input)

                        raise nvae

                elif (LA2_0 == 33) :
                    LA2_4 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 4, self.input)

                        raise nvae

                elif (LA2_0 == 34) :
                    LA2_5 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 5, self.input)

                        raise nvae

                elif (LA2_0 == 35) :
                    LA2_6 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 6, self.input)

                        raise nvae

                elif (LA2_0 == 36) :
                    LA2_7 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 7, self.input)

                        raise nvae

                elif (LA2_0 == 37) :
                    LA2_8 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 8, self.input)

                        raise nvae

                elif (LA2_0 == 38) :
                    LA2_9 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 9, self.input)

                        raise nvae

                elif (LA2_0 == 39) :
                    LA2_10 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 10, self.input)

                        raise nvae

                elif ((42 <= LA2_0 <= 43)) :
                    LA2_11 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 11, self.input)

                        raise nvae

                elif (LA2_0 == 45) :
                    LA2_12 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 12, self.input)

                        raise nvae

                elif (LA2_0 == IDENTIFIER) :
                    LA2_13 = self.input.LA(2)

                    if (((self.synpred4() and self.isTypeName(self.input.LT(1).text)) or self.synpred4())) :
                        alt2 = 1
                    elif (self.isTypeName(self.input.LT(1).text)) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 13, self.input)

                        raise nvae

                elif ((46 <= LA2_0 <= 47)) :
                    LA2_14 = self.input.LA(2)

                    if (self.synpred4()) :
                        alt2 = 1
                    elif (True) :
                        alt2 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 14, self.input)

                        raise nvae

                elif (LA2_0 == 52) and (self.synpred4()):
                    alt2 = 1
                elif (LA2_0 == 48) and (self.synpred4()):
                    alt2 = 1
                elif (LA2_0 == 23) :
                    alt2 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("63:1: external_declaration options {k=1; } : ( ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition | declaration );", 2, 0, self.input)

                    raise nvae

                if alt2 == 1:
                    # C.g:79:4: ( ( declaration_specifiers )? declarator ( declaration )* '{' )=> function_definition
                    self.following.append(self.FOLLOW_function_definition_in_external_declaration113)
                    self.function_definition()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt2 == 2:
                    # C.g:80:4: declaration
                    self.following.append(self.FOLLOW_declaration_in_external_declaration118)
                    self.declaration()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 2, external_declaration_StartIndex)

            pass

        return 

    # $ANTLR end external_declaration


    # $ANTLR start function_definition
    # C.g:83:1: function_definition : ( declaration_specifiers )? declarator ( ( declaration )+ compound_statement | compound_statement ) ;
    def function_definition(self, ):
        self.Symbols_stack.append(Symbols_scope())

        function_definition_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 3):
                    return 

                # C.g:88:2: ( ( declaration_specifiers )? declarator ( ( declaration )+ compound_statement | compound_statement ) )
                # C.g:88:4: ( declaration_specifiers )? declarator ( ( declaration )+ compound_statement | compound_statement )
                # C.g:88:4: ( declaration_specifiers )?
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if ((27 <= LA3_0 <= 39) or (42 <= LA3_0 <= 43) or (45 <= LA3_0 <= 47)) :
                    alt3 = 1
                elif (LA3_0 == IDENTIFIER) :
                    LA3 = self.input.LA(2)
                    if LA3 == 48:
                        LA3_18 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 27 or LA3 == 28 or LA3 == 29 or LA3 == 30:
                        LA3_20 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 31:
                        LA3_21 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 32:
                        LA3_22 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 33:
                        LA3_23 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 34:
                        LA3_24 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 35:
                        LA3_25 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 36:
                        LA3_26 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 37:
                        LA3_27 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 38:
                        LA3_28 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 39:
                        LA3_29 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 42 or LA3 == 43:
                        LA3_30 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 45:
                        LA3_31 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == IDENTIFIER:
                        LA3_32 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 46 or LA3 == 47:
                        LA3_33 = self.input.LA(3)

                        if ((self.synpred5() and self.isTypeName(self.input.LT(1).text))) :
                            alt3 = 1
                    elif LA3 == 52:
                        alt3 = 1
                if alt3 == 1:
                    # C.g:0:0: declaration_specifiers
                    self.following.append(self.FOLLOW_declaration_specifiers_in_function_definition140)
                    self.declaration_specifiers()
                    self.following.pop()
                    if self.failed:
                        return 



                self.following.append(self.FOLLOW_declarator_in_function_definition143)
                self.declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:89:3: ( ( declaration )+ compound_statement | compound_statement )
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == IDENTIFIER or LA5_0 == 23 or (27 <= LA5_0 <= 39) or (42 <= LA5_0 <= 43) or (45 <= LA5_0 <= 47)) :
                    alt5 = 1
                elif (LA5_0 == 40) :
                    alt5 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("89:3: ( ( declaration )+ compound_statement | compound_statement )", 5, 0, self.input)

                    raise nvae

                if alt5 == 1:
                    # C.g:89:5: ( declaration )+ compound_statement
                    # C.g:89:5: ( declaration )+
                    cnt4 = 0
                    while True: #loop4
                        alt4 = 2
                        LA4_0 = self.input.LA(1)

                        if (LA4_0 == IDENTIFIER or LA4_0 == 23 or (27 <= LA4_0 <= 39) or (42 <= LA4_0 <= 43) or (45 <= LA4_0 <= 47)) :
                            alt4 = 1


                        if alt4 == 1:
                            # C.g:0:0: declaration
                            self.following.append(self.FOLLOW_declaration_in_function_definition149)
                            self.declaration()
                            self.following.pop()
                            if self.failed:
                                return 


                        else:
                            if cnt4 >= 1:
                                break #loop4

                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            eee = EarlyExitException(4, self.input)
                            raise eee

                        cnt4 += 1


                    self.following.append(self.FOLLOW_compound_statement_in_function_definition152)
                    self.compound_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt5 == 2:
                    # C.g:90:5: compound_statement
                    self.following.append(self.FOLLOW_compound_statement_in_function_definition159)
                    self.compound_statement()
                    self.following.pop()
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 3, function_definition_StartIndex)

            self.Symbols_stack.pop()

            pass

        return 

    # $ANTLR end function_definition


    # $ANTLR start declaration
    # C.g:94:1: declaration : ( 'typedef' ( declaration_specifiers )? init_declarator_list ';' | declaration_specifiers ( init_declarator_list )? ';' );
    def declaration(self, ):
        self.declaration_stack.append(declaration_scope())
        declaration_StartIndex = self.input.index()
               
        self.declaration_stack[-1].isTypedef =  False

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 4):
                    return 

                # C.g:101:2: ( 'typedef' ( declaration_specifiers )? init_declarator_list ';' | declaration_specifiers ( init_declarator_list )? ';' )
                alt8 = 2
                LA8_0 = self.input.LA(1)

                if (LA8_0 == 23) :
                    alt8 = 1
                elif (LA8_0 == IDENTIFIER or (27 <= LA8_0 <= 39) or (42 <= LA8_0 <= 43) or (45 <= LA8_0 <= 47)) :
                    alt8 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("94:1: declaration : ( 'typedef' ( declaration_specifiers )? init_declarator_list ';' | declaration_specifiers ( init_declarator_list )? ';' );", 8, 0, self.input)

                    raise nvae

                if alt8 == 1:
                    # C.g:101:4: 'typedef' ( declaration_specifiers )? init_declarator_list ';'
                    self.match(self.input, 23, self.FOLLOW_23_in_declaration187)
                    if self.failed:
                        return 
                    # C.g:101:14: ( declaration_specifiers )?
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if ((27 <= LA6_0 <= 39) or (42 <= LA6_0 <= 43) or (45 <= LA6_0 <= 47)) :
                        alt6 = 1
                    elif (LA6_0 == IDENTIFIER) :
                        LA6_13 = self.input.LA(2)

                        if (LA6_13 == IDENTIFIER or (27 <= LA6_13 <= 39) or (42 <= LA6_13 <= 43) or (45 <= LA6_13 <= 47) or LA6_13 == 52) :
                            alt6 = 1
                        elif (LA6_13 == 48) :
                            LA6_19 = self.input.LA(3)

                            if ((self.synpred8() and self.isTypeName(self.input.LT(1).text))) :
                                alt6 = 1
                    if alt6 == 1:
                        # C.g:0:0: declaration_specifiers
                        self.following.append(self.FOLLOW_declaration_specifiers_in_declaration189)
                        self.declaration_specifiers()
                        self.following.pop()
                        if self.failed:
                            return 



                    if self.backtracking == 0:
                        self.declaration_stack[-1].isTypedef=True

                    self.following.append(self.FOLLOW_init_declarator_list_in_declaration197)
                    self.init_declarator_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_declaration199)
                    if self.failed:
                        return 


                elif alt8 == 2:
                    # C.g:103:4: declaration_specifiers ( init_declarator_list )? ';'
                    self.following.append(self.FOLLOW_declaration_specifiers_in_declaration205)
                    self.declaration_specifiers()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:103:27: ( init_declarator_list )?
                    alt7 = 2
                    LA7_0 = self.input.LA(1)

                    if (LA7_0 == IDENTIFIER or LA7_0 == 48 or LA7_0 == 52) :
                        alt7 = 1
                    if alt7 == 1:
                        # C.g:0:0: init_declarator_list
                        self.following.append(self.FOLLOW_init_declarator_list_in_declaration207)
                        self.init_declarator_list()
                        self.following.pop()
                        if self.failed:
                            return 



                    self.match(self.input, 24, self.FOLLOW_24_in_declaration210)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 4, declaration_StartIndex)

            self.declaration_stack.pop()
            pass

        return 

    # $ANTLR end declaration


    # $ANTLR start declaration_specifiers
    # C.g:106:1: declaration_specifiers : ( storage_class_specifier | type_specifier | type_qualifier )+ ;
    def declaration_specifiers(self, ):

        declaration_specifiers_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 5):
                    return 

                # C.g:107:2: ( ( storage_class_specifier | type_specifier | type_qualifier )+ )
                # C.g:107:6: ( storage_class_specifier | type_specifier | type_qualifier )+
                # C.g:107:6: ( storage_class_specifier | type_specifier | type_qualifier )+
                cnt9 = 0
                while True: #loop9
                    alt9 = 4
                    LA9 = self.input.LA(1)
                    if LA9 == IDENTIFIER:
                        LA9_2 = self.input.LA(2)

                        if ((self.synpred12() and self.isTypeName(self.input.LT(1).text))) :
                            alt9 = 2


                    elif LA9 == 27 or LA9 == 28 or LA9 == 29 or LA9 == 30:
                        alt9 = 1
                    elif LA9 == 31 or LA9 == 32 or LA9 == 33 or LA9 == 34 or LA9 == 35 or LA9 == 36 or LA9 == 37 or LA9 == 38 or LA9 == 39 or LA9 == 42 or LA9 == 43 or LA9 == 45:
                        alt9 = 2
                    elif LA9 == 46 or LA9 == 47:
                        alt9 = 3

                    if alt9 == 1:
                        # C.g:107:10: storage_class_specifier
                        self.following.append(self.FOLLOW_storage_class_specifier_in_declaration_specifiers227)
                        self.storage_class_specifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt9 == 2:
                        # C.g:108:7: type_specifier
                        self.following.append(self.FOLLOW_type_specifier_in_declaration_specifiers235)
                        self.type_specifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt9 == 3:
                        # C.g:109:13: type_qualifier
                        self.following.append(self.FOLLOW_type_qualifier_in_declaration_specifiers249)
                        self.type_qualifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt9 >= 1:
                            break #loop9

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(9, self.input)
                        raise eee

                    cnt9 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 5, declaration_specifiers_StartIndex)

            pass

        return 

    # $ANTLR end declaration_specifiers


    # $ANTLR start init_declarator_list
    # C.g:113:1: init_declarator_list : init_declarator ( ',' init_declarator )* ;
    def init_declarator_list(self, ):

        init_declarator_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 6):
                    return 

                # C.g:114:2: ( init_declarator ( ',' init_declarator )* )
                # C.g:114:4: init_declarator ( ',' init_declarator )*
                self.following.append(self.FOLLOW_init_declarator_in_init_declarator_list271)
                self.init_declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:114:20: ( ',' init_declarator )*
                while True: #loop10
                    alt10 = 2
                    LA10_0 = self.input.LA(1)

                    if (LA10_0 == 25) :
                        alt10 = 1


                    if alt10 == 1:
                        # C.g:114:21: ',' init_declarator
                        self.match(self.input, 25, self.FOLLOW_25_in_init_declarator_list274)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_init_declarator_in_init_declarator_list276)
                        self.init_declarator()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop10






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 6, init_declarator_list_StartIndex)

            pass

        return 

    # $ANTLR end init_declarator_list


    # $ANTLR start init_declarator
    # C.g:117:1: init_declarator : declarator ( '=' initializer )? ;
    def init_declarator(self, ):

        init_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 7):
                    return 

                # C.g:118:2: ( declarator ( '=' initializer )? )
                # C.g:118:4: declarator ( '=' initializer )?
                self.following.append(self.FOLLOW_declarator_in_init_declarator289)
                self.declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:118:15: ( '=' initializer )?
                alt11 = 2
                LA11_0 = self.input.LA(1)

                if (LA11_0 == 26) :
                    alt11 = 1
                if alt11 == 1:
                    # C.g:118:16: '=' initializer
                    self.match(self.input, 26, self.FOLLOW_26_in_init_declarator292)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_initializer_in_init_declarator294)
                    self.initializer()
                    self.following.pop()
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 7, init_declarator_StartIndex)

            pass

        return 

    # $ANTLR end init_declarator


    # $ANTLR start storage_class_specifier
    # C.g:121:1: storage_class_specifier : ( 'extern' | 'static' | 'auto' | 'register' );
    def storage_class_specifier(self, ):

        storage_class_specifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 8):
                    return 

                # C.g:122:2: ( 'extern' | 'static' | 'auto' | 'register' )
                # C.g:
                if (27 <= self.input.LA(1) <= 30):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_storage_class_specifier0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 8, storage_class_specifier_StartIndex)

            pass

        return 

    # $ANTLR end storage_class_specifier


    # $ANTLR start type_specifier
    # C.g:128:1: type_specifier : ( 'void' | 'char' | 'short' | 'int' | 'long' | 'float' | 'double' | 'signed' | 'unsigned' | struct_or_union_specifier | enum_specifier | type_id );
    def type_specifier(self, ):

        type_specifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 9):
                    return 

                # C.g:129:2: ( 'void' | 'char' | 'short' | 'int' | 'long' | 'float' | 'double' | 'signed' | 'unsigned' | struct_or_union_specifier | enum_specifier | type_id )
                alt12 = 12
                LA12 = self.input.LA(1)
                if LA12 == 31:
                    alt12 = 1
                elif LA12 == 32:
                    alt12 = 2
                elif LA12 == 33:
                    alt12 = 3
                elif LA12 == 34:
                    alt12 = 4
                elif LA12 == 35:
                    alt12 = 5
                elif LA12 == 36:
                    alt12 = 6
                elif LA12 == 37:
                    alt12 = 7
                elif LA12 == 38:
                    alt12 = 8
                elif LA12 == 39:
                    alt12 = 9
                elif LA12 == 42 or LA12 == 43:
                    alt12 = 10
                elif LA12 == 45:
                    alt12 = 11
                elif LA12 == IDENTIFIER:
                    alt12 = 12
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("128:1: type_specifier : ( 'void' | 'char' | 'short' | 'int' | 'long' | 'float' | 'double' | 'signed' | 'unsigned' | struct_or_union_specifier | enum_specifier | type_id );", 12, 0, self.input)

                    raise nvae

                if alt12 == 1:
                    # C.g:129:4: 'void'
                    self.match(self.input, 31, self.FOLLOW_31_in_type_specifier333)
                    if self.failed:
                        return 


                elif alt12 == 2:
                    # C.g:130:4: 'char'
                    self.match(self.input, 32, self.FOLLOW_32_in_type_specifier338)
                    if self.failed:
                        return 


                elif alt12 == 3:
                    # C.g:131:4: 'short'
                    self.match(self.input, 33, self.FOLLOW_33_in_type_specifier343)
                    if self.failed:
                        return 


                elif alt12 == 4:
                    # C.g:132:4: 'int'
                    self.match(self.input, 34, self.FOLLOW_34_in_type_specifier348)
                    if self.failed:
                        return 


                elif alt12 == 5:
                    # C.g:133:4: 'long'
                    self.match(self.input, 35, self.FOLLOW_35_in_type_specifier353)
                    if self.failed:
                        return 


                elif alt12 == 6:
                    # C.g:134:4: 'float'
                    self.match(self.input, 36, self.FOLLOW_36_in_type_specifier358)
                    if self.failed:
                        return 


                elif alt12 == 7:
                    # C.g:135:4: 'double'
                    self.match(self.input, 37, self.FOLLOW_37_in_type_specifier363)
                    if self.failed:
                        return 


                elif alt12 == 8:
                    # C.g:136:4: 'signed'
                    self.match(self.input, 38, self.FOLLOW_38_in_type_specifier368)
                    if self.failed:
                        return 


                elif alt12 == 9:
                    # C.g:137:4: 'unsigned'
                    self.match(self.input, 39, self.FOLLOW_39_in_type_specifier373)
                    if self.failed:
                        return 


                elif alt12 == 10:
                    # C.g:138:4: struct_or_union_specifier
                    self.following.append(self.FOLLOW_struct_or_union_specifier_in_type_specifier378)
                    self.struct_or_union_specifier()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt12 == 11:
                    # C.g:139:4: enum_specifier
                    self.following.append(self.FOLLOW_enum_specifier_in_type_specifier383)
                    self.enum_specifier()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt12 == 12:
                    # C.g:140:4: type_id
                    self.following.append(self.FOLLOW_type_id_in_type_specifier388)
                    self.type_id()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 9, type_specifier_StartIndex)

            pass

        return 

    # $ANTLR end type_specifier


    # $ANTLR start type_id
    # C.g:143:1: type_id : {...}? IDENTIFIER ;
    def type_id(self, ):

        type_id_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 10):
                    return 

                # C.g:144:5: ({...}? IDENTIFIER )
                # C.g:144:9: {...}? IDENTIFIER
                if not (self.isTypeName(self.input.LT(1).text)):
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    raise FailedPredicateException(self.input, "type_id", "self.isTypeName(self.input.LT(1).text)")

                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_type_id406)
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 10, type_id_StartIndex)

            pass

        return 

    # $ANTLR end type_id


    # $ANTLR start struct_or_union_specifier
    # C.g:148:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );
    def struct_or_union_specifier(self, ):
        self.Symbols_stack.append(Symbols_scope())

        struct_or_union_specifier_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 11):
                    return 

                # C.g:154:2: ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER )
                alt14 = 2
                LA14_0 = self.input.LA(1)

                if ((42 <= LA14_0 <= 43)) :
                    LA14_1 = self.input.LA(2)

                    if (LA14_1 == IDENTIFIER) :
                        LA14_2 = self.input.LA(3)

                        if (LA14_2 == 40) :
                            alt14 = 1
                        elif (LA14_2 == EOF or LA14_2 == IDENTIFIER or (24 <= LA14_2 <= 25) or (27 <= LA14_2 <= 39) or (42 <= LA14_2 <= 50) or LA14_2 == 52) :
                            alt14 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("148:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );", 14, 2, self.input)

                            raise nvae

                    elif (LA14_1 == 40) :
                        alt14 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("148:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );", 14, 1, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("148:1: struct_or_union_specifier options {k=3; } : ( struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}' | struct_or_union IDENTIFIER );", 14, 0, self.input)

                    raise nvae

                if alt14 == 1:
                    # C.g:154:4: struct_or_union ( IDENTIFIER )? '{' struct_declaration_list '}'
                    self.following.append(self.FOLLOW_struct_or_union_in_struct_or_union_specifier439)
                    self.struct_or_union()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:154:20: ( IDENTIFIER )?
                    alt13 = 2
                    LA13_0 = self.input.LA(1)

                    if (LA13_0 == IDENTIFIER) :
                        alt13 = 1
                    if alt13 == 1:
                        # C.g:0:0: IDENTIFIER
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_struct_or_union_specifier441)
                        if self.failed:
                            return 



                    self.match(self.input, 40, self.FOLLOW_40_in_struct_or_union_specifier444)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_struct_declaration_list_in_struct_or_union_specifier446)
                    self.struct_declaration_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 41, self.FOLLOW_41_in_struct_or_union_specifier448)
                    if self.failed:
                        return 


                elif alt14 == 2:
                    # C.g:155:4: struct_or_union IDENTIFIER
                    self.following.append(self.FOLLOW_struct_or_union_in_struct_or_union_specifier453)
                    self.struct_or_union()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_struct_or_union_specifier455)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 11, struct_or_union_specifier_StartIndex)

            self.Symbols_stack.pop()

            pass

        return 

    # $ANTLR end struct_or_union_specifier


    # $ANTLR start struct_or_union
    # C.g:158:1: struct_or_union : ( 'struct' | 'union' );
    def struct_or_union(self, ):

        struct_or_union_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 12):
                    return 

                # C.g:159:2: ( 'struct' | 'union' )
                # C.g:
                if (42 <= self.input.LA(1) <= 43):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_struct_or_union0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 12, struct_or_union_StartIndex)

            pass

        return 

    # $ANTLR end struct_or_union


    # $ANTLR start struct_declaration_list
    # C.g:163:1: struct_declaration_list : ( struct_declaration )+ ;
    def struct_declaration_list(self, ):

        struct_declaration_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 13):
                    return 

                # C.g:164:2: ( ( struct_declaration )+ )
                # C.g:164:4: ( struct_declaration )+
                # C.g:164:4: ( struct_declaration )+
                cnt15 = 0
                while True: #loop15
                    alt15 = 2
                    LA15_0 = self.input.LA(1)

                    if (LA15_0 == IDENTIFIER or (31 <= LA15_0 <= 39) or (42 <= LA15_0 <= 43) or (45 <= LA15_0 <= 47)) :
                        alt15 = 1


                    if alt15 == 1:
                        # C.g:0:0: struct_declaration
                        self.following.append(self.FOLLOW_struct_declaration_in_struct_declaration_list482)
                        self.struct_declaration()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt15 >= 1:
                            break #loop15

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(15, self.input)
                        raise eee

                    cnt15 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 13, struct_declaration_list_StartIndex)

            pass

        return 

    # $ANTLR end struct_declaration_list


    # $ANTLR start struct_declaration
    # C.g:167:1: struct_declaration : specifier_qualifier_list struct_declarator_list ';' ;
    def struct_declaration(self, ):

        struct_declaration_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 14):
                    return 

                # C.g:168:2: ( specifier_qualifier_list struct_declarator_list ';' )
                # C.g:168:4: specifier_qualifier_list struct_declarator_list ';'
                self.following.append(self.FOLLOW_specifier_qualifier_list_in_struct_declaration494)
                self.specifier_qualifier_list()
                self.following.pop()
                if self.failed:
                    return 
                self.following.append(self.FOLLOW_struct_declarator_list_in_struct_declaration496)
                self.struct_declarator_list()
                self.following.pop()
                if self.failed:
                    return 
                self.match(self.input, 24, self.FOLLOW_24_in_struct_declaration498)
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 14, struct_declaration_StartIndex)

            pass

        return 

    # $ANTLR end struct_declaration


    # $ANTLR start specifier_qualifier_list
    # C.g:171:1: specifier_qualifier_list : ( type_qualifier | type_specifier )+ ;
    def specifier_qualifier_list(self, ):

        specifier_qualifier_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 15):
                    return 

                # C.g:172:2: ( ( type_qualifier | type_specifier )+ )
                # C.g:172:4: ( type_qualifier | type_specifier )+
                # C.g:172:4: ( type_qualifier | type_specifier )+
                cnt16 = 0
                while True: #loop16
                    alt16 = 3
                    LA16 = self.input.LA(1)
                    if LA16 == IDENTIFIER:
                        LA16 = self.input.LA(2)
                        if LA16 == IDENTIFIER or LA16 == 31 or LA16 == 32 or LA16 == 33 or LA16 == 34 or LA16 == 35 or LA16 == 36 or LA16 == 37 or LA16 == 38 or LA16 == 39 or LA16 == 42 or LA16 == 43 or LA16 == 45 or LA16 == 46 or LA16 == 47 or LA16 == 49 or LA16 == 52:
                            alt16 = 2
                        elif LA16 == 48:
                            LA16_21 = self.input.LA(3)

                            if ((self.synpred35() and self.isTypeName(self.input.LT(1).text))) :
                                alt16 = 2


                        elif LA16 == 44:
                            LA16_22 = self.input.LA(3)

                            if ((self.synpred35() and self.isTypeName(self.input.LT(1).text))) :
                                alt16 = 2


                        elif LA16 == 50:
                            LA16_23 = self.input.LA(3)

                            if ((self.synpred35() and self.isTypeName(self.input.LT(1).text))) :
                                alt16 = 2



                    elif LA16 == 46 or LA16 == 47:
                        alt16 = 1
                    elif LA16 == 31 or LA16 == 32 or LA16 == 33 or LA16 == 34 or LA16 == 35 or LA16 == 36 or LA16 == 37 or LA16 == 38 or LA16 == 39 or LA16 == 42 or LA16 == 43 or LA16 == 45:
                        alt16 = 2

                    if alt16 == 1:
                        # C.g:172:6: type_qualifier
                        self.following.append(self.FOLLOW_type_qualifier_in_specifier_qualifier_list511)
                        self.type_qualifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt16 == 2:
                        # C.g:172:23: type_specifier
                        self.following.append(self.FOLLOW_type_specifier_in_specifier_qualifier_list515)
                        self.type_specifier()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt16 >= 1:
                            break #loop16

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(16, self.input)
                        raise eee

                    cnt16 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 15, specifier_qualifier_list_StartIndex)

            pass

        return 

    # $ANTLR end specifier_qualifier_list


    # $ANTLR start struct_declarator_list
    # C.g:175:1: struct_declarator_list : struct_declarator ( ',' struct_declarator )* ;
    def struct_declarator_list(self, ):

        struct_declarator_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 16):
                    return 

                # C.g:176:2: ( struct_declarator ( ',' struct_declarator )* )
                # C.g:176:4: struct_declarator ( ',' struct_declarator )*
                self.following.append(self.FOLLOW_struct_declarator_in_struct_declarator_list529)
                self.struct_declarator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:176:22: ( ',' struct_declarator )*
                while True: #loop17
                    alt17 = 2
                    LA17_0 = self.input.LA(1)

                    if (LA17_0 == 25) :
                        alt17 = 1


                    if alt17 == 1:
                        # C.g:176:23: ',' struct_declarator
                        self.match(self.input, 25, self.FOLLOW_25_in_struct_declarator_list532)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_struct_declarator_in_struct_declarator_list534)
                        self.struct_declarator()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop17






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 16, struct_declarator_list_StartIndex)

            pass

        return 

    # $ANTLR end struct_declarator_list


    # $ANTLR start struct_declarator
    # C.g:179:1: struct_declarator : ( declarator ( ':' constant_expression )? | ':' constant_expression );
    def struct_declarator(self, ):

        struct_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 17):
                    return 

                # C.g:180:2: ( declarator ( ':' constant_expression )? | ':' constant_expression )
                alt19 = 2
                LA19_0 = self.input.LA(1)

                if (LA19_0 == IDENTIFIER or LA19_0 == 48 or LA19_0 == 52) :
                    alt19 = 1
                elif (LA19_0 == 44) :
                    alt19 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("179:1: struct_declarator : ( declarator ( ':' constant_expression )? | ':' constant_expression );", 19, 0, self.input)

                    raise nvae

                if alt19 == 1:
                    # C.g:180:4: declarator ( ':' constant_expression )?
                    self.following.append(self.FOLLOW_declarator_in_struct_declarator547)
                    self.declarator()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:180:15: ( ':' constant_expression )?
                    alt18 = 2
                    LA18_0 = self.input.LA(1)

                    if (LA18_0 == 44) :
                        alt18 = 1
                    if alt18 == 1:
                        # C.g:180:16: ':' constant_expression
                        self.match(self.input, 44, self.FOLLOW_44_in_struct_declarator550)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_constant_expression_in_struct_declarator552)
                        self.constant_expression()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt19 == 2:
                    # C.g:181:4: ':' constant_expression
                    self.match(self.input, 44, self.FOLLOW_44_in_struct_declarator559)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_struct_declarator561)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 17, struct_declarator_StartIndex)

            pass

        return 

    # $ANTLR end struct_declarator


    # $ANTLR start enum_specifier
    # C.g:184:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );
    def enum_specifier(self, ):

        enum_specifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 18):
                    return 

                # C.g:186:2: ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER )
                alt20 = 3
                LA20_0 = self.input.LA(1)

                if (LA20_0 == 45) :
                    LA20_1 = self.input.LA(2)

                    if (LA20_1 == 40) :
                        alt20 = 1
                    elif (LA20_1 == IDENTIFIER) :
                        LA20_3 = self.input.LA(3)

                        if (LA20_3 == 40) :
                            alt20 = 2
                        elif (LA20_3 == EOF or LA20_3 == IDENTIFIER or (24 <= LA20_3 <= 25) or (27 <= LA20_3 <= 39) or (42 <= LA20_3 <= 50) or LA20_3 == 52) :
                            alt20 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("184:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );", 20, 3, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("184:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );", 20, 1, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("184:1: enum_specifier options {k=3; } : ( 'enum' '{' enumerator_list '}' | 'enum' IDENTIFIER '{' enumerator_list '}' | 'enum' IDENTIFIER );", 20, 0, self.input)

                    raise nvae

                if alt20 == 1:
                    # C.g:186:4: 'enum' '{' enumerator_list '}'
                    self.match(self.input, 45, self.FOLLOW_45_in_enum_specifier579)
                    if self.failed:
                        return 
                    self.match(self.input, 40, self.FOLLOW_40_in_enum_specifier581)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_enumerator_list_in_enum_specifier583)
                    self.enumerator_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 41, self.FOLLOW_41_in_enum_specifier585)
                    if self.failed:
                        return 


                elif alt20 == 2:
                    # C.g:187:4: 'enum' IDENTIFIER '{' enumerator_list '}'
                    self.match(self.input, 45, self.FOLLOW_45_in_enum_specifier590)
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_enum_specifier592)
                    if self.failed:
                        return 
                    self.match(self.input, 40, self.FOLLOW_40_in_enum_specifier594)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_enumerator_list_in_enum_specifier596)
                    self.enumerator_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 41, self.FOLLOW_41_in_enum_specifier598)
                    if self.failed:
                        return 


                elif alt20 == 3:
                    # C.g:188:4: 'enum' IDENTIFIER
                    self.match(self.input, 45, self.FOLLOW_45_in_enum_specifier603)
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_enum_specifier605)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 18, enum_specifier_StartIndex)

            pass

        return 

    # $ANTLR end enum_specifier


    # $ANTLR start enumerator_list
    # C.g:191:1: enumerator_list : enumerator ( ',' enumerator )* ;
    def enumerator_list(self, ):

        enumerator_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 19):
                    return 

                # C.g:192:2: ( enumerator ( ',' enumerator )* )
                # C.g:192:4: enumerator ( ',' enumerator )*
                self.following.append(self.FOLLOW_enumerator_in_enumerator_list616)
                self.enumerator()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:192:15: ( ',' enumerator )*
                while True: #loop21
                    alt21 = 2
                    LA21_0 = self.input.LA(1)

                    if (LA21_0 == 25) :
                        alt21 = 1


                    if alt21 == 1:
                        # C.g:192:16: ',' enumerator
                        self.match(self.input, 25, self.FOLLOW_25_in_enumerator_list619)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_enumerator_in_enumerator_list621)
                        self.enumerator()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop21






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 19, enumerator_list_StartIndex)

            pass

        return 

    # $ANTLR end enumerator_list


    # $ANTLR start enumerator
    # C.g:195:1: enumerator : IDENTIFIER ( '=' constant_expression )? ;
    def enumerator(self, ):

        enumerator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 20):
                    return 

                # C.g:196:2: ( IDENTIFIER ( '=' constant_expression )? )
                # C.g:196:4: IDENTIFIER ( '=' constant_expression )?
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_enumerator634)
                if self.failed:
                    return 
                # C.g:196:15: ( '=' constant_expression )?
                alt22 = 2
                LA22_0 = self.input.LA(1)

                if (LA22_0 == 26) :
                    alt22 = 1
                if alt22 == 1:
                    # C.g:196:16: '=' constant_expression
                    self.match(self.input, 26, self.FOLLOW_26_in_enumerator637)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_enumerator639)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 20, enumerator_StartIndex)

            pass

        return 

    # $ANTLR end enumerator


    # $ANTLR start type_qualifier
    # C.g:199:1: type_qualifier : ( 'const' | 'volatile' );
    def type_qualifier(self, ):

        type_qualifier_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 21):
                    return 

                # C.g:200:2: ( 'const' | 'volatile' )
                # C.g:
                if (46 <= self.input.LA(1) <= 47):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_type_qualifier0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 21, type_qualifier_StartIndex)

            pass

        return 

    # $ANTLR end type_qualifier


    # $ANTLR start declarator
    # C.g:204:1: declarator : ( ( pointer )? direct_declarator | pointer );
    def declarator(self, ):

        declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 22):
                    return 

                # C.g:205:2: ( ( pointer )? direct_declarator | pointer )
                alt24 = 2
                LA24_0 = self.input.LA(1)

                if (LA24_0 == 52) :
                    LA24_1 = self.input.LA(2)

                    if (self.synpred45()) :
                        alt24 = 1
                    elif (True) :
                        alt24 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("204:1: declarator : ( ( pointer )? direct_declarator | pointer );", 24, 1, self.input)

                        raise nvae

                elif (LA24_0 == IDENTIFIER or LA24_0 == 48) :
                    alt24 = 1
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("204:1: declarator : ( ( pointer )? direct_declarator | pointer );", 24, 0, self.input)

                    raise nvae

                if alt24 == 1:
                    # C.g:205:4: ( pointer )? direct_declarator
                    # C.g:205:4: ( pointer )?
                    alt23 = 2
                    LA23_0 = self.input.LA(1)

                    if (LA23_0 == 52) :
                        alt23 = 1
                    if alt23 == 1:
                        # C.g:0:0: pointer
                        self.following.append(self.FOLLOW_pointer_in_declarator668)
                        self.pointer()
                        self.following.pop()
                        if self.failed:
                            return 



                    self.following.append(self.FOLLOW_direct_declarator_in_declarator671)
                    self.direct_declarator()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt24 == 2:
                    # C.g:206:4: pointer
                    self.following.append(self.FOLLOW_pointer_in_declarator676)
                    self.pointer()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 22, declarator_StartIndex)

            pass

        return 

    # $ANTLR end declarator


    # $ANTLR start direct_declarator
    # C.g:209:1: direct_declarator : ( IDENTIFIER | '(' declarator ')' ) ( declarator_suffix )* ;
    def direct_declarator(self, ):

        direct_declarator_StartIndex = self.input.index()
        IDENTIFIER1 = None

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 23):
                    return 

                # C.g:210:2: ( ( IDENTIFIER | '(' declarator ')' ) ( declarator_suffix )* )
                # C.g:210:6: ( IDENTIFIER | '(' declarator ')' ) ( declarator_suffix )*
                # C.g:210:6: ( IDENTIFIER | '(' declarator ')' )
                alt25 = 2
                LA25_0 = self.input.LA(1)

                if (LA25_0 == IDENTIFIER) :
                    alt25 = 1
                elif (LA25_0 == 48) :
                    alt25 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("210:6: ( IDENTIFIER | '(' declarator ')' )", 25, 0, self.input)

                    raise nvae

                if alt25 == 1:
                    # C.g:210:8: IDENTIFIER
                    IDENTIFIER1 = self.input.LT(1)
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_direct_declarator691)
                    if self.failed:
                        return 
                    if self.backtracking == 0:
                            
                        if len(self.declaration_stack) > 0 and self.declaration_stack[-1].isTypedef:
                        	self.Symbols_stack[-1].types.add(IDENTIFIER1.text)
                        	print "define type "+IDENTIFIER1.text
                        			



                elif alt25 == 2:
                    # C.g:216:5: '(' declarator ')'
                    self.match(self.input, 48, self.FOLLOW_48_in_direct_declarator702)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_declarator_in_direct_declarator704)
                    self.declarator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_direct_declarator706)
                    if self.failed:
                        return 



                # C.g:218:9: ( declarator_suffix )*
                while True: #loop26
                    alt26 = 2
                    LA26_0 = self.input.LA(1)

                    if (LA26_0 == 48) :
                        LA26 = self.input.LA(2)
                        if LA26 == 49:
                            LA26_26 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 27 or LA26 == 28 or LA26 == 29 or LA26 == 30:
                            LA26_27 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 31:
                            LA26_28 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 32:
                            LA26_29 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 33:
                            LA26_30 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 34:
                            LA26_31 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 35:
                            LA26_32 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 36:
                            LA26_33 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 37:
                            LA26_34 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 38:
                            LA26_35 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 39:
                            LA26_36 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 42 or LA26 == 43:
                            LA26_37 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 45:
                            LA26_38 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == IDENTIFIER:
                            LA26_39 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 46 or LA26 == 47:
                            LA26_40 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1



                    elif (LA26_0 == 50) :
                        LA26 = self.input.LA(2)
                        if LA26 == 51:
                            LA26_44 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 48:
                            LA26_45 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == IDENTIFIER:
                            LA26_46 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == HEX_LITERAL or LA26 == OCTAL_LITERAL or LA26 == DECIMAL_LITERAL or LA26 == CHARACTER_LITERAL or LA26 == STRING_LITERAL or LA26 == FLOATING_POINT_LITERAL:
                            LA26_47 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 58:
                            LA26_48 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 59:
                            LA26_49 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 52 or LA26 == 54 or LA26 == 55 or LA26 == 63 or LA26 == 64 or LA26 == 65:
                            LA26_50 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1


                        elif LA26 == 60:
                            LA26_51 = self.input.LA(3)

                            if (self.synpred47()) :
                                alt26 = 1





                    if alt26 == 1:
                        # C.g:0:0: declarator_suffix
                        self.following.append(self.FOLLOW_declarator_suffix_in_direct_declarator720)
                        self.declarator_suffix()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop26






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 23, direct_declarator_StartIndex)

            pass

        return 

    # $ANTLR end direct_declarator


    # $ANTLR start declarator_suffix
    # C.g:221:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );
    def declarator_suffix(self, ):

        declarator_suffix_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 24):
                    return 

                # C.g:222:2: ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' )
                alt27 = 5
                LA27_0 = self.input.LA(1)

                if (LA27_0 == 50) :
                    LA27_1 = self.input.LA(2)

                    if (LA27_1 == 51) :
                        alt27 = 2
                    elif ((IDENTIFIER <= LA27_1 <= FLOATING_POINT_LITERAL) or LA27_1 == 48 or LA27_1 == 52 or (54 <= LA27_1 <= 55) or (58 <= LA27_1 <= 60) or (63 <= LA27_1 <= 65)) :
                        alt27 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("221:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 27, 1, self.input)

                        raise nvae

                elif (LA27_0 == 48) :
                    LA27 = self.input.LA(2)
                    if LA27 == 49:
                        alt27 = 5
                    elif LA27 == 27 or LA27 == 28 or LA27 == 29 or LA27 == 30 or LA27 == 31 or LA27 == 32 or LA27 == 33 or LA27 == 34 or LA27 == 35 or LA27 == 36 or LA27 == 37 or LA27 == 38 or LA27 == 39 or LA27 == 42 or LA27 == 43 or LA27 == 45 or LA27 == 46 or LA27 == 47:
                        alt27 = 3
                    elif LA27 == IDENTIFIER:
                        LA27_24 = self.input.LA(3)

                        if (self.synpred50()) :
                            alt27 = 3
                        elif (self.synpred51()) :
                            alt27 = 4
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("221:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 27, 24, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("221:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 27, 2, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("221:1: declarator_suffix : ( '[' constant_expression ']' | '[' ']' | '(' parameter_type_list ')' | '(' identifier_list ')' | '(' ')' );", 27, 0, self.input)

                    raise nvae

                if alt27 == 1:
                    # C.g:222:6: '[' constant_expression ']'
                    self.match(self.input, 50, self.FOLLOW_50_in_declarator_suffix734)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_declarator_suffix736)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_declarator_suffix738)
                    if self.failed:
                        return 


                elif alt27 == 2:
                    # C.g:223:9: '[' ']'
                    self.match(self.input, 50, self.FOLLOW_50_in_declarator_suffix748)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_declarator_suffix750)
                    if self.failed:
                        return 


                elif alt27 == 3:
                    # C.g:224:9: '(' parameter_type_list ')'
                    self.match(self.input, 48, self.FOLLOW_48_in_declarator_suffix760)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_parameter_type_list_in_declarator_suffix762)
                    self.parameter_type_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_declarator_suffix764)
                    if self.failed:
                        return 


                elif alt27 == 4:
                    # C.g:225:9: '(' identifier_list ')'
                    self.match(self.input, 48, self.FOLLOW_48_in_declarator_suffix774)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_identifier_list_in_declarator_suffix776)
                    self.identifier_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_declarator_suffix778)
                    if self.failed:
                        return 


                elif alt27 == 5:
                    # C.g:226:9: '(' ')'
                    self.match(self.input, 48, self.FOLLOW_48_in_declarator_suffix788)
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_declarator_suffix790)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 24, declarator_suffix_StartIndex)

            pass

        return 

    # $ANTLR end declarator_suffix


    # $ANTLR start pointer
    # C.g:229:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );
    def pointer(self, ):

        pointer_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 25):
                    return 

                # C.g:230:2: ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' )
                alt30 = 3
                LA30_0 = self.input.LA(1)

                if (LA30_0 == 52) :
                    LA30 = self.input.LA(2)
                    if LA30 == 52:
                        LA30_2 = self.input.LA(3)

                        if (self.synpred55()) :
                            alt30 = 2
                        elif (True) :
                            alt30 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("229:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );", 30, 2, self.input)

                            raise nvae

                    elif LA30 == EOF or LA30 == IDENTIFIER or LA30 == 23 or LA30 == 24 or LA30 == 25 or LA30 == 26 or LA30 == 27 or LA30 == 28 or LA30 == 29 or LA30 == 30 or LA30 == 31 or LA30 == 32 or LA30 == 33 or LA30 == 34 or LA30 == 35 or LA30 == 36 or LA30 == 37 or LA30 == 38 or LA30 == 39 or LA30 == 40 or LA30 == 42 or LA30 == 43 or LA30 == 44 or LA30 == 45 or LA30 == 48 or LA30 == 49 or LA30 == 50:
                        alt30 = 3
                    elif LA30 == 46 or LA30 == 47:
                        LA30_18 = self.input.LA(3)

                        if (self.synpred54()) :
                            alt30 = 1
                        elif (True) :
                            alt30 = 3
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("229:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );", 30, 18, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("229:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );", 30, 1, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("229:1: pointer : ( '*' ( type_qualifier )+ ( pointer )? | '*' pointer | '*' );", 30, 0, self.input)

                    raise nvae

                if alt30 == 1:
                    # C.g:230:4: '*' ( type_qualifier )+ ( pointer )?
                    self.match(self.input, 52, self.FOLLOW_52_in_pointer801)
                    if self.failed:
                        return 
                    # C.g:230:8: ( type_qualifier )+
                    cnt28 = 0
                    while True: #loop28
                        alt28 = 2
                        LA28_0 = self.input.LA(1)

                        if ((46 <= LA28_0 <= 47)) :
                            LA28_17 = self.input.LA(2)

                            if (self.synpred52()) :
                                alt28 = 1




                        if alt28 == 1:
                            # C.g:0:0: type_qualifier
                            self.following.append(self.FOLLOW_type_qualifier_in_pointer803)
                            self.type_qualifier()
                            self.following.pop()
                            if self.failed:
                                return 


                        else:
                            if cnt28 >= 1:
                                break #loop28

                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            eee = EarlyExitException(28, self.input)
                            raise eee

                        cnt28 += 1


                    # C.g:230:24: ( pointer )?
                    alt29 = 2
                    LA29_0 = self.input.LA(1)

                    if (LA29_0 == 52) :
                        LA29_1 = self.input.LA(2)

                        if (self.synpred53()) :
                            alt29 = 1
                    if alt29 == 1:
                        # C.g:0:0: pointer
                        self.following.append(self.FOLLOW_pointer_in_pointer806)
                        self.pointer()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt30 == 2:
                    # C.g:231:4: '*' pointer
                    self.match(self.input, 52, self.FOLLOW_52_in_pointer812)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_pointer_in_pointer814)
                    self.pointer()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt30 == 3:
                    # C.g:232:4: '*'
                    self.match(self.input, 52, self.FOLLOW_52_in_pointer819)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 25, pointer_StartIndex)

            pass

        return 

    # $ANTLR end pointer


    # $ANTLR start parameter_type_list
    # C.g:235:1: parameter_type_list : parameter_list ( ',' '...' )? ;
    def parameter_type_list(self, ):

        parameter_type_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 26):
                    return 

                # C.g:236:2: ( parameter_list ( ',' '...' )? )
                # C.g:236:4: parameter_list ( ',' '...' )?
                self.following.append(self.FOLLOW_parameter_list_in_parameter_type_list830)
                self.parameter_list()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:236:19: ( ',' '...' )?
                alt31 = 2
                LA31_0 = self.input.LA(1)

                if (LA31_0 == 25) :
                    alt31 = 1
                if alt31 == 1:
                    # C.g:236:20: ',' '...'
                    self.match(self.input, 25, self.FOLLOW_25_in_parameter_type_list833)
                    if self.failed:
                        return 
                    self.match(self.input, 53, self.FOLLOW_53_in_parameter_type_list835)
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 26, parameter_type_list_StartIndex)

            pass

        return 

    # $ANTLR end parameter_type_list


    # $ANTLR start parameter_list
    # C.g:239:1: parameter_list : parameter_declaration ( ',' parameter_declaration )* ;
    def parameter_list(self, ):

        parameter_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 27):
                    return 

                # C.g:240:2: ( parameter_declaration ( ',' parameter_declaration )* )
                # C.g:240:4: parameter_declaration ( ',' parameter_declaration )*
                self.following.append(self.FOLLOW_parameter_declaration_in_parameter_list848)
                self.parameter_declaration()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:240:26: ( ',' parameter_declaration )*
                while True: #loop32
                    alt32 = 2
                    LA32_0 = self.input.LA(1)

                    if (LA32_0 == 25) :
                        LA32_1 = self.input.LA(2)

                        if (LA32_1 == IDENTIFIER or (27 <= LA32_1 <= 39) or (42 <= LA32_1 <= 43) or (45 <= LA32_1 <= 47)) :
                            alt32 = 1




                    if alt32 == 1:
                        # C.g:240:27: ',' parameter_declaration
                        self.match(self.input, 25, self.FOLLOW_25_in_parameter_list851)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_parameter_declaration_in_parameter_list853)
                        self.parameter_declaration()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop32






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 27, parameter_list_StartIndex)

            pass

        return 

    # $ANTLR end parameter_list


    # $ANTLR start parameter_declaration
    # C.g:243:1: parameter_declaration : declaration_specifiers ( declarator | abstract_declarator )* ;
    def parameter_declaration(self, ):

        parameter_declaration_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 28):
                    return 

                # C.g:244:2: ( declaration_specifiers ( declarator | abstract_declarator )* )
                # C.g:244:4: declaration_specifiers ( declarator | abstract_declarator )*
                self.following.append(self.FOLLOW_declaration_specifiers_in_parameter_declaration866)
                self.declaration_specifiers()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:244:27: ( declarator | abstract_declarator )*
                while True: #loop33
                    alt33 = 3
                    LA33 = self.input.LA(1)
                    if LA33 == 52:
                        LA33_4 = self.input.LA(2)

                        if (self.synpred58()) :
                            alt33 = 1
                        elif (self.synpred59()) :
                            alt33 = 2


                    elif LA33 == IDENTIFIER:
                        alt33 = 1
                    elif LA33 == 48:
                        LA33 = self.input.LA(2)
                        if LA33 == 27 or LA33 == 28 or LA33 == 29 or LA33 == 30 or LA33 == 31 or LA33 == 32 or LA33 == 33 or LA33 == 34 or LA33 == 35 or LA33 == 36 or LA33 == 37 or LA33 == 38 or LA33 == 39 or LA33 == 42 or LA33 == 43 or LA33 == 45 or LA33 == 46 or LA33 == 47 or LA33 == 49 or LA33 == 50:
                            alt33 = 2
                        elif LA33 == IDENTIFIER:
                            LA33_29 = self.input.LA(3)

                            if (self.synpred58()) :
                                alt33 = 1
                            elif (self.synpred59()) :
                                alt33 = 2


                        elif LA33 == 52:
                            LA33_31 = self.input.LA(3)

                            if (self.synpred58()) :
                                alt33 = 1
                            elif (self.synpred59()) :
                                alt33 = 2


                        elif LA33 == 48:
                            LA33_32 = self.input.LA(3)

                            if (self.synpred58()) :
                                alt33 = 1
                            elif (self.synpred59()) :
                                alt33 = 2



                    elif LA33 == 50:
                        alt33 = 2

                    if alt33 == 1:
                        # C.g:244:28: declarator
                        self.following.append(self.FOLLOW_declarator_in_parameter_declaration869)
                        self.declarator()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt33 == 2:
                        # C.g:244:39: abstract_declarator
                        self.following.append(self.FOLLOW_abstract_declarator_in_parameter_declaration871)
                        self.abstract_declarator()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop33






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 28, parameter_declaration_StartIndex)

            pass

        return 

    # $ANTLR end parameter_declaration


    # $ANTLR start identifier_list
    # C.g:247:1: identifier_list : IDENTIFIER ( ',' IDENTIFIER )* ;
    def identifier_list(self, ):

        identifier_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 29):
                    return 

                # C.g:248:2: ( IDENTIFIER ( ',' IDENTIFIER )* )
                # C.g:248:4: IDENTIFIER ( ',' IDENTIFIER )*
                self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_identifier_list884)
                if self.failed:
                    return 
                # C.g:248:15: ( ',' IDENTIFIER )*
                while True: #loop34
                    alt34 = 2
                    LA34_0 = self.input.LA(1)

                    if (LA34_0 == 25) :
                        alt34 = 1


                    if alt34 == 1:
                        # C.g:248:16: ',' IDENTIFIER
                        self.match(self.input, 25, self.FOLLOW_25_in_identifier_list887)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_identifier_list889)
                        if self.failed:
                            return 


                    else:
                        break #loop34






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 29, identifier_list_StartIndex)

            pass

        return 

    # $ANTLR end identifier_list


    # $ANTLR start type_name
    # C.g:251:1: type_name : specifier_qualifier_list ( abstract_declarator )? ;
    def type_name(self, ):

        type_name_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 30):
                    return 

                # C.g:252:2: ( specifier_qualifier_list ( abstract_declarator )? )
                # C.g:252:4: specifier_qualifier_list ( abstract_declarator )?
                self.following.append(self.FOLLOW_specifier_qualifier_list_in_type_name902)
                self.specifier_qualifier_list()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:252:29: ( abstract_declarator )?
                alt35 = 2
                LA35_0 = self.input.LA(1)

                if (LA35_0 == 48 or LA35_0 == 50 or LA35_0 == 52) :
                    alt35 = 1
                if alt35 == 1:
                    # C.g:0:0: abstract_declarator
                    self.following.append(self.FOLLOW_abstract_declarator_in_type_name904)
                    self.abstract_declarator()
                    self.following.pop()
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 30, type_name_StartIndex)

            pass

        return 

    # $ANTLR end type_name


    # $ANTLR start abstract_declarator
    # C.g:255:1: abstract_declarator : ( pointer ( direct_abstract_declarator )? | direct_abstract_declarator );
    def abstract_declarator(self, ):

        abstract_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 31):
                    return 

                # C.g:256:2: ( pointer ( direct_abstract_declarator )? | direct_abstract_declarator )
                alt37 = 2
                LA37_0 = self.input.LA(1)

                if (LA37_0 == 52) :
                    alt37 = 1
                elif (LA37_0 == 48 or LA37_0 == 50) :
                    alt37 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("255:1: abstract_declarator : ( pointer ( direct_abstract_declarator )? | direct_abstract_declarator );", 37, 0, self.input)

                    raise nvae

                if alt37 == 1:
                    # C.g:256:4: pointer ( direct_abstract_declarator )?
                    self.following.append(self.FOLLOW_pointer_in_abstract_declarator916)
                    self.pointer()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:256:12: ( direct_abstract_declarator )?
                    alt36 = 2
                    LA36_0 = self.input.LA(1)

                    if (LA36_0 == 48) :
                        LA36 = self.input.LA(2)
                        if LA36 == 49:
                            LA36_8 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 27 or LA36 == 28 or LA36 == 29 or LA36 == 30:
                            LA36_9 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 31:
                            LA36_10 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 32:
                            LA36_11 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 33:
                            LA36_12 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 34:
                            LA36_13 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 35:
                            LA36_14 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 36:
                            LA36_15 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 37:
                            LA36_16 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 38:
                            LA36_17 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 39:
                            LA36_18 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 42 or LA36 == 43:
                            LA36_19 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 45:
                            LA36_20 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == IDENTIFIER:
                            LA36_21 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 46 or LA36 == 47:
                            LA36_22 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 52:
                            LA36_23 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 48:
                            LA36_24 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 50:
                            LA36_25 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                    elif (LA36_0 == 50) :
                        LA36 = self.input.LA(2)
                        if LA36 == 51:
                            LA36_26 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 48:
                            LA36_27 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == IDENTIFIER:
                            LA36_28 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == HEX_LITERAL or LA36 == OCTAL_LITERAL or LA36 == DECIMAL_LITERAL or LA36 == CHARACTER_LITERAL or LA36 == STRING_LITERAL or LA36 == FLOATING_POINT_LITERAL:
                            LA36_29 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 58:
                            LA36_30 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 59:
                            LA36_31 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 52 or LA36 == 54 or LA36 == 55 or LA36 == 63 or LA36 == 64 or LA36 == 65:
                            LA36_32 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                        elif LA36 == 60:
                            LA36_33 = self.input.LA(3)

                            if (self.synpred62()) :
                                alt36 = 1
                    if alt36 == 1:
                        # C.g:0:0: direct_abstract_declarator
                        self.following.append(self.FOLLOW_direct_abstract_declarator_in_abstract_declarator918)
                        self.direct_abstract_declarator()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt37 == 2:
                    # C.g:257:4: direct_abstract_declarator
                    self.following.append(self.FOLLOW_direct_abstract_declarator_in_abstract_declarator924)
                    self.direct_abstract_declarator()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 31, abstract_declarator_StartIndex)

            pass

        return 

    # $ANTLR end abstract_declarator


    # $ANTLR start direct_abstract_declarator
    # C.g:260:1: direct_abstract_declarator : ( '(' abstract_declarator ')' | abstract_declarator_suffix ) ( abstract_declarator_suffix )* ;
    def direct_abstract_declarator(self, ):

        direct_abstract_declarator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 32):
                    return 

                # C.g:261:2: ( ( '(' abstract_declarator ')' | abstract_declarator_suffix ) ( abstract_declarator_suffix )* )
                # C.g:261:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix ) ( abstract_declarator_suffix )*
                # C.g:261:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix )
                alt38 = 2
                LA38_0 = self.input.LA(1)

                if (LA38_0 == 48) :
                    LA38_1 = self.input.LA(2)

                    if (LA38_1 == IDENTIFIER or (27 <= LA38_1 <= 39) or (42 <= LA38_1 <= 43) or (45 <= LA38_1 <= 47) or LA38_1 == 49) :
                        alt38 = 2
                    elif (LA38_1 == 48 or LA38_1 == 50 or LA38_1 == 52) :
                        alt38 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("261:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix )", 38, 1, self.input)

                        raise nvae

                elif (LA38_0 == 50) :
                    alt38 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("261:4: ( '(' abstract_declarator ')' | abstract_declarator_suffix )", 38, 0, self.input)

                    raise nvae

                if alt38 == 1:
                    # C.g:261:6: '(' abstract_declarator ')'
                    self.match(self.input, 48, self.FOLLOW_48_in_direct_abstract_declarator937)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_abstract_declarator_in_direct_abstract_declarator939)
                    self.abstract_declarator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_direct_abstract_declarator941)
                    if self.failed:
                        return 


                elif alt38 == 2:
                    # C.g:261:36: abstract_declarator_suffix
                    self.following.append(self.FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator945)
                    self.abstract_declarator_suffix()
                    self.following.pop()
                    if self.failed:
                        return 



                # C.g:261:65: ( abstract_declarator_suffix )*
                while True: #loop39
                    alt39 = 2
                    LA39_0 = self.input.LA(1)

                    if (LA39_0 == 48) :
                        LA39 = self.input.LA(2)
                        if LA39 == 49:
                            LA39_8 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 27 or LA39 == 28 or LA39 == 29 or LA39 == 30:
                            LA39_9 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 31:
                            LA39_10 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 32:
                            LA39_11 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 33:
                            LA39_12 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 34:
                            LA39_13 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 35:
                            LA39_14 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 36:
                            LA39_15 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 37:
                            LA39_16 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 38:
                            LA39_17 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 39:
                            LA39_18 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 42 or LA39 == 43:
                            LA39_19 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 45:
                            LA39_20 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == IDENTIFIER:
                            LA39_21 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 46 or LA39 == 47:
                            LA39_22 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1



                    elif (LA39_0 == 50) :
                        LA39 = self.input.LA(2)
                        if LA39 == 51:
                            LA39_26 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 48:
                            LA39_27 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == IDENTIFIER:
                            LA39_28 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == HEX_LITERAL or LA39 == OCTAL_LITERAL or LA39 == DECIMAL_LITERAL or LA39 == CHARACTER_LITERAL or LA39 == STRING_LITERAL or LA39 == FLOATING_POINT_LITERAL:
                            LA39_29 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 58:
                            LA39_30 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 59:
                            LA39_31 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 52 or LA39 == 54 or LA39 == 55 or LA39 == 63 or LA39 == 64 or LA39 == 65:
                            LA39_32 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1


                        elif LA39 == 60:
                            LA39_33 = self.input.LA(3)

                            if (self.synpred65()) :
                                alt39 = 1





                    if alt39 == 1:
                        # C.g:0:0: abstract_declarator_suffix
                        self.following.append(self.FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator949)
                        self.abstract_declarator_suffix()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop39






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 32, direct_abstract_declarator_StartIndex)

            pass

        return 

    # $ANTLR end direct_abstract_declarator


    # $ANTLR start abstract_declarator_suffix
    # C.g:264:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );
    def abstract_declarator_suffix(self, ):

        abstract_declarator_suffix_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 33):
                    return 

                # C.g:265:2: ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' )
                alt40 = 4
                LA40_0 = self.input.LA(1)

                if (LA40_0 == 50) :
                    LA40_1 = self.input.LA(2)

                    if (LA40_1 == 51) :
                        alt40 = 1
                    elif ((IDENTIFIER <= LA40_1 <= FLOATING_POINT_LITERAL) or LA40_1 == 48 or LA40_1 == 52 or (54 <= LA40_1 <= 55) or (58 <= LA40_1 <= 60) or (63 <= LA40_1 <= 65)) :
                        alt40 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("264:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );", 40, 1, self.input)

                        raise nvae

                elif (LA40_0 == 48) :
                    LA40_2 = self.input.LA(2)

                    if (LA40_2 == 49) :
                        alt40 = 3
                    elif (LA40_2 == IDENTIFIER or (27 <= LA40_2 <= 39) or (42 <= LA40_2 <= 43) or (45 <= LA40_2 <= 47)) :
                        alt40 = 4
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("264:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );", 40, 2, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("264:1: abstract_declarator_suffix : ( '[' ']' | '[' constant_expression ']' | '(' ')' | '(' parameter_type_list ')' );", 40, 0, self.input)

                    raise nvae

                if alt40 == 1:
                    # C.g:265:4: '[' ']'
                    self.match(self.input, 50, self.FOLLOW_50_in_abstract_declarator_suffix961)
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_abstract_declarator_suffix963)
                    if self.failed:
                        return 


                elif alt40 == 2:
                    # C.g:266:4: '[' constant_expression ']'
                    self.match(self.input, 50, self.FOLLOW_50_in_abstract_declarator_suffix968)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_abstract_declarator_suffix970)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 51, self.FOLLOW_51_in_abstract_declarator_suffix972)
                    if self.failed:
                        return 


                elif alt40 == 3:
                    # C.g:267:4: '(' ')'
                    self.match(self.input, 48, self.FOLLOW_48_in_abstract_declarator_suffix977)
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_abstract_declarator_suffix979)
                    if self.failed:
                        return 


                elif alt40 == 4:
                    # C.g:268:4: '(' parameter_type_list ')'
                    self.match(self.input, 48, self.FOLLOW_48_in_abstract_declarator_suffix984)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_parameter_type_list_in_abstract_declarator_suffix986)
                    self.parameter_type_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_abstract_declarator_suffix988)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 33, abstract_declarator_suffix_StartIndex)

            pass

        return 

    # $ANTLR end abstract_declarator_suffix


    # $ANTLR start initializer
    # C.g:271:1: initializer : ( assignment_expression | '{' initializer_list ( ',' )? '}' );
    def initializer(self, ):

        initializer_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 34):
                    return 

                # C.g:272:2: ( assignment_expression | '{' initializer_list ( ',' )? '}' )
                alt42 = 2
                LA42_0 = self.input.LA(1)

                if ((IDENTIFIER <= LA42_0 <= FLOATING_POINT_LITERAL) or LA42_0 == 48 or LA42_0 == 52 or (54 <= LA42_0 <= 55) or (58 <= LA42_0 <= 60) or (63 <= LA42_0 <= 65)) :
                    alt42 = 1
                elif (LA42_0 == 40) :
                    alt42 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("271:1: initializer : ( assignment_expression | '{' initializer_list ( ',' )? '}' );", 42, 0, self.input)

                    raise nvae

                if alt42 == 1:
                    # C.g:272:4: assignment_expression
                    self.following.append(self.FOLLOW_assignment_expression_in_initializer1000)
                    self.assignment_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt42 == 2:
                    # C.g:273:4: '{' initializer_list ( ',' )? '}'
                    self.match(self.input, 40, self.FOLLOW_40_in_initializer1005)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_initializer_list_in_initializer1007)
                    self.initializer_list()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:273:25: ( ',' )?
                    alt41 = 2
                    LA41_0 = self.input.LA(1)

                    if (LA41_0 == 25) :
                        alt41 = 1
                    if alt41 == 1:
                        # C.g:0:0: ','
                        self.match(self.input, 25, self.FOLLOW_25_in_initializer1009)
                        if self.failed:
                            return 



                    self.match(self.input, 41, self.FOLLOW_41_in_initializer1012)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 34, initializer_StartIndex)

            pass

        return 

    # $ANTLR end initializer


    # $ANTLR start initializer_list
    # C.g:276:1: initializer_list : initializer ( ',' initializer )* ;
    def initializer_list(self, ):

        initializer_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 35):
                    return 

                # C.g:277:2: ( initializer ( ',' initializer )* )
                # C.g:277:4: initializer ( ',' initializer )*
                self.following.append(self.FOLLOW_initializer_in_initializer_list1023)
                self.initializer()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:277:16: ( ',' initializer )*
                while True: #loop43
                    alt43 = 2
                    LA43_0 = self.input.LA(1)

                    if (LA43_0 == 25) :
                        LA43_1 = self.input.LA(2)

                        if ((IDENTIFIER <= LA43_1 <= FLOATING_POINT_LITERAL) or LA43_1 == 40 or LA43_1 == 48 or LA43_1 == 52 or (54 <= LA43_1 <= 55) or (58 <= LA43_1 <= 60) or (63 <= LA43_1 <= 65)) :
                            alt43 = 1




                    if alt43 == 1:
                        # C.g:277:17: ',' initializer
                        self.match(self.input, 25, self.FOLLOW_25_in_initializer_list1026)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_initializer_in_initializer_list1028)
                        self.initializer()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop43






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 35, initializer_list_StartIndex)

            pass

        return 

    # $ANTLR end initializer_list


    # $ANTLR start argument_expression_list
    # C.g:282:1: argument_expression_list : assignment_expression ( ',' assignment_expression )* ;
    def argument_expression_list(self, ):

        argument_expression_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 36):
                    return 

                # C.g:283:2: ( assignment_expression ( ',' assignment_expression )* )
                # C.g:283:6: assignment_expression ( ',' assignment_expression )*
                self.following.append(self.FOLLOW_assignment_expression_in_argument_expression_list1045)
                self.assignment_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:283:28: ( ',' assignment_expression )*
                while True: #loop44
                    alt44 = 2
                    LA44_0 = self.input.LA(1)

                    if (LA44_0 == 25) :
                        alt44 = 1


                    if alt44 == 1:
                        # C.g:283:29: ',' assignment_expression
                        self.match(self.input, 25, self.FOLLOW_25_in_argument_expression_list1048)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_assignment_expression_in_argument_expression_list1050)
                        self.assignment_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop44






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 36, argument_expression_list_StartIndex)

            pass

        return 

    # $ANTLR end argument_expression_list


    # $ANTLR start additive_expression
    # C.g:286:1: additive_expression : ( multiplicative_expression ) ( '+' multiplicative_expression | '-' multiplicative_expression )* ;
    def additive_expression(self, ):

        additive_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 37):
                    return 

                # C.g:287:2: ( ( multiplicative_expression ) ( '+' multiplicative_expression | '-' multiplicative_expression )* )
                # C.g:287:4: ( multiplicative_expression ) ( '+' multiplicative_expression | '-' multiplicative_expression )*
                # C.g:287:4: ( multiplicative_expression )
                # C.g:287:5: multiplicative_expression
                self.following.append(self.FOLLOW_multiplicative_expression_in_additive_expression1064)
                self.multiplicative_expression()
                self.following.pop()
                if self.failed:
                    return 



                # C.g:287:32: ( '+' multiplicative_expression | '-' multiplicative_expression )*
                while True: #loop45
                    alt45 = 3
                    LA45_0 = self.input.LA(1)

                    if (LA45_0 == 54) :
                        alt45 = 1
                    elif (LA45_0 == 55) :
                        alt45 = 2


                    if alt45 == 1:
                        # C.g:287:33: '+' multiplicative_expression
                        self.match(self.input, 54, self.FOLLOW_54_in_additive_expression1068)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_multiplicative_expression_in_additive_expression1070)
                        self.multiplicative_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt45 == 2:
                        # C.g:287:65: '-' multiplicative_expression
                        self.match(self.input, 55, self.FOLLOW_55_in_additive_expression1074)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_multiplicative_expression_in_additive_expression1076)
                        self.multiplicative_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop45






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 37, additive_expression_StartIndex)

            pass

        return 

    # $ANTLR end additive_expression


    # $ANTLR start multiplicative_expression
    # C.g:290:1: multiplicative_expression : ( cast_expression ) ( '*' cast_expression | '/' cast_expression | '%' cast_expression )* ;
    def multiplicative_expression(self, ):

        multiplicative_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 38):
                    return 

                # C.g:291:2: ( ( cast_expression ) ( '*' cast_expression | '/' cast_expression | '%' cast_expression )* )
                # C.g:291:4: ( cast_expression ) ( '*' cast_expression | '/' cast_expression | '%' cast_expression )*
                # C.g:291:4: ( cast_expression )
                # C.g:291:5: cast_expression
                self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1090)
                self.cast_expression()
                self.following.pop()
                if self.failed:
                    return 



                # C.g:291:22: ( '*' cast_expression | '/' cast_expression | '%' cast_expression )*
                while True: #loop46
                    alt46 = 4
                    LA46 = self.input.LA(1)
                    if LA46 == 52:
                        alt46 = 1
                    elif LA46 == 56:
                        alt46 = 2
                    elif LA46 == 57:
                        alt46 = 3

                    if alt46 == 1:
                        # C.g:291:23: '*' cast_expression
                        self.match(self.input, 52, self.FOLLOW_52_in_multiplicative_expression1094)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1096)
                        self.cast_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt46 == 2:
                        # C.g:291:45: '/' cast_expression
                        self.match(self.input, 56, self.FOLLOW_56_in_multiplicative_expression1100)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1102)
                        self.cast_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    elif alt46 == 3:
                        # C.g:291:67: '%' cast_expression
                        self.match(self.input, 57, self.FOLLOW_57_in_multiplicative_expression1106)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_cast_expression_in_multiplicative_expression1108)
                        self.cast_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop46






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 38, multiplicative_expression_StartIndex)

            pass

        return 

    # $ANTLR end multiplicative_expression


    # $ANTLR start cast_expression
    # C.g:294:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );
    def cast_expression(self, ):

        cast_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 39):
                    return 

                # C.g:295:2: ( '(' type_name ')' cast_expression | unary_expression )
                alt47 = 2
                LA47_0 = self.input.LA(1)

                if (LA47_0 == 48) :
                    LA47 = self.input.LA(2)
                    if LA47 == 31 or LA47 == 32 or LA47 == 33 or LA47 == 34 or LA47 == 35 or LA47 == 36 or LA47 == 37 or LA47 == 38 or LA47 == 39 or LA47 == 42 or LA47 == 43 or LA47 == 45 or LA47 == 46 or LA47 == 47:
                        alt47 = 1
                    elif LA47 == IDENTIFIER:
                        LA47_20 = self.input.LA(3)

                        if (self.synpred78()) :
                            alt47 = 1
                        elif (True) :
                            alt47 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("294:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );", 47, 20, self.input)

                            raise nvae

                    elif LA47 == HEX_LITERAL or LA47 == OCTAL_LITERAL or LA47 == DECIMAL_LITERAL or LA47 == CHARACTER_LITERAL or LA47 == STRING_LITERAL or LA47 == FLOATING_POINT_LITERAL or LA47 == 48 or LA47 == 52 or LA47 == 54 or LA47 == 55 or LA47 == 58 or LA47 == 59 or LA47 == 60 or LA47 == 63 or LA47 == 64 or LA47 == 65:
                        alt47 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("294:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );", 47, 1, self.input)

                        raise nvae

                elif ((IDENTIFIER <= LA47_0 <= FLOATING_POINT_LITERAL) or LA47_0 == 52 or (54 <= LA47_0 <= 55) or (58 <= LA47_0 <= 60) or (63 <= LA47_0 <= 65)) :
                    alt47 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("294:1: cast_expression : ( '(' type_name ')' cast_expression | unary_expression );", 47, 0, self.input)

                    raise nvae

                if alt47 == 1:
                    # C.g:295:4: '(' type_name ')' cast_expression
                    self.match(self.input, 48, self.FOLLOW_48_in_cast_expression1121)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_type_name_in_cast_expression1123)
                    self.type_name()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_cast_expression1125)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_cast_expression_in_cast_expression1127)
                    self.cast_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt47 == 2:
                    # C.g:296:4: unary_expression
                    self.following.append(self.FOLLOW_unary_expression_in_cast_expression1132)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 39, cast_expression_StartIndex)

            pass

        return 

    # $ANTLR end cast_expression


    # $ANTLR start unary_expression
    # C.g:299:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );
    def unary_expression(self, ):

        unary_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 40):
                    return 

                # C.g:300:2: ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' )
                alt48 = 6
                LA48 = self.input.LA(1)
                if LA48 == IDENTIFIER or LA48 == HEX_LITERAL or LA48 == OCTAL_LITERAL or LA48 == DECIMAL_LITERAL or LA48 == CHARACTER_LITERAL or LA48 == STRING_LITERAL or LA48 == FLOATING_POINT_LITERAL or LA48 == 48:
                    alt48 = 1
                elif LA48 == 58:
                    alt48 = 2
                elif LA48 == 59:
                    alt48 = 3
                elif LA48 == 52 or LA48 == 54 or LA48 == 55 or LA48 == 63 or LA48 == 64 or LA48 == 65:
                    alt48 = 4
                elif LA48 == 60:
                    LA48_7 = self.input.LA(2)

                    if (LA48_7 == 48) :
                        LA48_8 = self.input.LA(3)

                        if (self.synpred83()) :
                            alt48 = 5
                        elif (True) :
                            alt48 = 6
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("299:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );", 48, 8, self.input)

                            raise nvae

                    elif ((IDENTIFIER <= LA48_7 <= FLOATING_POINT_LITERAL) or LA48_7 == 52 or (54 <= LA48_7 <= 55) or (58 <= LA48_7 <= 60) or (63 <= LA48_7 <= 65)) :
                        alt48 = 5
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("299:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );", 48, 7, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("299:1: unary_expression : ( postfix_expression | '++' unary_expression | '--' unary_expression | unary_operator cast_expression | 'sizeof' unary_expression | 'sizeof' '(' type_name ')' );", 48, 0, self.input)

                    raise nvae

                if alt48 == 1:
                    # C.g:300:4: postfix_expression
                    self.following.append(self.FOLLOW_postfix_expression_in_unary_expression1143)
                    self.postfix_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt48 == 2:
                    # C.g:301:4: '++' unary_expression
                    self.match(self.input, 58, self.FOLLOW_58_in_unary_expression1148)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_unary_expression_in_unary_expression1150)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt48 == 3:
                    # C.g:302:4: '--' unary_expression
                    self.match(self.input, 59, self.FOLLOW_59_in_unary_expression1155)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_unary_expression_in_unary_expression1157)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt48 == 4:
                    # C.g:303:4: unary_operator cast_expression
                    self.following.append(self.FOLLOW_unary_operator_in_unary_expression1162)
                    self.unary_operator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_cast_expression_in_unary_expression1164)
                    self.cast_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt48 == 5:
                    # C.g:304:4: 'sizeof' unary_expression
                    self.match(self.input, 60, self.FOLLOW_60_in_unary_expression1169)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_unary_expression_in_unary_expression1171)
                    self.unary_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt48 == 6:
                    # C.g:305:4: 'sizeof' '(' type_name ')'
                    self.match(self.input, 60, self.FOLLOW_60_in_unary_expression1176)
                    if self.failed:
                        return 
                    self.match(self.input, 48, self.FOLLOW_48_in_unary_expression1178)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_type_name_in_unary_expression1180)
                    self.type_name()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_unary_expression1182)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 40, unary_expression_StartIndex)

            pass

        return 

    # $ANTLR end unary_expression


    # $ANTLR start postfix_expression
    # C.g:308:1: postfix_expression : primary_expression ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )* ;
    def postfix_expression(self, ):

        postfix_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 41):
                    return 

                # C.g:309:2: ( primary_expression ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )* )
                # C.g:309:6: primary_expression ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )*
                self.following.append(self.FOLLOW_primary_expression_in_postfix_expression1195)
                self.primary_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:310:9: ( '[' expression ']' | '(' ')' | '(' argument_expression_list ')' | '.' IDENTIFIER | '*' IDENTIFIER | '->' IDENTIFIER | '++' | '--' )*
                while True: #loop49
                    alt49 = 9
                    LA49 = self.input.LA(1)
                    if LA49 == 52:
                        LA49_1 = self.input.LA(2)

                        if (LA49_1 == IDENTIFIER) :
                            LA49_29 = self.input.LA(3)

                            if (self.synpred88()) :
                                alt49 = 5




                    elif LA49 == 50:
                        alt49 = 1
                    elif LA49 == 48:
                        LA49_24 = self.input.LA(2)

                        if (LA49_24 == 49) :
                            alt49 = 2
                        elif ((IDENTIFIER <= LA49_24 <= FLOATING_POINT_LITERAL) or LA49_24 == 48 or LA49_24 == 52 or (54 <= LA49_24 <= 55) or (58 <= LA49_24 <= 60) or (63 <= LA49_24 <= 65)) :
                            alt49 = 3


                    elif LA49 == 61:
                        alt49 = 4
                    elif LA49 == 62:
                        alt49 = 6
                    elif LA49 == 58:
                        alt49 = 7
                    elif LA49 == 59:
                        alt49 = 8

                    if alt49 == 1:
                        # C.g:310:13: '[' expression ']'
                        self.match(self.input, 50, self.FOLLOW_50_in_postfix_expression1209)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_expression_in_postfix_expression1211)
                        self.expression()
                        self.following.pop()
                        if self.failed:
                            return 
                        self.match(self.input, 51, self.FOLLOW_51_in_postfix_expression1213)
                        if self.failed:
                            return 


                    elif alt49 == 2:
                        # C.g:311:13: '(' ')'
                        self.match(self.input, 48, self.FOLLOW_48_in_postfix_expression1227)
                        if self.failed:
                            return 
                        self.match(self.input, 49, self.FOLLOW_49_in_postfix_expression1229)
                        if self.failed:
                            return 


                    elif alt49 == 3:
                        # C.g:312:13: '(' argument_expression_list ')'
                        self.match(self.input, 48, self.FOLLOW_48_in_postfix_expression1243)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_argument_expression_list_in_postfix_expression1245)
                        self.argument_expression_list()
                        self.following.pop()
                        if self.failed:
                            return 
                        self.match(self.input, 49, self.FOLLOW_49_in_postfix_expression1247)
                        if self.failed:
                            return 


                    elif alt49 == 4:
                        # C.g:313:13: '.' IDENTIFIER
                        self.match(self.input, 61, self.FOLLOW_61_in_postfix_expression1261)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_postfix_expression1263)
                        if self.failed:
                            return 


                    elif alt49 == 5:
                        # C.g:314:13: '*' IDENTIFIER
                        self.match(self.input, 52, self.FOLLOW_52_in_postfix_expression1277)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_postfix_expression1279)
                        if self.failed:
                            return 


                    elif alt49 == 6:
                        # C.g:315:13: '->' IDENTIFIER
                        self.match(self.input, 62, self.FOLLOW_62_in_postfix_expression1293)
                        if self.failed:
                            return 
                        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_postfix_expression1295)
                        if self.failed:
                            return 


                    elif alt49 == 7:
                        # C.g:316:13: '++'
                        self.match(self.input, 58, self.FOLLOW_58_in_postfix_expression1309)
                        if self.failed:
                            return 


                    elif alt49 == 8:
                        # C.g:317:13: '--'
                        self.match(self.input, 59, self.FOLLOW_59_in_postfix_expression1323)
                        if self.failed:
                            return 


                    else:
                        break #loop49






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 41, postfix_expression_StartIndex)

            pass

        return 

    # $ANTLR end postfix_expression


    # $ANTLR start unary_operator
    # C.g:321:1: unary_operator : ( '&' | '*' | '+' | '-' | '~' | '!' );
    def unary_operator(self, ):

        unary_operator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 42):
                    return 

                # C.g:322:2: ( '&' | '*' | '+' | '-' | '~' | '!' )
                # C.g:
                if self.input.LA(1) == 52 or (54 <= self.input.LA(1) <= 55) or (63 <= self.input.LA(1) <= 65):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_unary_operator0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 42, unary_operator_StartIndex)

            pass

        return 

    # $ANTLR end unary_operator


    # $ANTLR start primary_expression
    # C.g:330:1: primary_expression : ( IDENTIFIER | constant | '(' expression ')' );
    def primary_expression(self, ):

        primary_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 43):
                    return 

                # C.g:331:2: ( IDENTIFIER | constant | '(' expression ')' )
                alt50 = 3
                LA50 = self.input.LA(1)
                if LA50 == IDENTIFIER:
                    alt50 = 1
                elif LA50 == HEX_LITERAL or LA50 == OCTAL_LITERAL or LA50 == DECIMAL_LITERAL or LA50 == CHARACTER_LITERAL or LA50 == STRING_LITERAL or LA50 == FLOATING_POINT_LITERAL:
                    alt50 = 2
                elif LA50 == 48:
                    alt50 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("330:1: primary_expression : ( IDENTIFIER | constant | '(' expression ')' );", 50, 0, self.input)

                    raise nvae

                if alt50 == 1:
                    # C.g:331:4: IDENTIFIER
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_primary_expression1381)
                    if self.failed:
                        return 


                elif alt50 == 2:
                    # C.g:332:4: constant
                    self.following.append(self.FOLLOW_constant_in_primary_expression1386)
                    self.constant()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt50 == 3:
                    # C.g:333:4: '(' expression ')'
                    self.match(self.input, 48, self.FOLLOW_48_in_primary_expression1391)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_primary_expression1393)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_primary_expression1395)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 43, primary_expression_StartIndex)

            pass

        return 

    # $ANTLR end primary_expression


    # $ANTLR start constant
    # C.g:336:1: constant : ( HEX_LITERAL | OCTAL_LITERAL | DECIMAL_LITERAL | CHARACTER_LITERAL | STRING_LITERAL | FLOATING_POINT_LITERAL );
    def constant(self, ):

        constant_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 44):
                    return 

                # C.g:337:5: ( HEX_LITERAL | OCTAL_LITERAL | DECIMAL_LITERAL | CHARACTER_LITERAL | STRING_LITERAL | FLOATING_POINT_LITERAL )
                # C.g:
                if (HEX_LITERAL <= self.input.LA(1) <= FLOATING_POINT_LITERAL):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_constant0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 44, constant_StartIndex)

            pass

        return 

    # $ANTLR end constant


    # $ANTLR start expression
    # C.g:347:1: expression : assignment_expression ( ',' assignment_expression )* ;
    def expression(self, ):

        expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 45):
                    return 

                # C.g:348:2: ( assignment_expression ( ',' assignment_expression )* )
                # C.g:348:4: assignment_expression ( ',' assignment_expression )*
                self.following.append(self.FOLLOW_assignment_expression_in_expression1470)
                self.assignment_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:348:26: ( ',' assignment_expression )*
                while True: #loop51
                    alt51 = 2
                    LA51_0 = self.input.LA(1)

                    if (LA51_0 == 25) :
                        alt51 = 1


                    if alt51 == 1:
                        # C.g:348:27: ',' assignment_expression
                        self.match(self.input, 25, self.FOLLOW_25_in_expression1473)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_assignment_expression_in_expression1475)
                        self.assignment_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop51






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 45, expression_StartIndex)

            pass

        return 

    # $ANTLR end expression


    # $ANTLR start constant_expression
    # C.g:351:1: constant_expression : conditional_expression ;
    def constant_expression(self, ):

        constant_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 46):
                    return 

                # C.g:352:2: ( conditional_expression )
                # C.g:352:4: conditional_expression
                self.following.append(self.FOLLOW_conditional_expression_in_constant_expression1488)
                self.conditional_expression()
                self.following.pop()
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 46, constant_expression_StartIndex)

            pass

        return 

    # $ANTLR end constant_expression


    # $ANTLR start assignment_expression
    # C.g:355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );
    def assignment_expression(self, ):

        assignment_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 47):
                    return 

                # C.g:356:2: ( lvalue assignment_operator assignment_expression | conditional_expression )
                alt52 = 2
                LA52 = self.input.LA(1)
                if LA52 == IDENTIFIER:
                    LA52 = self.input.LA(2)
                    if LA52 == 50:
                        LA52_8 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 8, self.input)

                            raise nvae

                    elif LA52 == 48:
                        LA52_9 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 9, self.input)

                            raise nvae

                    elif LA52 == 61:
                        LA52_10 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 10, self.input)

                            raise nvae

                    elif LA52 == 52:
                        LA52_11 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 11, self.input)

                            raise nvae

                    elif LA52 == 62:
                        LA52_12 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 12, self.input)

                            raise nvae

                    elif LA52 == 58:
                        LA52_13 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 13, self.input)

                            raise nvae

                    elif LA52 == 59:
                        LA52_14 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 14, self.input)

                            raise nvae

                    elif LA52 == EOF or LA52 == 24 or LA52 == 25 or LA52 == 41 or LA52 == 44 or LA52 == 49 or LA52 == 51 or LA52 == 54 or LA52 == 55 or LA52 == 56 or LA52 == 57 or LA52 == 63 or LA52 == 76 or LA52 == 77 or LA52 == 78 or LA52 == 79 or LA52 == 80 or LA52 == 81 or LA52 == 82 or LA52 == 83 or LA52 == 84 or LA52 == 85 or LA52 == 86 or LA52 == 87 or LA52 == 88:
                        alt52 = 2
                    elif LA52 == 26 or LA52 == 66 or LA52 == 67 or LA52 == 68 or LA52 == 69 or LA52 == 70 or LA52 == 71 or LA52 == 72 or LA52 == 73 or LA52 == 74 or LA52 == 75:
                        alt52 = 1
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 1, self.input)

                        raise nvae

                elif LA52 == HEX_LITERAL or LA52 == OCTAL_LITERAL or LA52 == DECIMAL_LITERAL or LA52 == CHARACTER_LITERAL or LA52 == STRING_LITERAL or LA52 == FLOATING_POINT_LITERAL:
                    LA52 = self.input.LA(2)
                    if LA52 == 50:
                        LA52_36 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 36, self.input)

                            raise nvae

                    elif LA52 == 48:
                        LA52_37 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 37, self.input)

                            raise nvae

                    elif LA52 == 61:
                        LA52_38 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 38, self.input)

                            raise nvae

                    elif LA52 == 52:
                        LA52_39 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 39, self.input)

                            raise nvae

                    elif LA52 == 62:
                        LA52_40 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 40, self.input)

                            raise nvae

                    elif LA52 == 58:
                        LA52_41 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 41, self.input)

                            raise nvae

                    elif LA52 == 59:
                        LA52_42 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 42, self.input)

                            raise nvae

                    elif LA52 == 26 or LA52 == 66 or LA52 == 67 or LA52 == 68 or LA52 == 69 or LA52 == 70 or LA52 == 71 or LA52 == 72 or LA52 == 73 or LA52 == 74 or LA52 == 75:
                        alt52 = 1
                    elif LA52 == EOF or LA52 == 24 or LA52 == 25 or LA52 == 41 or LA52 == 44 or LA52 == 49 or LA52 == 51 or LA52 == 54 or LA52 == 55 or LA52 == 56 or LA52 == 57 or LA52 == 63 or LA52 == 76 or LA52 == 77 or LA52 == 78 or LA52 == 79 or LA52 == 80 or LA52 == 81 or LA52 == 82 or LA52 == 83 or LA52 == 84 or LA52 == 85 or LA52 == 86 or LA52 == 87 or LA52 == 88:
                        alt52 = 2
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 2, self.input)

                        raise nvae

                elif LA52 == 48:
                    LA52 = self.input.LA(2)
                    if LA52 == 31 or LA52 == 32 or LA52 == 33 or LA52 == 34 or LA52 == 35 or LA52 == 36 or LA52 == 37 or LA52 == 38 or LA52 == 39 or LA52 == 42 or LA52 == 43 or LA52 == 45 or LA52 == 46 or LA52 == 47:
                        alt52 = 2
                    elif LA52 == IDENTIFIER:
                        LA52_76 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 76, self.input)

                            raise nvae

                    elif LA52 == HEX_LITERAL or LA52 == OCTAL_LITERAL or LA52 == DECIMAL_LITERAL or LA52 == CHARACTER_LITERAL or LA52 == STRING_LITERAL or LA52 == FLOATING_POINT_LITERAL:
                        LA52_77 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 77, self.input)

                            raise nvae

                    elif LA52 == 48:
                        LA52_78 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 78, self.input)

                            raise nvae

                    elif LA52 == 58:
                        LA52_79 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 79, self.input)

                            raise nvae

                    elif LA52 == 59:
                        LA52_80 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 80, self.input)

                            raise nvae

                    elif LA52 == 52 or LA52 == 54 or LA52 == 55 or LA52 == 63 or LA52 == 64 or LA52 == 65:
                        LA52_81 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 81, self.input)

                            raise nvae

                    elif LA52 == 60:
                        LA52_82 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 82, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 3, self.input)

                        raise nvae

                elif LA52 == 58:
                    LA52 = self.input.LA(2)
                    if LA52 == IDENTIFIER:
                        LA52_83 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 83, self.input)

                            raise nvae

                    elif LA52 == HEX_LITERAL or LA52 == OCTAL_LITERAL or LA52 == DECIMAL_LITERAL or LA52 == CHARACTER_LITERAL or LA52 == STRING_LITERAL or LA52 == FLOATING_POINT_LITERAL:
                        LA52_84 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 84, self.input)

                            raise nvae

                    elif LA52 == 48:
                        LA52_85 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 85, self.input)

                            raise nvae

                    elif LA52 == 58:
                        LA52_86 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 86, self.input)

                            raise nvae

                    elif LA52 == 59:
                        LA52_87 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 87, self.input)

                            raise nvae

                    elif LA52 == 52 or LA52 == 54 or LA52 == 55 or LA52 == 63 or LA52 == 64 or LA52 == 65:
                        LA52_88 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 88, self.input)

                            raise nvae

                    elif LA52 == 60:
                        LA52_89 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 89, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 4, self.input)

                        raise nvae

                elif LA52 == 59:
                    LA52 = self.input.LA(2)
                    if LA52 == IDENTIFIER:
                        LA52_90 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 90, self.input)

                            raise nvae

                    elif LA52 == HEX_LITERAL or LA52 == OCTAL_LITERAL or LA52 == DECIMAL_LITERAL or LA52 == CHARACTER_LITERAL or LA52 == STRING_LITERAL or LA52 == FLOATING_POINT_LITERAL:
                        LA52_91 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 91, self.input)

                            raise nvae

                    elif LA52 == 48:
                        LA52_92 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 92, self.input)

                            raise nvae

                    elif LA52 == 58:
                        LA52_93 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 93, self.input)

                            raise nvae

                    elif LA52 == 59:
                        LA52_94 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 94, self.input)

                            raise nvae

                    elif LA52 == 52 or LA52 == 54 or LA52 == 55 or LA52 == 63 or LA52 == 64 or LA52 == 65:
                        LA52_95 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 95, self.input)

                            raise nvae

                    elif LA52 == 60:
                        LA52_96 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 96, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 5, self.input)

                        raise nvae

                elif LA52 == 52 or LA52 == 54 or LA52 == 55 or LA52 == 63 or LA52 == 64 or LA52 == 65:
                    LA52 = self.input.LA(2)
                    if LA52 == 48:
                        LA52_97 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 97, self.input)

                            raise nvae

                    elif LA52 == IDENTIFIER:
                        LA52_98 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 98, self.input)

                            raise nvae

                    elif LA52 == HEX_LITERAL or LA52 == OCTAL_LITERAL or LA52 == DECIMAL_LITERAL or LA52 == CHARACTER_LITERAL or LA52 == STRING_LITERAL or LA52 == FLOATING_POINT_LITERAL:
                        LA52_99 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 99, self.input)

                            raise nvae

                    elif LA52 == 58:
                        LA52_100 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 100, self.input)

                            raise nvae

                    elif LA52 == 59:
                        LA52_101 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 101, self.input)

                            raise nvae

                    elif LA52 == 52 or LA52 == 54 or LA52 == 55 or LA52 == 63 or LA52 == 64 or LA52 == 65:
                        LA52_102 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 102, self.input)

                            raise nvae

                    elif LA52 == 60:
                        LA52_103 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 103, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 6, self.input)

                        raise nvae

                elif LA52 == 60:
                    LA52 = self.input.LA(2)
                    if LA52 == 48:
                        LA52_104 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 104, self.input)

                            raise nvae

                    elif LA52 == IDENTIFIER:
                        LA52_105 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 105, self.input)

                            raise nvae

                    elif LA52 == HEX_LITERAL or LA52 == OCTAL_LITERAL or LA52 == DECIMAL_LITERAL or LA52 == CHARACTER_LITERAL or LA52 == STRING_LITERAL or LA52 == FLOATING_POINT_LITERAL:
                        LA52_106 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 106, self.input)

                            raise nvae

                    elif LA52 == 58:
                        LA52_107 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 107, self.input)

                            raise nvae

                    elif LA52 == 59:
                        LA52_108 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 108, self.input)

                            raise nvae

                    elif LA52 == 52 or LA52 == 54 or LA52 == 55 or LA52 == 63 or LA52 == 64 or LA52 == 65:
                        LA52_109 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 109, self.input)

                            raise nvae

                    elif LA52 == 60:
                        LA52_110 = self.input.LA(3)

                        if (self.synpred105()) :
                            alt52 = 1
                        elif (True) :
                            alt52 = 2
                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 110, self.input)

                            raise nvae

                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 7, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("355:1: assignment_expression : ( lvalue assignment_operator assignment_expression | conditional_expression );", 52, 0, self.input)

                    raise nvae

                if alt52 == 1:
                    # C.g:356:4: lvalue assignment_operator assignment_expression
                    self.following.append(self.FOLLOW_lvalue_in_assignment_expression1499)
                    self.lvalue()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_assignment_operator_in_assignment_expression1501)
                    self.assignment_operator()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_assignment_expression_in_assignment_expression1503)
                    self.assignment_expression()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt52 == 2:
                    # C.g:357:4: conditional_expression
                    self.following.append(self.FOLLOW_conditional_expression_in_assignment_expression1508)
                    self.conditional_expression()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 47, assignment_expression_StartIndex)

            pass

        return 

    # $ANTLR end assignment_expression


    # $ANTLR start lvalue
    # C.g:360:1: lvalue : unary_expression ;
    def lvalue(self, ):

        lvalue_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 48):
                    return 

                # C.g:361:2: ( unary_expression )
                # C.g:361:4: unary_expression
                self.following.append(self.FOLLOW_unary_expression_in_lvalue1520)
                self.unary_expression()
                self.following.pop()
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 48, lvalue_StartIndex)

            pass

        return 

    # $ANTLR end lvalue


    # $ANTLR start assignment_operator
    # C.g:364:1: assignment_operator : ( '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|=' );
    def assignment_operator(self, ):

        assignment_operator_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 49):
                    return 

                # C.g:365:2: ( '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|=' )
                # C.g:
                if self.input.LA(1) == 26 or (66 <= self.input.LA(1) <= 75):
                    self.input.consume();
                    self.errorRecovery = False
                    self.failed = False

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_assignment_operator0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 49, assignment_operator_StartIndex)

            pass

        return 

    # $ANTLR end assignment_operator


    # $ANTLR start conditional_expression
    # C.g:378:1: conditional_expression : logical_or_expression ( '?' expression ':' conditional_expression )? ;
    def conditional_expression(self, ):

        conditional_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 50):
                    return 

                # C.g:379:2: ( logical_or_expression ( '?' expression ':' conditional_expression )? )
                # C.g:379:4: logical_or_expression ( '?' expression ':' conditional_expression )?
                self.following.append(self.FOLLOW_logical_or_expression_in_conditional_expression1592)
                self.logical_or_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:379:26: ( '?' expression ':' conditional_expression )?
                alt53 = 2
                LA53_0 = self.input.LA(1)

                if (LA53_0 == 76) :
                    alt53 = 1
                if alt53 == 1:
                    # C.g:379:27: '?' expression ':' conditional_expression
                    self.match(self.input, 76, self.FOLLOW_76_in_conditional_expression1595)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_conditional_expression1597)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 44, self.FOLLOW_44_in_conditional_expression1599)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_conditional_expression_in_conditional_expression1601)
                    self.conditional_expression()
                    self.following.pop()
                    if self.failed:
                        return 







            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 50, conditional_expression_StartIndex)

            pass

        return 

    # $ANTLR end conditional_expression


    # $ANTLR start logical_or_expression
    # C.g:382:1: logical_or_expression : logical_and_expression ( '||' logical_and_expression )* ;
    def logical_or_expression(self, ):

        logical_or_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 51):
                    return 

                # C.g:383:2: ( logical_and_expression ( '||' logical_and_expression )* )
                # C.g:383:4: logical_and_expression ( '||' logical_and_expression )*
                self.following.append(self.FOLLOW_logical_and_expression_in_logical_or_expression1614)
                self.logical_and_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:383:27: ( '||' logical_and_expression )*
                while True: #loop54
                    alt54 = 2
                    LA54_0 = self.input.LA(1)

                    if (LA54_0 == 77) :
                        alt54 = 1


                    if alt54 == 1:
                        # C.g:383:28: '||' logical_and_expression
                        self.match(self.input, 77, self.FOLLOW_77_in_logical_or_expression1617)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_logical_and_expression_in_logical_or_expression1619)
                        self.logical_and_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop54






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 51, logical_or_expression_StartIndex)

            pass

        return 

    # $ANTLR end logical_or_expression


    # $ANTLR start logical_and_expression
    # C.g:386:1: logical_and_expression : inclusive_or_expression ( '&&' inclusive_or_expression )* ;
    def logical_and_expression(self, ):

        logical_and_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 52):
                    return 

                # C.g:387:2: ( inclusive_or_expression ( '&&' inclusive_or_expression )* )
                # C.g:387:4: inclusive_or_expression ( '&&' inclusive_or_expression )*
                self.following.append(self.FOLLOW_inclusive_or_expression_in_logical_and_expression1632)
                self.inclusive_or_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:387:28: ( '&&' inclusive_or_expression )*
                while True: #loop55
                    alt55 = 2
                    LA55_0 = self.input.LA(1)

                    if (LA55_0 == 78) :
                        alt55 = 1


                    if alt55 == 1:
                        # C.g:387:29: '&&' inclusive_or_expression
                        self.match(self.input, 78, self.FOLLOW_78_in_logical_and_expression1635)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_inclusive_or_expression_in_logical_and_expression1637)
                        self.inclusive_or_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop55






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 52, logical_and_expression_StartIndex)

            pass

        return 

    # $ANTLR end logical_and_expression


    # $ANTLR start inclusive_or_expression
    # C.g:390:1: inclusive_or_expression : exclusive_or_expression ( '|' exclusive_or_expression )* ;
    def inclusive_or_expression(self, ):

        inclusive_or_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 53):
                    return 

                # C.g:391:2: ( exclusive_or_expression ( '|' exclusive_or_expression )* )
                # C.g:391:4: exclusive_or_expression ( '|' exclusive_or_expression )*
                self.following.append(self.FOLLOW_exclusive_or_expression_in_inclusive_or_expression1650)
                self.exclusive_or_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:391:28: ( '|' exclusive_or_expression )*
                while True: #loop56
                    alt56 = 2
                    LA56_0 = self.input.LA(1)

                    if (LA56_0 == 79) :
                        alt56 = 1


                    if alt56 == 1:
                        # C.g:391:29: '|' exclusive_or_expression
                        self.match(self.input, 79, self.FOLLOW_79_in_inclusive_or_expression1653)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_exclusive_or_expression_in_inclusive_or_expression1655)
                        self.exclusive_or_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop56






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 53, inclusive_or_expression_StartIndex)

            pass

        return 

    # $ANTLR end inclusive_or_expression


    # $ANTLR start exclusive_or_expression
    # C.g:394:1: exclusive_or_expression : and_expression ( '^' and_expression )* ;
    def exclusive_or_expression(self, ):

        exclusive_or_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 54):
                    return 

                # C.g:395:2: ( and_expression ( '^' and_expression )* )
                # C.g:395:4: and_expression ( '^' and_expression )*
                self.following.append(self.FOLLOW_and_expression_in_exclusive_or_expression1668)
                self.and_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:395:19: ( '^' and_expression )*
                while True: #loop57
                    alt57 = 2
                    LA57_0 = self.input.LA(1)

                    if (LA57_0 == 80) :
                        alt57 = 1


                    if alt57 == 1:
                        # C.g:395:20: '^' and_expression
                        self.match(self.input, 80, self.FOLLOW_80_in_exclusive_or_expression1671)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_and_expression_in_exclusive_or_expression1673)
                        self.and_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop57






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 54, exclusive_or_expression_StartIndex)

            pass

        return 

    # $ANTLR end exclusive_or_expression


    # $ANTLR start and_expression
    # C.g:398:1: and_expression : equality_expression ( '&' equality_expression )* ;
    def and_expression(self, ):

        and_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 55):
                    return 

                # C.g:399:2: ( equality_expression ( '&' equality_expression )* )
                # C.g:399:4: equality_expression ( '&' equality_expression )*
                self.following.append(self.FOLLOW_equality_expression_in_and_expression1686)
                self.equality_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:399:24: ( '&' equality_expression )*
                while True: #loop58
                    alt58 = 2
                    LA58_0 = self.input.LA(1)

                    if (LA58_0 == 63) :
                        alt58 = 1


                    if alt58 == 1:
                        # C.g:399:25: '&' equality_expression
                        self.match(self.input, 63, self.FOLLOW_63_in_and_expression1689)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_equality_expression_in_and_expression1691)
                        self.equality_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop58






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 55, and_expression_StartIndex)

            pass

        return 

    # $ANTLR end and_expression


    # $ANTLR start equality_expression
    # C.g:401:1: equality_expression : relational_expression ( ( '==' | '!=' ) relational_expression )* ;
    def equality_expression(self, ):

        equality_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 56):
                    return 

                # C.g:402:2: ( relational_expression ( ( '==' | '!=' ) relational_expression )* )
                # C.g:402:4: relational_expression ( ( '==' | '!=' ) relational_expression )*
                self.following.append(self.FOLLOW_relational_expression_in_equality_expression1703)
                self.relational_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:402:26: ( ( '==' | '!=' ) relational_expression )*
                while True: #loop59
                    alt59 = 2
                    LA59_0 = self.input.LA(1)

                    if ((81 <= LA59_0 <= 82)) :
                        alt59 = 1


                    if alt59 == 1:
                        # C.g:402:27: ( '==' | '!=' ) relational_expression
                        if (81 <= self.input.LA(1) <= 82):
                            self.input.consume();
                            self.errorRecovery = False
                            self.failed = False

                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            mse = MismatchedSetException(None, self.input)
                            self.recoverFromMismatchedSet(
                                self.input, mse, self.FOLLOW_set_in_equality_expression1706
                                )
                            raise mse


                        self.following.append(self.FOLLOW_relational_expression_in_equality_expression1712)
                        self.relational_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop59






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 56, equality_expression_StartIndex)

            pass

        return 

    # $ANTLR end equality_expression


    # $ANTLR start relational_expression
    # C.g:405:1: relational_expression : shift_expression ( ( '<' | '>' | '<=' | '>=' ) shift_expression )* ;
    def relational_expression(self, ):

        relational_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 57):
                    return 

                # C.g:406:2: ( shift_expression ( ( '<' | '>' | '<=' | '>=' ) shift_expression )* )
                # C.g:406:4: shift_expression ( ( '<' | '>' | '<=' | '>=' ) shift_expression )*
                self.following.append(self.FOLLOW_shift_expression_in_relational_expression1725)
                self.shift_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:406:21: ( ( '<' | '>' | '<=' | '>=' ) shift_expression )*
                while True: #loop60
                    alt60 = 2
                    LA60_0 = self.input.LA(1)

                    if ((83 <= LA60_0 <= 86)) :
                        alt60 = 1


                    if alt60 == 1:
                        # C.g:406:22: ( '<' | '>' | '<=' | '>=' ) shift_expression
                        if (83 <= self.input.LA(1) <= 86):
                            self.input.consume();
                            self.errorRecovery = False
                            self.failed = False

                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            mse = MismatchedSetException(None, self.input)
                            self.recoverFromMismatchedSet(
                                self.input, mse, self.FOLLOW_set_in_relational_expression1728
                                )
                            raise mse


                        self.following.append(self.FOLLOW_shift_expression_in_relational_expression1738)
                        self.shift_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop60






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 57, relational_expression_StartIndex)

            pass

        return 

    # $ANTLR end relational_expression


    # $ANTLR start shift_expression
    # C.g:409:1: shift_expression : additive_expression ( ( '<<' | '>>' ) additive_expression )* ;
    def shift_expression(self, ):

        shift_expression_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 58):
                    return 

                # C.g:410:2: ( additive_expression ( ( '<<' | '>>' ) additive_expression )* )
                # C.g:410:4: additive_expression ( ( '<<' | '>>' ) additive_expression )*
                self.following.append(self.FOLLOW_additive_expression_in_shift_expression1751)
                self.additive_expression()
                self.following.pop()
                if self.failed:
                    return 
                # C.g:410:24: ( ( '<<' | '>>' ) additive_expression )*
                while True: #loop61
                    alt61 = 2
                    LA61_0 = self.input.LA(1)

                    if ((87 <= LA61_0 <= 88)) :
                        alt61 = 1


                    if alt61 == 1:
                        # C.g:410:25: ( '<<' | '>>' ) additive_expression
                        if (87 <= self.input.LA(1) <= 88):
                            self.input.consume();
                            self.errorRecovery = False
                            self.failed = False

                        else:
                            if self.backtracking > 0:
                                self.failed = True
                                return 

                            mse = MismatchedSetException(None, self.input)
                            self.recoverFromMismatchedSet(
                                self.input, mse, self.FOLLOW_set_in_shift_expression1754
                                )
                            raise mse


                        self.following.append(self.FOLLOW_additive_expression_in_shift_expression1760)
                        self.additive_expression()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop61






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 58, shift_expression_StartIndex)

            pass

        return 

    # $ANTLR end shift_expression


    # $ANTLR start statement
    # C.g:415:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement );
    def statement(self, ):

        statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 59):
                    return 

                # C.g:416:2: ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement )
                alt62 = 6
                LA62 = self.input.LA(1)
                if LA62 == IDENTIFIER:
                    LA62_1 = self.input.LA(2)

                    if (LA62_1 == 44) :
                        alt62 = 1
                    elif ((24 <= LA62_1 <= 26) or LA62_1 == 48 or LA62_1 == 50 or LA62_1 == 52 or (54 <= LA62_1 <= 59) or (61 <= LA62_1 <= 63) or (66 <= LA62_1 <= 88)) :
                        alt62 = 3
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("415:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement );", 62, 1, self.input)

                        raise nvae

                elif LA62 == 89 or LA62 == 90:
                    alt62 = 1
                elif LA62 == 40:
                    alt62 = 2
                elif LA62 == HEX_LITERAL or LA62 == OCTAL_LITERAL or LA62 == DECIMAL_LITERAL or LA62 == CHARACTER_LITERAL or LA62 == STRING_LITERAL or LA62 == FLOATING_POINT_LITERAL or LA62 == 24 or LA62 == 48 or LA62 == 52 or LA62 == 54 or LA62 == 55 or LA62 == 58 or LA62 == 59 or LA62 == 60 or LA62 == 63 or LA62 == 64 or LA62 == 65:
                    alt62 = 3
                elif LA62 == 91 or LA62 == 93:
                    alt62 = 4
                elif LA62 == 94 or LA62 == 95 or LA62 == 96:
                    alt62 = 5
                elif LA62 == 97 or LA62 == 98 or LA62 == 99 or LA62 == 100:
                    alt62 = 6
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("415:1: statement : ( labeled_statement | compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement );", 62, 0, self.input)

                    raise nvae

                if alt62 == 1:
                    # C.g:416:4: labeled_statement
                    self.following.append(self.FOLLOW_labeled_statement_in_statement1775)
                    self.labeled_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt62 == 2:
                    # C.g:417:4: compound_statement
                    self.following.append(self.FOLLOW_compound_statement_in_statement1780)
                    self.compound_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt62 == 3:
                    # C.g:418:4: expression_statement
                    self.following.append(self.FOLLOW_expression_statement_in_statement1785)
                    self.expression_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt62 == 4:
                    # C.g:419:4: selection_statement
                    self.following.append(self.FOLLOW_selection_statement_in_statement1790)
                    self.selection_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt62 == 5:
                    # C.g:420:4: iteration_statement
                    self.following.append(self.FOLLOW_iteration_statement_in_statement1795)
                    self.iteration_statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt62 == 6:
                    # C.g:421:4: jump_statement
                    self.following.append(self.FOLLOW_jump_statement_in_statement1800)
                    self.jump_statement()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 59, statement_StartIndex)

            pass

        return 

    # $ANTLR end statement


    # $ANTLR start labeled_statement
    # C.g:424:1: labeled_statement : ( IDENTIFIER ':' statement | 'case' constant_expression ':' statement | 'default' ':' statement );
    def labeled_statement(self, ):

        labeled_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 60):
                    return 

                # C.g:425:2: ( IDENTIFIER ':' statement | 'case' constant_expression ':' statement | 'default' ':' statement )
                alt63 = 3
                LA63 = self.input.LA(1)
                if LA63 == IDENTIFIER:
                    alt63 = 1
                elif LA63 == 89:
                    alt63 = 2
                elif LA63 == 90:
                    alt63 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("424:1: labeled_statement : ( IDENTIFIER ':' statement | 'case' constant_expression ':' statement | 'default' ':' statement );", 63, 0, self.input)

                    raise nvae

                if alt63 == 1:
                    # C.g:425:4: IDENTIFIER ':' statement
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_labeled_statement1811)
                    if self.failed:
                        return 
                    self.match(self.input, 44, self.FOLLOW_44_in_labeled_statement1813)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_labeled_statement1815)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt63 == 2:
                    # C.g:426:4: 'case' constant_expression ':' statement
                    self.match(self.input, 89, self.FOLLOW_89_in_labeled_statement1820)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_constant_expression_in_labeled_statement1822)
                    self.constant_expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 44, self.FOLLOW_44_in_labeled_statement1824)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_labeled_statement1826)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt63 == 3:
                    # C.g:427:4: 'default' ':' statement
                    self.match(self.input, 90, self.FOLLOW_90_in_labeled_statement1831)
                    if self.failed:
                        return 
                    self.match(self.input, 44, self.FOLLOW_44_in_labeled_statement1833)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_labeled_statement1835)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 60, labeled_statement_StartIndex)

            pass

        return 

    # $ANTLR end labeled_statement


    # $ANTLR start compound_statement
    # C.g:430:1: compound_statement : '{' ( declaration )* ( statement_list )? '}' ;
    def compound_statement(self, ):
        self.Symbols_stack.append(Symbols_scope())

        compound_statement_StartIndex = self.input.index()
               
        self.Symbols_stack[-1].types = set()

        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 61):
                    return 

                # C.g:435:2: ( '{' ( declaration )* ( statement_list )? '}' )
                # C.g:435:4: '{' ( declaration )* ( statement_list )? '}'
                self.match(self.input, 40, self.FOLLOW_40_in_compound_statement1857)
                if self.failed:
                    return 
                # C.g:435:8: ( declaration )*
                while True: #loop64
                    alt64 = 2
                    LA64_0 = self.input.LA(1)

                    if (LA64_0 == IDENTIFIER) :
                        LA64 = self.input.LA(2)
                        if LA64 == 48:
                            LA64_38 = self.input.LA(3)

                            if ((self.synpred137() and self.isTypeName(self.input.LT(1).text))) :
                                alt64 = 1


                        elif LA64 == 52:
                            LA64_40 = self.input.LA(3)

                            if ((self.synpred137() and self.isTypeName(self.input.LT(1).text))) :
                                alt64 = 1


                        elif LA64 == 24:
                            LA64_59 = self.input.LA(3)

                            if ((self.synpred137() and self.isTypeName(self.input.LT(1).text))) :
                                alt64 = 1


                        elif LA64 == IDENTIFIER or LA64 == 27 or LA64 == 28 or LA64 == 29 or LA64 == 30 or LA64 == 31 or LA64 == 32 or LA64 == 33 or LA64 == 34 or LA64 == 35 or LA64 == 36 or LA64 == 37 or LA64 == 38 or LA64 == 39 or LA64 == 42 or LA64 == 43 or LA64 == 45 or LA64 == 46 or LA64 == 47:
                            alt64 = 1

                    elif (LA64_0 == 23 or (27 <= LA64_0 <= 39) or (42 <= LA64_0 <= 43) or (45 <= LA64_0 <= 47)) :
                        alt64 = 1


                    if alt64 == 1:
                        # C.g:0:0: declaration
                        self.following.append(self.FOLLOW_declaration_in_compound_statement1859)
                        self.declaration()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        break #loop64


                # C.g:435:21: ( statement_list )?
                alt65 = 2
                LA65_0 = self.input.LA(1)

                if ((IDENTIFIER <= LA65_0 <= FLOATING_POINT_LITERAL) or LA65_0 == 24 or LA65_0 == 40 or LA65_0 == 48 or LA65_0 == 52 or (54 <= LA65_0 <= 55) or (58 <= LA65_0 <= 60) or (63 <= LA65_0 <= 65) or (89 <= LA65_0 <= 91) or (93 <= LA65_0 <= 100)) :
                    alt65 = 1
                if alt65 == 1:
                    # C.g:0:0: statement_list
                    self.following.append(self.FOLLOW_statement_list_in_compound_statement1862)
                    self.statement_list()
                    self.following.pop()
                    if self.failed:
                        return 



                self.match(self.input, 41, self.FOLLOW_41_in_compound_statement1865)
                if self.failed:
                    return 




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 61, compound_statement_StartIndex)

            self.Symbols_stack.pop()

            pass

        return 

    # $ANTLR end compound_statement


    # $ANTLR start statement_list
    # C.g:438:1: statement_list : ( statement )+ ;
    def statement_list(self, ):

        statement_list_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 62):
                    return 

                # C.g:439:2: ( ( statement )+ )
                # C.g:439:4: ( statement )+
                # C.g:439:4: ( statement )+
                cnt66 = 0
                while True: #loop66
                    alt66 = 2
                    LA66_0 = self.input.LA(1)

                    if ((IDENTIFIER <= LA66_0 <= FLOATING_POINT_LITERAL) or LA66_0 == 24 or LA66_0 == 40 or LA66_0 == 48 or LA66_0 == 52 or (54 <= LA66_0 <= 55) or (58 <= LA66_0 <= 60) or (63 <= LA66_0 <= 65) or (89 <= LA66_0 <= 91) or (93 <= LA66_0 <= 100)) :
                        alt66 = 1


                    if alt66 == 1:
                        # C.g:0:0: statement
                        self.following.append(self.FOLLOW_statement_in_statement_list1876)
                        self.statement()
                        self.following.pop()
                        if self.failed:
                            return 


                    else:
                        if cnt66 >= 1:
                            break #loop66

                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        eee = EarlyExitException(66, self.input)
                        raise eee

                    cnt66 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 62, statement_list_StartIndex)

            pass

        return 

    # $ANTLR end statement_list


    # $ANTLR start expression_statement
    # C.g:442:1: expression_statement : ( ';' | expression ';' );
    def expression_statement(self, ):

        expression_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 63):
                    return 

                # C.g:443:2: ( ';' | expression ';' )
                alt67 = 2
                LA67_0 = self.input.LA(1)

                if (LA67_0 == 24) :
                    alt67 = 1
                elif ((IDENTIFIER <= LA67_0 <= FLOATING_POINT_LITERAL) or LA67_0 == 48 or LA67_0 == 52 or (54 <= LA67_0 <= 55) or (58 <= LA67_0 <= 60) or (63 <= LA67_0 <= 65)) :
                    alt67 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("442:1: expression_statement : ( ';' | expression ';' );", 67, 0, self.input)

                    raise nvae

                if alt67 == 1:
                    # C.g:443:4: ';'
                    self.match(self.input, 24, self.FOLLOW_24_in_expression_statement1888)
                    if self.failed:
                        return 


                elif alt67 == 2:
                    # C.g:444:4: expression ';'
                    self.following.append(self.FOLLOW_expression_in_expression_statement1893)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_expression_statement1895)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 63, expression_statement_StartIndex)

            pass

        return 

    # $ANTLR end expression_statement


    # $ANTLR start selection_statement
    # C.g:447:1: selection_statement : ( 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )? | 'switch' '(' expression ')' statement );
    def selection_statement(self, ):

        selection_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 64):
                    return 

                # C.g:448:2: ( 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )? | 'switch' '(' expression ')' statement )
                alt69 = 2
                LA69_0 = self.input.LA(1)

                if (LA69_0 == 91) :
                    alt69 = 1
                elif (LA69_0 == 93) :
                    alt69 = 2
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("447:1: selection_statement : ( 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )? | 'switch' '(' expression ')' statement );", 69, 0, self.input)

                    raise nvae

                if alt69 == 1:
                    # C.g:448:4: 'if' '(' expression ')' statement ( options {k=1; backtrack=false; } : 'else' statement )?
                    self.match(self.input, 91, self.FOLLOW_91_in_selection_statement1906)
                    if self.failed:
                        return 
                    self.match(self.input, 48, self.FOLLOW_48_in_selection_statement1908)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_selection_statement1910)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_selection_statement1912)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_selection_statement1914)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:448:38: ( options {k=1; backtrack=false; } : 'else' statement )?
                    alt68 = 2
                    LA68_0 = self.input.LA(1)

                    if (LA68_0 == 92) :
                        alt68 = 1
                    if alt68 == 1:
                        # C.g:448:71: 'else' statement
                        self.match(self.input, 92, self.FOLLOW_92_in_selection_statement1929)
                        if self.failed:
                            return 
                        self.following.append(self.FOLLOW_statement_in_selection_statement1931)
                        self.statement()
                        self.following.pop()
                        if self.failed:
                            return 





                elif alt69 == 2:
                    # C.g:449:4: 'switch' '(' expression ')' statement
                    self.match(self.input, 93, self.FOLLOW_93_in_selection_statement1938)
                    if self.failed:
                        return 
                    self.match(self.input, 48, self.FOLLOW_48_in_selection_statement1940)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_selection_statement1942)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_selection_statement1944)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_selection_statement1946)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 64, selection_statement_StartIndex)

            pass

        return 

    # $ANTLR end selection_statement


    # $ANTLR start iteration_statement
    # C.g:452:1: iteration_statement : ( 'while' '(' expression ')' statement | 'do' statement 'while' '(' expression ')' ';' | 'for' '(' expression_statement expression_statement ( expression )? ')' statement );
    def iteration_statement(self, ):

        iteration_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 65):
                    return 

                # C.g:453:2: ( 'while' '(' expression ')' statement | 'do' statement 'while' '(' expression ')' ';' | 'for' '(' expression_statement expression_statement ( expression )? ')' statement )
                alt71 = 3
                LA71 = self.input.LA(1)
                if LA71 == 94:
                    alt71 = 1
                elif LA71 == 95:
                    alt71 = 2
                elif LA71 == 96:
                    alt71 = 3
                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("452:1: iteration_statement : ( 'while' '(' expression ')' statement | 'do' statement 'while' '(' expression ')' ';' | 'for' '(' expression_statement expression_statement ( expression )? ')' statement );", 71, 0, self.input)

                    raise nvae

                if alt71 == 1:
                    # C.g:453:4: 'while' '(' expression ')' statement
                    self.match(self.input, 94, self.FOLLOW_94_in_iteration_statement1957)
                    if self.failed:
                        return 
                    self.match(self.input, 48, self.FOLLOW_48_in_iteration_statement1959)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_iteration_statement1961)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_iteration_statement1963)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_iteration_statement1965)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 


                elif alt71 == 2:
                    # C.g:454:4: 'do' statement 'while' '(' expression ')' ';'
                    self.match(self.input, 95, self.FOLLOW_95_in_iteration_statement1970)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_iteration_statement1972)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 94, self.FOLLOW_94_in_iteration_statement1974)
                    if self.failed:
                        return 
                    self.match(self.input, 48, self.FOLLOW_48_in_iteration_statement1976)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_iteration_statement1978)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 49, self.FOLLOW_49_in_iteration_statement1980)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_iteration_statement1982)
                    if self.failed:
                        return 


                elif alt71 == 3:
                    # C.g:455:4: 'for' '(' expression_statement expression_statement ( expression )? ')' statement
                    self.match(self.input, 96, self.FOLLOW_96_in_iteration_statement1987)
                    if self.failed:
                        return 
                    self.match(self.input, 48, self.FOLLOW_48_in_iteration_statement1989)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_statement_in_iteration_statement1991)
                    self.expression_statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_statement_in_iteration_statement1993)
                    self.expression_statement()
                    self.following.pop()
                    if self.failed:
                        return 
                    # C.g:455:56: ( expression )?
                    alt70 = 2
                    LA70_0 = self.input.LA(1)

                    if ((IDENTIFIER <= LA70_0 <= FLOATING_POINT_LITERAL) or LA70_0 == 48 or LA70_0 == 52 or (54 <= LA70_0 <= 55) or (58 <= LA70_0 <= 60) or (63 <= LA70_0 <= 65)) :
                        alt70 = 1
                    if alt70 == 1:
                        # C.g:0:0: expression
                        self.following.append(self.FOLLOW_expression_in_iteration_statement1995)
                        self.expression()
                        self.following.pop()
                        if self.failed:
                            return 



                    self.match(self.input, 49, self.FOLLOW_49_in_iteration_statement1998)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_statement_in_iteration_statement2000)
                    self.statement()
                    self.following.pop()
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 65, iteration_statement_StartIndex)

            pass

        return 

    # $ANTLR end iteration_statement


    # $ANTLR start jump_statement
    # C.g:458:1: jump_statement : ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' );
    def jump_statement(self, ):

        jump_statement_StartIndex = self.input.index()
        try:
            try:
                if self.backtracking > 0 and self.alreadyParsedRule(self.input, 66):
                    return 

                # C.g:459:2: ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' )
                alt72 = 5
                LA72 = self.input.LA(1)
                if LA72 == 97:
                    alt72 = 1
                elif LA72 == 98:
                    alt72 = 2
                elif LA72 == 99:
                    alt72 = 3
                elif LA72 == 100:
                    LA72_4 = self.input.LA(2)

                    if (LA72_4 == 24) :
                        alt72 = 4
                    elif ((IDENTIFIER <= LA72_4 <= FLOATING_POINT_LITERAL) or LA72_4 == 48 or LA72_4 == 52 or (54 <= LA72_4 <= 55) or (58 <= LA72_4 <= 60) or (63 <= LA72_4 <= 65)) :
                        alt72 = 5
                    else:
                        if self.backtracking > 0:
                            self.failed = True
                            return 

                        nvae = NoViableAltException("458:1: jump_statement : ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' );", 72, 4, self.input)

                        raise nvae

                else:
                    if self.backtracking > 0:
                        self.failed = True
                        return 

                    nvae = NoViableAltException("458:1: jump_statement : ( 'goto' IDENTIFIER ';' | 'continue' ';' | 'break' ';' | 'return' ';' | 'return' expression ';' );", 72, 0, self.input)

                    raise nvae

                if alt72 == 1:
                    # C.g:459:4: 'goto' IDENTIFIER ';'
                    self.match(self.input, 97, self.FOLLOW_97_in_jump_statement2011)
                    if self.failed:
                        return 
                    self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_jump_statement2013)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2015)
                    if self.failed:
                        return 


                elif alt72 == 2:
                    # C.g:460:4: 'continue' ';'
                    self.match(self.input, 98, self.FOLLOW_98_in_jump_statement2020)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2022)
                    if self.failed:
                        return 


                elif alt72 == 3:
                    # C.g:461:4: 'break' ';'
                    self.match(self.input, 99, self.FOLLOW_99_in_jump_statement2027)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2029)
                    if self.failed:
                        return 


                elif alt72 == 4:
                    # C.g:462:4: 'return' ';'
                    self.match(self.input, 100, self.FOLLOW_100_in_jump_statement2034)
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2036)
                    if self.failed:
                        return 


                elif alt72 == 5:
                    # C.g:463:4: 'return' expression ';'
                    self.match(self.input, 100, self.FOLLOW_100_in_jump_statement2041)
                    if self.failed:
                        return 
                    self.following.append(self.FOLLOW_expression_in_jump_statement2043)
                    self.expression()
                    self.following.pop()
                    if self.failed:
                        return 
                    self.match(self.input, 24, self.FOLLOW_24_in_jump_statement2045)
                    if self.failed:
                        return 



            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:
            if self.backtracking > 0:
                self.memoize(self.input, 66, jump_statement_StartIndex)

            pass

        return 

    # $ANTLR end jump_statement

    # $ANTLR start synpred2
    def synpred2_fragment(self, ):
        # C.g:79:6: ( declaration_specifiers )
        # C.g:79:6: declaration_specifiers
        self.following.append(self.FOLLOW_declaration_specifiers_in_synpred2100)
        self.declaration_specifiers()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred2



    # $ANTLR start synpred4
    def synpred4_fragment(self, ):
        # C.g:79:4: ( ( declaration_specifiers )? declarator ( declaration )* '{' )
        # C.g:79:6: ( declaration_specifiers )? declarator ( declaration )* '{'
        # C.g:79:6: ( declaration_specifiers )?
        alt73 = 2
        LA73_0 = self.input.LA(1)

        if ((27 <= LA73_0 <= 39) or (42 <= LA73_0 <= 43) or (45 <= LA73_0 <= 47)) :
            alt73 = 1
        elif (LA73_0 == IDENTIFIER) :
            LA73 = self.input.LA(2)
            if LA73 == 52:
                alt73 = 1
            elif LA73 == IDENTIFIER:
                LA73_18 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 48:
                LA73_19 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 27 or LA73 == 28 or LA73 == 29 or LA73 == 30:
                LA73_20 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 31:
                LA73_21 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 32:
                LA73_22 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 33:
                LA73_23 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 34:
                LA73_24 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 35:
                LA73_25 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 36:
                LA73_26 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 37:
                LA73_27 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 38:
                LA73_28 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 39:
                LA73_29 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 42 or LA73 == 43:
                LA73_30 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 45:
                LA73_31 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
            elif LA73 == 46 or LA73 == 47:
                LA73_32 = self.input.LA(3)

                if ((self.synpred2() and self.isTypeName(self.input.LT(1).text))) :
                    alt73 = 1
        if alt73 == 1:
            # C.g:0:0: declaration_specifiers
            self.following.append(self.FOLLOW_declaration_specifiers_in_synpred4100)
            self.declaration_specifiers()
            self.following.pop()
            if self.failed:
                return 



        self.following.append(self.FOLLOW_declarator_in_synpred4103)
        self.declarator()
        self.following.pop()
        if self.failed:
            return 
        # C.g:79:41: ( declaration )*
        while True: #loop74
            alt74 = 2
            LA74_0 = self.input.LA(1)

            if (LA74_0 == IDENTIFIER or LA74_0 == 23 or (27 <= LA74_0 <= 39) or (42 <= LA74_0 <= 43) or (45 <= LA74_0 <= 47)) :
                alt74 = 1


            if alt74 == 1:
                # C.g:0:0: declaration
                self.following.append(self.FOLLOW_declaration_in_synpred4105)
                self.declaration()
                self.following.pop()
                if self.failed:
                    return 


            else:
                break #loop74


        self.match(self.input, 40, self.FOLLOW_40_in_synpred4108)
        if self.failed:
            return 


    # $ANTLR end synpred4



    # $ANTLR start synpred5
    def synpred5_fragment(self, ):
        # C.g:88:4: ( declaration_specifiers )
        # C.g:88:4: declaration_specifiers
        self.following.append(self.FOLLOW_declaration_specifiers_in_synpred5140)
        self.declaration_specifiers()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred5



    # $ANTLR start synpred8
    def synpred8_fragment(self, ):
        # C.g:101:14: ( declaration_specifiers )
        # C.g:101:14: declaration_specifiers
        self.following.append(self.FOLLOW_declaration_specifiers_in_synpred8189)
        self.declaration_specifiers()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred8



    # $ANTLR start synpred12
    def synpred12_fragment(self, ):
        # C.g:108:7: ( type_specifier )
        # C.g:108:7: type_specifier
        self.following.append(self.FOLLOW_type_specifier_in_synpred12235)
        self.type_specifier()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred12



    # $ANTLR start synpred35
    def synpred35_fragment(self, ):
        # C.g:172:23: ( type_specifier )
        # C.g:172:23: type_specifier
        self.following.append(self.FOLLOW_type_specifier_in_synpred35515)
        self.type_specifier()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred35



    # $ANTLR start synpred45
    def synpred45_fragment(self, ):
        # C.g:205:4: ( ( pointer )? direct_declarator )
        # C.g:205:4: ( pointer )? direct_declarator
        # C.g:205:4: ( pointer )?
        alt79 = 2
        LA79_0 = self.input.LA(1)

        if (LA79_0 == 52) :
            alt79 = 1
        if alt79 == 1:
            # C.g:0:0: pointer
            self.following.append(self.FOLLOW_pointer_in_synpred45668)
            self.pointer()
            self.following.pop()
            if self.failed:
                return 



        self.following.append(self.FOLLOW_direct_declarator_in_synpred45671)
        self.direct_declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred45



    # $ANTLR start synpred47
    def synpred47_fragment(self, ):
        # C.g:218:9: ( declarator_suffix )
        # C.g:218:9: declarator_suffix
        self.following.append(self.FOLLOW_declarator_suffix_in_synpred47720)
        self.declarator_suffix()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred47



    # $ANTLR start synpred50
    def synpred50_fragment(self, ):
        # C.g:224:9: ( '(' parameter_type_list ')' )
        # C.g:224:9: '(' parameter_type_list ')'
        self.match(self.input, 48, self.FOLLOW_48_in_synpred50760)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_parameter_type_list_in_synpred50762)
        self.parameter_type_list()
        self.following.pop()
        if self.failed:
            return 
        self.match(self.input, 49, self.FOLLOW_49_in_synpred50764)
        if self.failed:
            return 


    # $ANTLR end synpred50



    # $ANTLR start synpred51
    def synpred51_fragment(self, ):
        # C.g:225:9: ( '(' identifier_list ')' )
        # C.g:225:9: '(' identifier_list ')'
        self.match(self.input, 48, self.FOLLOW_48_in_synpred51774)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_identifier_list_in_synpred51776)
        self.identifier_list()
        self.following.pop()
        if self.failed:
            return 
        self.match(self.input, 49, self.FOLLOW_49_in_synpred51778)
        if self.failed:
            return 


    # $ANTLR end synpred51



    # $ANTLR start synpred52
    def synpred52_fragment(self, ):
        # C.g:230:8: ( type_qualifier )
        # C.g:230:8: type_qualifier
        self.following.append(self.FOLLOW_type_qualifier_in_synpred52803)
        self.type_qualifier()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred52



    # $ANTLR start synpred53
    def synpred53_fragment(self, ):
        # C.g:230:24: ( pointer )
        # C.g:230:24: pointer
        self.following.append(self.FOLLOW_pointer_in_synpred53806)
        self.pointer()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred53



    # $ANTLR start synpred54
    def synpred54_fragment(self, ):
        # C.g:230:4: ( '*' ( type_qualifier )+ ( pointer )? )
        # C.g:230:4: '*' ( type_qualifier )+ ( pointer )?
        self.match(self.input, 52, self.FOLLOW_52_in_synpred54801)
        if self.failed:
            return 
        # C.g:230:8: ( type_qualifier )+
        cnt80 = 0
        while True: #loop80
            alt80 = 2
            LA80_0 = self.input.LA(1)

            if ((46 <= LA80_0 <= 47)) :
                alt80 = 1


            if alt80 == 1:
                # C.g:0:0: type_qualifier
                self.following.append(self.FOLLOW_type_qualifier_in_synpred54803)
                self.type_qualifier()
                self.following.pop()
                if self.failed:
                    return 


            else:
                if cnt80 >= 1:
                    break #loop80

                if self.backtracking > 0:
                    self.failed = True
                    return 

                eee = EarlyExitException(80, self.input)
                raise eee

            cnt80 += 1


        # C.g:230:24: ( pointer )?
        alt81 = 2
        LA81_0 = self.input.LA(1)

        if (LA81_0 == 52) :
            alt81 = 1
        if alt81 == 1:
            # C.g:0:0: pointer
            self.following.append(self.FOLLOW_pointer_in_synpred54806)
            self.pointer()
            self.following.pop()
            if self.failed:
                return 





    # $ANTLR end synpred54



    # $ANTLR start synpred55
    def synpred55_fragment(self, ):
        # C.g:231:4: ( '*' pointer )
        # C.g:231:4: '*' pointer
        self.match(self.input, 52, self.FOLLOW_52_in_synpred55812)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_pointer_in_synpred55814)
        self.pointer()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred55



    # $ANTLR start synpred58
    def synpred58_fragment(self, ):
        # C.g:244:28: ( declarator )
        # C.g:244:28: declarator
        self.following.append(self.FOLLOW_declarator_in_synpred58869)
        self.declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred58



    # $ANTLR start synpred59
    def synpred59_fragment(self, ):
        # C.g:244:39: ( abstract_declarator )
        # C.g:244:39: abstract_declarator
        self.following.append(self.FOLLOW_abstract_declarator_in_synpred59871)
        self.abstract_declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred59



    # $ANTLR start synpred62
    def synpred62_fragment(self, ):
        # C.g:256:12: ( direct_abstract_declarator )
        # C.g:256:12: direct_abstract_declarator
        self.following.append(self.FOLLOW_direct_abstract_declarator_in_synpred62918)
        self.direct_abstract_declarator()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred62



    # $ANTLR start synpred65
    def synpred65_fragment(self, ):
        # C.g:261:65: ( abstract_declarator_suffix )
        # C.g:261:65: abstract_declarator_suffix
        self.following.append(self.FOLLOW_abstract_declarator_suffix_in_synpred65949)
        self.abstract_declarator_suffix()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred65



    # $ANTLR start synpred78
    def synpred78_fragment(self, ):
        # C.g:295:4: ( '(' type_name ')' cast_expression )
        # C.g:295:4: '(' type_name ')' cast_expression
        self.match(self.input, 48, self.FOLLOW_48_in_synpred781121)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_type_name_in_synpred781123)
        self.type_name()
        self.following.pop()
        if self.failed:
            return 
        self.match(self.input, 49, self.FOLLOW_49_in_synpred781125)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_cast_expression_in_synpred781127)
        self.cast_expression()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred78



    # $ANTLR start synpred83
    def synpred83_fragment(self, ):
        # C.g:304:4: ( 'sizeof' unary_expression )
        # C.g:304:4: 'sizeof' unary_expression
        self.match(self.input, 60, self.FOLLOW_60_in_synpred831169)
        if self.failed:
            return 
        self.following.append(self.FOLLOW_unary_expression_in_synpred831171)
        self.unary_expression()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred83



    # $ANTLR start synpred88
    def synpred88_fragment(self, ):
        # C.g:314:13: ( '*' IDENTIFIER )
        # C.g:314:13: '*' IDENTIFIER
        self.match(self.input, 52, self.FOLLOW_52_in_synpred881277)
        if self.failed:
            return 
        self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_synpred881279)
        if self.failed:
            return 


    # $ANTLR end synpred88



    # $ANTLR start synpred105
    def synpred105_fragment(self, ):
        # C.g:356:4: ( lvalue assignment_operator assignment_expression )
        # C.g:356:4: lvalue assignment_operator assignment_expression
        self.following.append(self.FOLLOW_lvalue_in_synpred1051499)
        self.lvalue()
        self.following.pop()
        if self.failed:
            return 
        self.following.append(self.FOLLOW_assignment_operator_in_synpred1051501)
        self.assignment_operator()
        self.following.pop()
        if self.failed:
            return 
        self.following.append(self.FOLLOW_assignment_expression_in_synpred1051503)
        self.assignment_expression()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred105



    # $ANTLR start synpred137
    def synpred137_fragment(self, ):
        # C.g:435:8: ( declaration )
        # C.g:435:8: declaration
        self.following.append(self.FOLLOW_declaration_in_synpred1371859)
        self.declaration()
        self.following.pop()
        if self.failed:
            return 


    # $ANTLR end synpred137



    def synpred35(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred35_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred59(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred59_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred58(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred58_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred45(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred45_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred83(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred83_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred65(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred65_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred47(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred47_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred137(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred137_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred55(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred55_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred54(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred54_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred78(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred78_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred62(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred62_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred5(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred5_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred53(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred53_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred88(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred88_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred52(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred52_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred51(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred51_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred8(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred8_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred50(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred50_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred105(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred105_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred2(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred2_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred4(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred4_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success

    def synpred12(self):
        self.backtracking += 1
        start = self.input.mark()
        self.synpred12_fragment()
        success = not self.failed
        self.input.rewind(start)
        self.backtracking -= 1
        self.failed = False
        return success



 

    FOLLOW_external_declaration_in_translation_unit77 = frozenset([1, 4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 52])
    FOLLOW_function_definition_in_external_declaration113 = frozenset([1])
    FOLLOW_declaration_in_external_declaration118 = frozenset([1])
    FOLLOW_declaration_specifiers_in_function_definition140 = frozenset([4, 48, 52])
    FOLLOW_declarator_in_function_definition143 = frozenset([4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47])
    FOLLOW_declaration_in_function_definition149 = frozenset([4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47])
    FOLLOW_compound_statement_in_function_definition152 = frozenset([1])
    FOLLOW_compound_statement_in_function_definition159 = frozenset([1])
    FOLLOW_23_in_declaration187 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48, 52])
    FOLLOW_declaration_specifiers_in_declaration189 = frozenset([4, 48, 52])
    FOLLOW_init_declarator_list_in_declaration197 = frozenset([24])
    FOLLOW_24_in_declaration199 = frozenset([1])
    FOLLOW_declaration_specifiers_in_declaration205 = frozenset([4, 24, 48, 52])
    FOLLOW_init_declarator_list_in_declaration207 = frozenset([24])
    FOLLOW_24_in_declaration210 = frozenset([1])
    FOLLOW_storage_class_specifier_in_declaration_specifiers227 = frozenset([1, 4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_type_specifier_in_declaration_specifiers235 = frozenset([1, 4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_type_qualifier_in_declaration_specifiers249 = frozenset([1, 4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_init_declarator_in_init_declarator_list271 = frozenset([1, 25])
    FOLLOW_25_in_init_declarator_list274 = frozenset([4, 48, 52])
    FOLLOW_init_declarator_in_init_declarator_list276 = frozenset([1, 25])
    FOLLOW_declarator_in_init_declarator289 = frozenset([1, 26])
    FOLLOW_26_in_init_declarator292 = frozenset([4, 5, 6, 7, 8, 9, 10, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_initializer_in_init_declarator294 = frozenset([1])
    FOLLOW_set_in_storage_class_specifier0 = frozenset([1])
    FOLLOW_31_in_type_specifier333 = frozenset([1])
    FOLLOW_32_in_type_specifier338 = frozenset([1])
    FOLLOW_33_in_type_specifier343 = frozenset([1])
    FOLLOW_34_in_type_specifier348 = frozenset([1])
    FOLLOW_35_in_type_specifier353 = frozenset([1])
    FOLLOW_36_in_type_specifier358 = frozenset([1])
    FOLLOW_37_in_type_specifier363 = frozenset([1])
    FOLLOW_38_in_type_specifier368 = frozenset([1])
    FOLLOW_39_in_type_specifier373 = frozenset([1])
    FOLLOW_struct_or_union_specifier_in_type_specifier378 = frozenset([1])
    FOLLOW_enum_specifier_in_type_specifier383 = frozenset([1])
    FOLLOW_type_id_in_type_specifier388 = frozenset([1])
    FOLLOW_IDENTIFIER_in_type_id406 = frozenset([1])
    FOLLOW_struct_or_union_in_struct_or_union_specifier439 = frozenset([4, 40])
    FOLLOW_IDENTIFIER_in_struct_or_union_specifier441 = frozenset([40])
    FOLLOW_40_in_struct_or_union_specifier444 = frozenset([4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_struct_declaration_list_in_struct_or_union_specifier446 = frozenset([41])
    FOLLOW_41_in_struct_or_union_specifier448 = frozenset([1])
    FOLLOW_struct_or_union_in_struct_or_union_specifier453 = frozenset([4])
    FOLLOW_IDENTIFIER_in_struct_or_union_specifier455 = frozenset([1])
    FOLLOW_set_in_struct_or_union0 = frozenset([1])
    FOLLOW_struct_declaration_in_struct_declaration_list482 = frozenset([1, 4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_specifier_qualifier_list_in_struct_declaration494 = frozenset([4, 44, 48, 52])
    FOLLOW_struct_declarator_list_in_struct_declaration496 = frozenset([24])
    FOLLOW_24_in_struct_declaration498 = frozenset([1])
    FOLLOW_type_qualifier_in_specifier_qualifier_list511 = frozenset([1, 4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_type_specifier_in_specifier_qualifier_list515 = frozenset([1, 4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_struct_declarator_in_struct_declarator_list529 = frozenset([1, 25])
    FOLLOW_25_in_struct_declarator_list532 = frozenset([4, 44, 48, 52])
    FOLLOW_struct_declarator_in_struct_declarator_list534 = frozenset([1, 25])
    FOLLOW_declarator_in_struct_declarator547 = frozenset([1, 44])
    FOLLOW_44_in_struct_declarator550 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_constant_expression_in_struct_declarator552 = frozenset([1])
    FOLLOW_44_in_struct_declarator559 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_constant_expression_in_struct_declarator561 = frozenset([1])
    FOLLOW_45_in_enum_specifier579 = frozenset([40])
    FOLLOW_40_in_enum_specifier581 = frozenset([4])
    FOLLOW_enumerator_list_in_enum_specifier583 = frozenset([41])
    FOLLOW_41_in_enum_specifier585 = frozenset([1])
    FOLLOW_45_in_enum_specifier590 = frozenset([4])
    FOLLOW_IDENTIFIER_in_enum_specifier592 = frozenset([40])
    FOLLOW_40_in_enum_specifier594 = frozenset([4])
    FOLLOW_enumerator_list_in_enum_specifier596 = frozenset([41])
    FOLLOW_41_in_enum_specifier598 = frozenset([1])
    FOLLOW_45_in_enum_specifier603 = frozenset([4])
    FOLLOW_IDENTIFIER_in_enum_specifier605 = frozenset([1])
    FOLLOW_enumerator_in_enumerator_list616 = frozenset([1, 25])
    FOLLOW_25_in_enumerator_list619 = frozenset([4])
    FOLLOW_enumerator_in_enumerator_list621 = frozenset([1, 25])
    FOLLOW_IDENTIFIER_in_enumerator634 = frozenset([1, 26])
    FOLLOW_26_in_enumerator637 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_constant_expression_in_enumerator639 = frozenset([1])
    FOLLOW_set_in_type_qualifier0 = frozenset([1])
    FOLLOW_pointer_in_declarator668 = frozenset([4, 48])
    FOLLOW_direct_declarator_in_declarator671 = frozenset([1])
    FOLLOW_pointer_in_declarator676 = frozenset([1])
    FOLLOW_IDENTIFIER_in_direct_declarator691 = frozenset([1, 48, 50])
    FOLLOW_48_in_direct_declarator702 = frozenset([4, 48, 52])
    FOLLOW_declarator_in_direct_declarator704 = frozenset([49])
    FOLLOW_49_in_direct_declarator706 = frozenset([1, 48, 50])
    FOLLOW_declarator_suffix_in_direct_declarator720 = frozenset([1, 48, 50])
    FOLLOW_50_in_declarator_suffix734 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_constant_expression_in_declarator_suffix736 = frozenset([51])
    FOLLOW_51_in_declarator_suffix738 = frozenset([1])
    FOLLOW_50_in_declarator_suffix748 = frozenset([51])
    FOLLOW_51_in_declarator_suffix750 = frozenset([1])
    FOLLOW_48_in_declarator_suffix760 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_parameter_type_list_in_declarator_suffix762 = frozenset([49])
    FOLLOW_49_in_declarator_suffix764 = frozenset([1])
    FOLLOW_48_in_declarator_suffix774 = frozenset([4])
    FOLLOW_identifier_list_in_declarator_suffix776 = frozenset([49])
    FOLLOW_49_in_declarator_suffix778 = frozenset([1])
    FOLLOW_48_in_declarator_suffix788 = frozenset([49])
    FOLLOW_49_in_declarator_suffix790 = frozenset([1])
    FOLLOW_52_in_pointer801 = frozenset([46, 47])
    FOLLOW_type_qualifier_in_pointer803 = frozenset([1, 46, 47, 52])
    FOLLOW_pointer_in_pointer806 = frozenset([1])
    FOLLOW_52_in_pointer812 = frozenset([52])
    FOLLOW_pointer_in_pointer814 = frozenset([1])
    FOLLOW_52_in_pointer819 = frozenset([1])
    FOLLOW_parameter_list_in_parameter_type_list830 = frozenset([1, 25])
    FOLLOW_25_in_parameter_type_list833 = frozenset([53])
    FOLLOW_53_in_parameter_type_list835 = frozenset([1])
    FOLLOW_parameter_declaration_in_parameter_list848 = frozenset([1, 25])
    FOLLOW_25_in_parameter_list851 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_parameter_declaration_in_parameter_list853 = frozenset([1, 25])
    FOLLOW_declaration_specifiers_in_parameter_declaration866 = frozenset([1, 4, 48, 50, 52])
    FOLLOW_declarator_in_parameter_declaration869 = frozenset([1, 4, 48, 50, 52])
    FOLLOW_abstract_declarator_in_parameter_declaration871 = frozenset([1, 4, 48, 50, 52])
    FOLLOW_IDENTIFIER_in_identifier_list884 = frozenset([1, 25])
    FOLLOW_25_in_identifier_list887 = frozenset([4])
    FOLLOW_IDENTIFIER_in_identifier_list889 = frozenset([1, 25])
    FOLLOW_specifier_qualifier_list_in_type_name902 = frozenset([1, 48, 50, 52])
    FOLLOW_abstract_declarator_in_type_name904 = frozenset([1])
    FOLLOW_pointer_in_abstract_declarator916 = frozenset([1, 48, 50])
    FOLLOW_direct_abstract_declarator_in_abstract_declarator918 = frozenset([1])
    FOLLOW_direct_abstract_declarator_in_abstract_declarator924 = frozenset([1])
    FOLLOW_48_in_direct_abstract_declarator937 = frozenset([48, 50, 52])
    FOLLOW_abstract_declarator_in_direct_abstract_declarator939 = frozenset([49])
    FOLLOW_49_in_direct_abstract_declarator941 = frozenset([1, 48, 50])
    FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator945 = frozenset([1, 48, 50])
    FOLLOW_abstract_declarator_suffix_in_direct_abstract_declarator949 = frozenset([1, 48, 50])
    FOLLOW_50_in_abstract_declarator_suffix961 = frozenset([51])
    FOLLOW_51_in_abstract_declarator_suffix963 = frozenset([1])
    FOLLOW_50_in_abstract_declarator_suffix968 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_constant_expression_in_abstract_declarator_suffix970 = frozenset([51])
    FOLLOW_51_in_abstract_declarator_suffix972 = frozenset([1])
    FOLLOW_48_in_abstract_declarator_suffix977 = frozenset([49])
    FOLLOW_49_in_abstract_declarator_suffix979 = frozenset([1])
    FOLLOW_48_in_abstract_declarator_suffix984 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_parameter_type_list_in_abstract_declarator_suffix986 = frozenset([49])
    FOLLOW_49_in_abstract_declarator_suffix988 = frozenset([1])
    FOLLOW_assignment_expression_in_initializer1000 = frozenset([1])
    FOLLOW_40_in_initializer1005 = frozenset([4, 5, 6, 7, 8, 9, 10, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_initializer_list_in_initializer1007 = frozenset([25, 41])
    FOLLOW_25_in_initializer1009 = frozenset([41])
    FOLLOW_41_in_initializer1012 = frozenset([1])
    FOLLOW_initializer_in_initializer_list1023 = frozenset([1, 25])
    FOLLOW_25_in_initializer_list1026 = frozenset([4, 5, 6, 7, 8, 9, 10, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_initializer_in_initializer_list1028 = frozenset([1, 25])
    FOLLOW_assignment_expression_in_argument_expression_list1045 = frozenset([1, 25])
    FOLLOW_25_in_argument_expression_list1048 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_assignment_expression_in_argument_expression_list1050 = frozenset([1, 25])
    FOLLOW_multiplicative_expression_in_additive_expression1064 = frozenset([1, 54, 55])
    FOLLOW_54_in_additive_expression1068 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_multiplicative_expression_in_additive_expression1070 = frozenset([1, 54, 55])
    FOLLOW_55_in_additive_expression1074 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_multiplicative_expression_in_additive_expression1076 = frozenset([1, 54, 55])
    FOLLOW_cast_expression_in_multiplicative_expression1090 = frozenset([1, 52, 56, 57])
    FOLLOW_52_in_multiplicative_expression1094 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_cast_expression_in_multiplicative_expression1096 = frozenset([1, 52, 56, 57])
    FOLLOW_56_in_multiplicative_expression1100 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_cast_expression_in_multiplicative_expression1102 = frozenset([1, 52, 56, 57])
    FOLLOW_57_in_multiplicative_expression1106 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_cast_expression_in_multiplicative_expression1108 = frozenset([1, 52, 56, 57])
    FOLLOW_48_in_cast_expression1121 = frozenset([4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_type_name_in_cast_expression1123 = frozenset([49])
    FOLLOW_49_in_cast_expression1125 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_cast_expression_in_cast_expression1127 = frozenset([1])
    FOLLOW_unary_expression_in_cast_expression1132 = frozenset([1])
    FOLLOW_postfix_expression_in_unary_expression1143 = frozenset([1])
    FOLLOW_58_in_unary_expression1148 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_unary_expression_in_unary_expression1150 = frozenset([1])
    FOLLOW_59_in_unary_expression1155 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_unary_expression_in_unary_expression1157 = frozenset([1])
    FOLLOW_unary_operator_in_unary_expression1162 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_cast_expression_in_unary_expression1164 = frozenset([1])
    FOLLOW_60_in_unary_expression1169 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_unary_expression_in_unary_expression1171 = frozenset([1])
    FOLLOW_60_in_unary_expression1176 = frozenset([48])
    FOLLOW_48_in_unary_expression1178 = frozenset([4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_type_name_in_unary_expression1180 = frozenset([49])
    FOLLOW_49_in_unary_expression1182 = frozenset([1])
    FOLLOW_primary_expression_in_postfix_expression1195 = frozenset([1, 48, 50, 52, 58, 59, 61, 62])
    FOLLOW_50_in_postfix_expression1209 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_in_postfix_expression1211 = frozenset([51])
    FOLLOW_51_in_postfix_expression1213 = frozenset([1, 48, 50, 52, 58, 59, 61, 62])
    FOLLOW_48_in_postfix_expression1227 = frozenset([49])
    FOLLOW_49_in_postfix_expression1229 = frozenset([1, 48, 50, 52, 58, 59, 61, 62])
    FOLLOW_48_in_postfix_expression1243 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_argument_expression_list_in_postfix_expression1245 = frozenset([49])
    FOLLOW_49_in_postfix_expression1247 = frozenset([1, 48, 50, 52, 58, 59, 61, 62])
    FOLLOW_61_in_postfix_expression1261 = frozenset([4])
    FOLLOW_IDENTIFIER_in_postfix_expression1263 = frozenset([1, 48, 50, 52, 58, 59, 61, 62])
    FOLLOW_52_in_postfix_expression1277 = frozenset([4])
    FOLLOW_IDENTIFIER_in_postfix_expression1279 = frozenset([1, 48, 50, 52, 58, 59, 61, 62])
    FOLLOW_62_in_postfix_expression1293 = frozenset([4])
    FOLLOW_IDENTIFIER_in_postfix_expression1295 = frozenset([1, 48, 50, 52, 58, 59, 61, 62])
    FOLLOW_58_in_postfix_expression1309 = frozenset([1, 48, 50, 52, 58, 59, 61, 62])
    FOLLOW_59_in_postfix_expression1323 = frozenset([1, 48, 50, 52, 58, 59, 61, 62])
    FOLLOW_set_in_unary_operator0 = frozenset([1])
    FOLLOW_IDENTIFIER_in_primary_expression1381 = frozenset([1])
    FOLLOW_constant_in_primary_expression1386 = frozenset([1])
    FOLLOW_48_in_primary_expression1391 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_in_primary_expression1393 = frozenset([49])
    FOLLOW_49_in_primary_expression1395 = frozenset([1])
    FOLLOW_set_in_constant0 = frozenset([1])
    FOLLOW_assignment_expression_in_expression1470 = frozenset([1, 25])
    FOLLOW_25_in_expression1473 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_assignment_expression_in_expression1475 = frozenset([1, 25])
    FOLLOW_conditional_expression_in_constant_expression1488 = frozenset([1])
    FOLLOW_lvalue_in_assignment_expression1499 = frozenset([26, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75])
    FOLLOW_assignment_operator_in_assignment_expression1501 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_assignment_expression_in_assignment_expression1503 = frozenset([1])
    FOLLOW_conditional_expression_in_assignment_expression1508 = frozenset([1])
    FOLLOW_unary_expression_in_lvalue1520 = frozenset([1])
    FOLLOW_set_in_assignment_operator0 = frozenset([1])
    FOLLOW_logical_or_expression_in_conditional_expression1592 = frozenset([1, 76])
    FOLLOW_76_in_conditional_expression1595 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_in_conditional_expression1597 = frozenset([44])
    FOLLOW_44_in_conditional_expression1599 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_conditional_expression_in_conditional_expression1601 = frozenset([1])
    FOLLOW_logical_and_expression_in_logical_or_expression1614 = frozenset([1, 77])
    FOLLOW_77_in_logical_or_expression1617 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_logical_and_expression_in_logical_or_expression1619 = frozenset([1, 77])
    FOLLOW_inclusive_or_expression_in_logical_and_expression1632 = frozenset([1, 78])
    FOLLOW_78_in_logical_and_expression1635 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_inclusive_or_expression_in_logical_and_expression1637 = frozenset([1, 78])
    FOLLOW_exclusive_or_expression_in_inclusive_or_expression1650 = frozenset([1, 79])
    FOLLOW_79_in_inclusive_or_expression1653 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_exclusive_or_expression_in_inclusive_or_expression1655 = frozenset([1, 79])
    FOLLOW_and_expression_in_exclusive_or_expression1668 = frozenset([1, 80])
    FOLLOW_80_in_exclusive_or_expression1671 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_and_expression_in_exclusive_or_expression1673 = frozenset([1, 80])
    FOLLOW_equality_expression_in_and_expression1686 = frozenset([1, 63])
    FOLLOW_63_in_and_expression1689 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_equality_expression_in_and_expression1691 = frozenset([1, 63])
    FOLLOW_relational_expression_in_equality_expression1703 = frozenset([1, 81, 82])
    FOLLOW_set_in_equality_expression1706 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_relational_expression_in_equality_expression1712 = frozenset([1, 81, 82])
    FOLLOW_shift_expression_in_relational_expression1725 = frozenset([1, 83, 84, 85, 86])
    FOLLOW_set_in_relational_expression1728 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_shift_expression_in_relational_expression1738 = frozenset([1, 83, 84, 85, 86])
    FOLLOW_additive_expression_in_shift_expression1751 = frozenset([1, 87, 88])
    FOLLOW_set_in_shift_expression1754 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_additive_expression_in_shift_expression1760 = frozenset([1, 87, 88])
    FOLLOW_labeled_statement_in_statement1775 = frozenset([1])
    FOLLOW_compound_statement_in_statement1780 = frozenset([1])
    FOLLOW_expression_statement_in_statement1785 = frozenset([1])
    FOLLOW_selection_statement_in_statement1790 = frozenset([1])
    FOLLOW_iteration_statement_in_statement1795 = frozenset([1])
    FOLLOW_jump_statement_in_statement1800 = frozenset([1])
    FOLLOW_IDENTIFIER_in_labeled_statement1811 = frozenset([44])
    FOLLOW_44_in_labeled_statement1813 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_in_labeled_statement1815 = frozenset([1])
    FOLLOW_89_in_labeled_statement1820 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_constant_expression_in_labeled_statement1822 = frozenset([44])
    FOLLOW_44_in_labeled_statement1824 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_in_labeled_statement1826 = frozenset([1])
    FOLLOW_90_in_labeled_statement1831 = frozenset([44])
    FOLLOW_44_in_labeled_statement1833 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_in_labeled_statement1835 = frozenset([1])
    FOLLOW_40_in_compound_statement1857 = frozenset([4, 5, 6, 7, 8, 9, 10, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_declaration_in_compound_statement1859 = frozenset([4, 5, 6, 7, 8, 9, 10, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 47, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_list_in_compound_statement1862 = frozenset([41])
    FOLLOW_41_in_compound_statement1865 = frozenset([1])
    FOLLOW_statement_in_statement_list1876 = frozenset([1, 4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_24_in_expression_statement1888 = frozenset([1])
    FOLLOW_expression_in_expression_statement1893 = frozenset([24])
    FOLLOW_24_in_expression_statement1895 = frozenset([1])
    FOLLOW_91_in_selection_statement1906 = frozenset([48])
    FOLLOW_48_in_selection_statement1908 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_in_selection_statement1910 = frozenset([49])
    FOLLOW_49_in_selection_statement1912 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_in_selection_statement1914 = frozenset([1, 92])
    FOLLOW_92_in_selection_statement1929 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_in_selection_statement1931 = frozenset([1])
    FOLLOW_93_in_selection_statement1938 = frozenset([48])
    FOLLOW_48_in_selection_statement1940 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_in_selection_statement1942 = frozenset([49])
    FOLLOW_49_in_selection_statement1944 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_in_selection_statement1946 = frozenset([1])
    FOLLOW_94_in_iteration_statement1957 = frozenset([48])
    FOLLOW_48_in_iteration_statement1959 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_in_iteration_statement1961 = frozenset([49])
    FOLLOW_49_in_iteration_statement1963 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_in_iteration_statement1965 = frozenset([1])
    FOLLOW_95_in_iteration_statement1970 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_in_iteration_statement1972 = frozenset([94])
    FOLLOW_94_in_iteration_statement1974 = frozenset([48])
    FOLLOW_48_in_iteration_statement1976 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_in_iteration_statement1978 = frozenset([49])
    FOLLOW_49_in_iteration_statement1980 = frozenset([24])
    FOLLOW_24_in_iteration_statement1982 = frozenset([1])
    FOLLOW_96_in_iteration_statement1987 = frozenset([48])
    FOLLOW_48_in_iteration_statement1989 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_statement_in_iteration_statement1991 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_statement_in_iteration_statement1993 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 49, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_in_iteration_statement1995 = frozenset([49])
    FOLLOW_49_in_iteration_statement1998 = frozenset([4, 5, 6, 7, 8, 9, 10, 24, 40, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99, 100])
    FOLLOW_statement_in_iteration_statement2000 = frozenset([1])
    FOLLOW_97_in_jump_statement2011 = frozenset([4])
    FOLLOW_IDENTIFIER_in_jump_statement2013 = frozenset([24])
    FOLLOW_24_in_jump_statement2015 = frozenset([1])
    FOLLOW_98_in_jump_statement2020 = frozenset([24])
    FOLLOW_24_in_jump_statement2022 = frozenset([1])
    FOLLOW_99_in_jump_statement2027 = frozenset([24])
    FOLLOW_24_in_jump_statement2029 = frozenset([1])
    FOLLOW_100_in_jump_statement2034 = frozenset([24])
    FOLLOW_24_in_jump_statement2036 = frozenset([1])
    FOLLOW_100_in_jump_statement2041 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_expression_in_jump_statement2043 = frozenset([24])
    FOLLOW_24_in_jump_statement2045 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred2100 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred4100 = frozenset([4, 48, 52])
    FOLLOW_declarator_in_synpred4103 = frozenset([4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47])
    FOLLOW_declaration_in_synpred4105 = frozenset([4, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47])
    FOLLOW_40_in_synpred4108 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred5140 = frozenset([1])
    FOLLOW_declaration_specifiers_in_synpred8189 = frozenset([1])
    FOLLOW_type_specifier_in_synpred12235 = frozenset([1])
    FOLLOW_type_specifier_in_synpred35515 = frozenset([1])
    FOLLOW_pointer_in_synpred45668 = frozenset([4, 48])
    FOLLOW_direct_declarator_in_synpred45671 = frozenset([1])
    FOLLOW_declarator_suffix_in_synpred47720 = frozenset([1])
    FOLLOW_48_in_synpred50760 = frozenset([4, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_parameter_type_list_in_synpred50762 = frozenset([49])
    FOLLOW_49_in_synpred50764 = frozenset([1])
    FOLLOW_48_in_synpred51774 = frozenset([4])
    FOLLOW_identifier_list_in_synpred51776 = frozenset([49])
    FOLLOW_49_in_synpred51778 = frozenset([1])
    FOLLOW_type_qualifier_in_synpred52803 = frozenset([1])
    FOLLOW_pointer_in_synpred53806 = frozenset([1])
    FOLLOW_52_in_synpred54801 = frozenset([46, 47])
    FOLLOW_type_qualifier_in_synpred54803 = frozenset([1, 46, 47, 52])
    FOLLOW_pointer_in_synpred54806 = frozenset([1])
    FOLLOW_52_in_synpred55812 = frozenset([52])
    FOLLOW_pointer_in_synpred55814 = frozenset([1])
    FOLLOW_declarator_in_synpred58869 = frozenset([1])
    FOLLOW_abstract_declarator_in_synpred59871 = frozenset([1])
    FOLLOW_direct_abstract_declarator_in_synpred62918 = frozenset([1])
    FOLLOW_abstract_declarator_suffix_in_synpred65949 = frozenset([1])
    FOLLOW_48_in_synpred781121 = frozenset([4, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43, 45, 46, 47])
    FOLLOW_type_name_in_synpred781123 = frozenset([49])
    FOLLOW_49_in_synpred781125 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_cast_expression_in_synpred781127 = frozenset([1])
    FOLLOW_60_in_synpred831169 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_unary_expression_in_synpred831171 = frozenset([1])
    FOLLOW_52_in_synpred881277 = frozenset([4])
    FOLLOW_IDENTIFIER_in_synpred881279 = frozenset([1])
    FOLLOW_lvalue_in_synpred1051499 = frozenset([26, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75])
    FOLLOW_assignment_operator_in_synpred1051501 = frozenset([4, 5, 6, 7, 8, 9, 10, 48, 52, 54, 55, 58, 59, 60, 63, 64, 65])
    FOLLOW_assignment_expression_in_synpred1051503 = frozenset([1])
    FOLLOW_declaration_in_synpred1371859 = frozenset([1])

