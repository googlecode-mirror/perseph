# $ANTLR 3.0.1 SimpleCWalker.g 2008-07-31 14:01:38

from antlr3 import *
from antlr3.tree import *
from antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
LT=18
CHAR=15
FOR=13
FUNC_HDR=6
INT=12
FUNC_DEF=8
INT_TYPE=14
ID=10
EOF=-1
FUNC_DECL=7
ARG_DEF=5
WS=20
BLOCK=9
PLUS=19
VOID=16
EQ=11
VAR_DEF=4
EQEQ=17

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "VAR_DEF", "ARG_DEF", "FUNC_HDR", "FUNC_DECL", "FUNC_DEF", "BLOCK", 
    "ID", "EQ", "INT", "FOR", "INT_TYPE", "CHAR", "VOID", "EQEQ", "LT", 
    "PLUS", "WS", "';'", "'('", "','", "')'", "'{'", "'}'"
]



class SimpleCWalker(TreeParser):
    grammarFileName = "SimpleCWalker.g"
    tokenNames = tokenNames

    def __init__(self, input):
        TreeParser.__init__(self, input)



                




    # $ANTLR start program
    # SimpleCWalker.g:8:1: program : ( declaration )+ ;
    def program(self, ):

        try:
            try:
                # SimpleCWalker.g:9:5: ( ( declaration )+ )
                # SimpleCWalker.g:9:9: ( declaration )+
                # SimpleCWalker.g:9:9: ( declaration )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == VAR_DEF or (FUNC_DECL <= LA1_0 <= FUNC_DEF)) :
                        alt1 = 1


                    if alt1 == 1:
                        # SimpleCWalker.g:9:9: declaration
                        self.following.append(self.FOLLOW_declaration_in_program49)
                        self.declaration()
                        self.following.pop()



                    else:
                        if cnt1 >= 1:
                            break #loop1

                        eee = EarlyExitException(1, self.input)
                        raise eee

                    cnt1 += 1






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end program


    # $ANTLR start declaration
    # SimpleCWalker.g:12:1: declaration : ( variable | ^( FUNC_DECL functionHeader ) | ^( FUNC_DEF functionHeader block ) );
    def declaration(self, ):

        try:
            try:
                # SimpleCWalker.g:13:5: ( variable | ^( FUNC_DECL functionHeader ) | ^( FUNC_DEF functionHeader block ) )
                alt2 = 3
                LA2 = self.input.LA(1)
                if LA2 == VAR_DEF:
                    alt2 = 1
                elif LA2 == FUNC_DECL:
                    alt2 = 2
                elif LA2 == FUNC_DEF:
                    alt2 = 3
                else:
                    nvae = NoViableAltException("12:1: declaration : ( variable | ^( FUNC_DECL functionHeader ) | ^( FUNC_DEF functionHeader block ) );", 2, 0, self.input)

                    raise nvae

                if alt2 == 1:
                    # SimpleCWalker.g:13:9: variable
                    self.following.append(self.FOLLOW_variable_in_declaration69)
                    self.variable()
                    self.following.pop()



                elif alt2 == 2:
                    # SimpleCWalker.g:14:9: ^( FUNC_DECL functionHeader )
                    self.match(self.input, FUNC_DECL, self.FOLLOW_FUNC_DECL_in_declaration80)


                    self.match(self.input, DOWN, None)
                    self.following.append(self.FOLLOW_functionHeader_in_declaration82)
                    self.functionHeader()
                    self.following.pop()


                    self.match(self.input, UP, None)



                elif alt2 == 3:
                    # SimpleCWalker.g:15:9: ^( FUNC_DEF functionHeader block )
                    self.match(self.input, FUNC_DEF, self.FOLLOW_FUNC_DEF_in_declaration94)


                    self.match(self.input, DOWN, None)
                    self.following.append(self.FOLLOW_functionHeader_in_declaration96)
                    self.functionHeader()
                    self.following.pop()

                    self.following.append(self.FOLLOW_block_in_declaration98)
                    self.block()
                    self.following.pop()


                    self.match(self.input, UP, None)




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end declaration


    # $ANTLR start variable
    # SimpleCWalker.g:18:1: variable : ^( VAR_DEF type declarator ) ;
    def variable(self, ):

        try:
            try:
                # SimpleCWalker.g:19:5: ( ^( VAR_DEF type declarator ) )
                # SimpleCWalker.g:19:9: ^( VAR_DEF type declarator )
                self.match(self.input, VAR_DEF, self.FOLLOW_VAR_DEF_in_variable119)


                self.match(self.input, DOWN, None)
                self.following.append(self.FOLLOW_type_in_variable121)
                self.type()
                self.following.pop()

                self.following.append(self.FOLLOW_declarator_in_variable123)
                self.declarator()
                self.following.pop()


                self.match(self.input, UP, None)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end variable


    # $ANTLR start declarator
    # SimpleCWalker.g:22:1: declarator : ID ;
    def declarator(self, ):

        try:
            try:
                # SimpleCWalker.g:23:5: ( ID )
                # SimpleCWalker.g:23:9: ID
                self.match(self.input, ID, self.FOLLOW_ID_in_declarator143)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end declarator


    # $ANTLR start functionHeader
    # SimpleCWalker.g:26:1: functionHeader : ^( FUNC_HDR type ID ( formalParameter )+ ) ;
    def functionHeader(self, ):

        try:
            try:
                # SimpleCWalker.g:27:5: ( ^( FUNC_HDR type ID ( formalParameter )+ ) )
                # SimpleCWalker.g:27:9: ^( FUNC_HDR type ID ( formalParameter )+ )
                self.match(self.input, FUNC_HDR, self.FOLLOW_FUNC_HDR_in_functionHeader164)


                self.match(self.input, DOWN, None)
                self.following.append(self.FOLLOW_type_in_functionHeader166)
                self.type()
                self.following.pop()

                self.match(self.input, ID, self.FOLLOW_ID_in_functionHeader168)

                # SimpleCWalker.g:27:28: ( formalParameter )+
                cnt3 = 0
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == ARG_DEF) :
                        alt3 = 1


                    if alt3 == 1:
                        # SimpleCWalker.g:27:28: formalParameter
                        self.following.append(self.FOLLOW_formalParameter_in_functionHeader170)
                        self.formalParameter()
                        self.following.pop()



                    else:
                        if cnt3 >= 1:
                            break #loop3

                        eee = EarlyExitException(3, self.input)
                        raise eee

                    cnt3 += 1



                self.match(self.input, UP, None)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end functionHeader


    # $ANTLR start formalParameter
    # SimpleCWalker.g:30:1: formalParameter : ^( ARG_DEF type declarator ) ;
    def formalParameter(self, ):

        try:
            try:
                # SimpleCWalker.g:31:5: ( ^( ARG_DEF type declarator ) )
                # SimpleCWalker.g:31:9: ^( ARG_DEF type declarator )
                self.match(self.input, ARG_DEF, self.FOLLOW_ARG_DEF_in_formalParameter192)


                self.match(self.input, DOWN, None)
                self.following.append(self.FOLLOW_type_in_formalParameter194)
                self.type()
                self.following.pop()

                self.following.append(self.FOLLOW_declarator_in_formalParameter196)
                self.declarator()
                self.following.pop()


                self.match(self.input, UP, None)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end formalParameter


    # $ANTLR start type
    # SimpleCWalker.g:34:1: type : ( 'int' | 'char' | 'void' | ID );
    def type(self, ):

        try:
            try:
                # SimpleCWalker.g:35:5: ( 'int' | 'char' | 'void' | ID )
                # SimpleCWalker.g:
                if self.input.LA(1) == ID or (INT_TYPE <= self.input.LA(1) <= VOID):
                    self.input.consume();
                    self.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_type0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end type


    # $ANTLR start block
    # SimpleCWalker.g:41:1: block : ^( BLOCK ( variable )* ( stat )* ) ;
    def block(self, ):

        try:
            try:
                # SimpleCWalker.g:42:5: ( ^( BLOCK ( variable )* ( stat )* ) )
                # SimpleCWalker.g:42:9: ^( BLOCK ( variable )* ( stat )* )
                self.match(self.input, BLOCK, self.FOLLOW_BLOCK_in_block274)


                if self.input.LA(1) == DOWN:
                    self.match(self.input, DOWN, None)
                    # SimpleCWalker.g:42:17: ( variable )*
                    while True: #loop4
                        alt4 = 2
                        LA4_0 = self.input.LA(1)

                        if (LA4_0 == VAR_DEF) :
                            alt4 = 1


                        if alt4 == 1:
                            # SimpleCWalker.g:42:17: variable
                            self.following.append(self.FOLLOW_variable_in_block276)
                            self.variable()
                            self.following.pop()



                        else:
                            break #loop4


                    # SimpleCWalker.g:42:27: ( stat )*
                    while True: #loop5
                        alt5 = 2
                        LA5_0 = self.input.LA(1)

                        if ((BLOCK <= LA5_0 <= FOR) or (EQEQ <= LA5_0 <= PLUS)) :
                            alt5 = 1


                        if alt5 == 1:
                            # SimpleCWalker.g:42:27: stat
                            self.following.append(self.FOLLOW_stat_in_block279)
                            self.stat()
                            self.following.pop()



                        else:
                            break #loop5



                    self.match(self.input, UP, None)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end block


    # $ANTLR start stat
    # SimpleCWalker.g:45:1: stat : ( forStat | expr | block );
    def stat(self, ):

        try:
            try:
                # SimpleCWalker.g:45:5: ( forStat | expr | block )
                alt6 = 3
                LA6 = self.input.LA(1)
                if LA6 == FOR:
                    alt6 = 1
                elif LA6 == ID or LA6 == EQ or LA6 == INT or LA6 == EQEQ or LA6 == LT or LA6 == PLUS:
                    alt6 = 2
                elif LA6 == BLOCK:
                    alt6 = 3
                else:
                    nvae = NoViableAltException("45:1: stat : ( forStat | expr | block );", 6, 0, self.input)

                    raise nvae

                if alt6 == 1:
                    # SimpleCWalker.g:45:7: forStat
                    self.following.append(self.FOLLOW_forStat_in_stat293)
                    self.forStat()
                    self.following.pop()



                elif alt6 == 2:
                    # SimpleCWalker.g:46:7: expr
                    self.following.append(self.FOLLOW_expr_in_stat301)
                    self.expr()
                    self.following.pop()



                elif alt6 == 3:
                    # SimpleCWalker.g:47:7: block
                    self.following.append(self.FOLLOW_block_in_stat309)
                    self.block()
                    self.following.pop()




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end stat


    # $ANTLR start forStat
    # SimpleCWalker.g:50:1: forStat : ^( 'for' expr expr expr block ) ;
    def forStat(self, ):

        try:
            try:
                # SimpleCWalker.g:51:5: ( ^( 'for' expr expr expr block ) )
                # SimpleCWalker.g:51:9: ^( 'for' expr expr expr block )
                self.match(self.input, FOR, self.FOLLOW_FOR_in_forStat329)


                self.match(self.input, DOWN, None)
                self.following.append(self.FOLLOW_expr_in_forStat331)
                self.expr()
                self.following.pop()

                self.following.append(self.FOLLOW_expr_in_forStat333)
                self.expr()
                self.following.pop()

                self.following.append(self.FOLLOW_expr_in_forStat335)
                self.expr()
                self.following.pop()

                self.following.append(self.FOLLOW_block_in_forStat337)
                self.block()
                self.following.pop()


                self.match(self.input, UP, None)





            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end forStat


    # $ANTLR start expr
    # SimpleCWalker.g:54:1: expr : ( ^( EQEQ expr expr ) | ^( LT expr expr ) | ^( PLUS expr expr ) | ^( EQ ID expr ) | atom );
    def expr(self, ):

        try:
            try:
                # SimpleCWalker.g:54:5: ( ^( EQEQ expr expr ) | ^( LT expr expr ) | ^( PLUS expr expr ) | ^( EQ ID expr ) | atom )
                alt7 = 5
                LA7 = self.input.LA(1)
                if LA7 == EQEQ:
                    alt7 = 1
                elif LA7 == LT:
                    alt7 = 2
                elif LA7 == PLUS:
                    alt7 = 3
                elif LA7 == EQ:
                    alt7 = 4
                elif LA7 == ID or LA7 == INT:
                    alt7 = 5
                else:
                    nvae = NoViableAltException("54:1: expr : ( ^( EQEQ expr expr ) | ^( LT expr expr ) | ^( PLUS expr expr ) | ^( EQ ID expr ) | atom );", 7, 0, self.input)

                    raise nvae

                if alt7 == 1:
                    # SimpleCWalker.g:54:9: ^( EQEQ expr expr )
                    self.match(self.input, EQEQ, self.FOLLOW_EQEQ_in_expr353)


                    self.match(self.input, DOWN, None)
                    self.following.append(self.FOLLOW_expr_in_expr355)
                    self.expr()
                    self.following.pop()

                    self.following.append(self.FOLLOW_expr_in_expr357)
                    self.expr()
                    self.following.pop()


                    self.match(self.input, UP, None)



                elif alt7 == 2:
                    # SimpleCWalker.g:55:9: ^( LT expr expr )
                    self.match(self.input, LT, self.FOLLOW_LT_in_expr369)


                    self.match(self.input, DOWN, None)
                    self.following.append(self.FOLLOW_expr_in_expr371)
                    self.expr()
                    self.following.pop()

                    self.following.append(self.FOLLOW_expr_in_expr373)
                    self.expr()
                    self.following.pop()


                    self.match(self.input, UP, None)



                elif alt7 == 3:
                    # SimpleCWalker.g:56:9: ^( PLUS expr expr )
                    self.match(self.input, PLUS, self.FOLLOW_PLUS_in_expr385)


                    self.match(self.input, DOWN, None)
                    self.following.append(self.FOLLOW_expr_in_expr387)
                    self.expr()
                    self.following.pop()

                    self.following.append(self.FOLLOW_expr_in_expr389)
                    self.expr()
                    self.following.pop()


                    self.match(self.input, UP, None)



                elif alt7 == 4:
                    # SimpleCWalker.g:57:9: ^( EQ ID expr )
                    self.match(self.input, EQ, self.FOLLOW_EQ_in_expr401)


                    self.match(self.input, DOWN, None)
                    self.match(self.input, ID, self.FOLLOW_ID_in_expr403)

                    self.following.append(self.FOLLOW_expr_in_expr405)
                    self.expr()
                    self.following.pop()


                    self.match(self.input, UP, None)



                elif alt7 == 5:
                    # SimpleCWalker.g:58:9: atom
                    self.following.append(self.FOLLOW_atom_in_expr416)
                    self.atom()
                    self.following.pop()




            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end expr


    # $ANTLR start atom
    # SimpleCWalker.g:61:1: atom : ( ID | INT );
    def atom(self, ):

        try:
            try:
                # SimpleCWalker.g:62:5: ( ID | INT )
                # SimpleCWalker.g:
                if self.input.LA(1) == ID or self.input.LA(1) == INT:
                    self.input.consume();
                    self.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_atom0
                        )
                    raise mse






            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return 

    # $ANTLR end atom


 

    FOLLOW_declaration_in_program49 = frozenset([1, 4, 7, 8])
    FOLLOW_variable_in_declaration69 = frozenset([1])
    FOLLOW_FUNC_DECL_in_declaration80 = frozenset([2])
    FOLLOW_functionHeader_in_declaration82 = frozenset([3])
    FOLLOW_FUNC_DEF_in_declaration94 = frozenset([2])
    FOLLOW_functionHeader_in_declaration96 = frozenset([9])
    FOLLOW_block_in_declaration98 = frozenset([3])
    FOLLOW_VAR_DEF_in_variable119 = frozenset([2])
    FOLLOW_type_in_variable121 = frozenset([10])
    FOLLOW_declarator_in_variable123 = frozenset([3])
    FOLLOW_ID_in_declarator143 = frozenset([1])
    FOLLOW_FUNC_HDR_in_functionHeader164 = frozenset([2])
    FOLLOW_type_in_functionHeader166 = frozenset([10])
    FOLLOW_ID_in_functionHeader168 = frozenset([5])
    FOLLOW_formalParameter_in_functionHeader170 = frozenset([3, 5])
    FOLLOW_ARG_DEF_in_formalParameter192 = frozenset([2])
    FOLLOW_type_in_formalParameter194 = frozenset([10])
    FOLLOW_declarator_in_formalParameter196 = frozenset([3])
    FOLLOW_set_in_type0 = frozenset([1])
    FOLLOW_BLOCK_in_block274 = frozenset([2])
    FOLLOW_variable_in_block276 = frozenset([3, 4, 9, 10, 11, 12, 13, 17, 18, 19])
    FOLLOW_stat_in_block279 = frozenset([3, 9, 10, 11, 12, 13, 17, 18, 19])
    FOLLOW_forStat_in_stat293 = frozenset([1])
    FOLLOW_expr_in_stat301 = frozenset([1])
    FOLLOW_block_in_stat309 = frozenset([1])
    FOLLOW_FOR_in_forStat329 = frozenset([2])
    FOLLOW_expr_in_forStat331 = frozenset([10, 11, 12, 17, 18, 19])
    FOLLOW_expr_in_forStat333 = frozenset([10, 11, 12, 17, 18, 19])
    FOLLOW_expr_in_forStat335 = frozenset([9])
    FOLLOW_block_in_forStat337 = frozenset([3])
    FOLLOW_EQEQ_in_expr353 = frozenset([2])
    FOLLOW_expr_in_expr355 = frozenset([10, 11, 12, 17, 18, 19])
    FOLLOW_expr_in_expr357 = frozenset([3])
    FOLLOW_LT_in_expr369 = frozenset([2])
    FOLLOW_expr_in_expr371 = frozenset([10, 11, 12, 17, 18, 19])
    FOLLOW_expr_in_expr373 = frozenset([3])
    FOLLOW_PLUS_in_expr385 = frozenset([2])
    FOLLOW_expr_in_expr387 = frozenset([10, 11, 12, 17, 18, 19])
    FOLLOW_expr_in_expr389 = frozenset([3])
    FOLLOW_EQ_in_expr401 = frozenset([2])
    FOLLOW_ID_in_expr403 = frozenset([10, 11, 12, 17, 18, 19])
    FOLLOW_expr_in_expr405 = frozenset([3])
    FOLLOW_atom_in_expr416 = frozenset([1])
    FOLLOW_set_in_atom0 = frozenset([1])

