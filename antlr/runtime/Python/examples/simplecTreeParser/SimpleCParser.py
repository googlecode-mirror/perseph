# $ANTLR 3.0.1 SimpleC.g 2008-07-31 14:01:33

from antlr3 import *
from antlr3.compat import set, frozenset

from antlr3.tree import *



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



class SimpleCParser(Parser):
    grammarFileName = "SimpleC.g"
    tokenNames = tokenNames

    def __init__(self, input):
        Parser.__init__(self, input)
        self.dfa2 = self.DFA2(
            self, 2,
            eot = self.DFA2_eot,
            eof = self.DFA2_eof,
            min = self.DFA2_min,
            max = self.DFA2_max,
            accept = self.DFA2_accept,
            special = self.DFA2_special,
            transition = self.DFA2_transition
            )




                
        self.adaptor = CommonTreeAdaptor()




    class program_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start program
    # SimpleC.g:16:1: program : ( declaration )+ ;
    def program(self, ):

        retval = self.program_return()
        retval.start = self.input.LT(1)

        root_0 = None

        declaration1 = None



        try:
            try:
                # SimpleC.g:17:5: ( ( declaration )+ )
                # SimpleC.g:17:9: ( declaration )+
                root_0 = self.adaptor.nil()

                # SimpleC.g:17:9: ( declaration )+
                cnt1 = 0
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if (LA1_0 == ID or (INT_TYPE <= LA1_0 <= VOID)) :
                        alt1 = 1


                    if alt1 == 1:
                        # SimpleC.g:17:9: declaration
                        self.following.append(self.FOLLOW_declaration_in_program85)
                        declaration1 = self.declaration()
                        self.following.pop()

                        self.adaptor.addChild(root_0, declaration1.tree)


                    else:
                        if cnt1 >= 1:
                            break #loop1

                        eee = EarlyExitException(1, self.input)
                        raise eee

                    cnt1 += 1





                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end program

    class declaration_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start declaration
    # SimpleC.g:20:1: declaration : ( variable | functionHeader ';' -> ^( FUNC_DECL functionHeader ) | functionHeader block -> ^( FUNC_DEF functionHeader block ) );
    def declaration(self, ):

        retval = self.declaration_return()
        retval.start = self.input.LT(1)

        root_0 = None

        char_literal4 = None
        variable2 = None

        functionHeader3 = None

        functionHeader5 = None

        block6 = None


        char_literal4_tree = None
        stream_21 = RewriteRuleTokenStream(self.adaptor, "token 21")
        stream_functionHeader = RewriteRuleSubtreeStream(self.adaptor, "rule functionHeader")
        stream_block = RewriteRuleSubtreeStream(self.adaptor, "rule block")
        try:
            try:
                # SimpleC.g:21:5: ( variable | functionHeader ';' -> ^( FUNC_DECL functionHeader ) | functionHeader block -> ^( FUNC_DEF functionHeader block ) )
                alt2 = 3
                alt2 = self.dfa2.predict(self.input)
                if alt2 == 1:
                    # SimpleC.g:21:9: variable
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_variable_in_declaration105)
                    variable2 = self.variable()
                    self.following.pop()

                    self.adaptor.addChild(root_0, variable2.tree)


                elif alt2 == 2:
                    # SimpleC.g:22:9: functionHeader ';'
                    self.following.append(self.FOLLOW_functionHeader_in_declaration115)
                    functionHeader3 = self.functionHeader()
                    self.following.pop()

                    stream_functionHeader.add(functionHeader3.tree)
                    char_literal4 = self.input.LT(1)
                    self.match(self.input, 21, self.FOLLOW_21_in_declaration117)

                    stream_21.add(char_literal4)
                    # AST Rewrite
                    # elements: functionHeader
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", None)


                    root_0 = self.adaptor.nil()
                    # 22:28: -> ^( FUNC_DECL functionHeader )
                    # SimpleC.g:22:31: ^( FUNC_DECL functionHeader )
                    root_1 = self.adaptor.nil()
                    root_1 = self.adaptor.becomeRoot(self.adaptor.createFromType(FUNC_DECL, "FUNC_DECL"), root_1)

                    self.adaptor.addChild(root_1, stream_functionHeader.next())

                    self.adaptor.addChild(root_0, root_1)





                elif alt2 == 3:
                    # SimpleC.g:23:9: functionHeader block
                    self.following.append(self.FOLLOW_functionHeader_in_declaration135)
                    functionHeader5 = self.functionHeader()
                    self.following.pop()

                    stream_functionHeader.add(functionHeader5.tree)
                    self.following.append(self.FOLLOW_block_in_declaration137)
                    block6 = self.block()
                    self.following.pop()

                    stream_block.add(block6.tree)
                    # AST Rewrite
                    # elements: block, functionHeader
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", None)


                    root_0 = self.adaptor.nil()
                    # 23:30: -> ^( FUNC_DEF functionHeader block )
                    # SimpleC.g:23:33: ^( FUNC_DEF functionHeader block )
                    root_1 = self.adaptor.nil()
                    root_1 = self.adaptor.becomeRoot(self.adaptor.createFromType(FUNC_DEF, "FUNC_DEF"), root_1)

                    self.adaptor.addChild(root_1, stream_functionHeader.next())
                    self.adaptor.addChild(root_1, stream_block.next())

                    self.adaptor.addChild(root_0, root_1)





                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end declaration

    class variable_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start variable
    # SimpleC.g:26:1: variable : type declarator ';' -> ^( VAR_DEF type declarator ) ;
    def variable(self, ):

        retval = self.variable_return()
        retval.start = self.input.LT(1)

        root_0 = None

        char_literal9 = None
        type7 = None

        declarator8 = None


        char_literal9_tree = None
        stream_21 = RewriteRuleTokenStream(self.adaptor, "token 21")
        stream_declarator = RewriteRuleSubtreeStream(self.adaptor, "rule declarator")
        stream_type = RewriteRuleSubtreeStream(self.adaptor, "rule type")
        try:
            try:
                # SimpleC.g:27:5: ( type declarator ';' -> ^( VAR_DEF type declarator ) )
                # SimpleC.g:27:9: type declarator ';'
                self.following.append(self.FOLLOW_type_in_variable166)
                type7 = self.type()
                self.following.pop()

                stream_type.add(type7.tree)
                self.following.append(self.FOLLOW_declarator_in_variable168)
                declarator8 = self.declarator()
                self.following.pop()

                stream_declarator.add(declarator8.tree)
                char_literal9 = self.input.LT(1)
                self.match(self.input, 21, self.FOLLOW_21_in_variable170)

                stream_21.add(char_literal9)
                # AST Rewrite
                # elements: type, declarator
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 

                retval.tree = root_0

                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", None)


                root_0 = self.adaptor.nil()
                # 27:29: -> ^( VAR_DEF type declarator )
                # SimpleC.g:27:32: ^( VAR_DEF type declarator )
                root_1 = self.adaptor.nil()
                root_1 = self.adaptor.becomeRoot(self.adaptor.createFromType(VAR_DEF, "VAR_DEF"), root_1)

                self.adaptor.addChild(root_1, stream_type.next())
                self.adaptor.addChild(root_1, stream_declarator.next())

                self.adaptor.addChild(root_0, root_1)






                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end variable

    class declarator_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start declarator
    # SimpleC.g:30:1: declarator : ID ;
    def declarator(self, ):

        retval = self.declarator_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID10 = None

        ID10_tree = None

        try:
            try:
                # SimpleC.g:31:5: ( ID )
                # SimpleC.g:31:9: ID
                root_0 = self.adaptor.nil()

                ID10 = self.input.LT(1)
                self.match(self.input, ID, self.FOLLOW_ID_in_declarator199)


                ID10_tree = self.adaptor.createWithPayload(ID10)
                self.adaptor.addChild(root_0, ID10_tree)




                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end declarator

    class functionHeader_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start functionHeader
    # SimpleC.g:34:1: functionHeader : type ID '(' ( formalParameter ( ',' formalParameter )* )? ')' -> ^( FUNC_HDR type ID ( formalParameter )+ ) ;
    def functionHeader(self, ):

        retval = self.functionHeader_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID12 = None
        char_literal13 = None
        char_literal15 = None
        char_literal17 = None
        type11 = None

        formalParameter14 = None

        formalParameter16 = None


        ID12_tree = None
        char_literal13_tree = None
        char_literal15_tree = None
        char_literal17_tree = None
        stream_ID = RewriteRuleTokenStream(self.adaptor, "token ID")
        stream_22 = RewriteRuleTokenStream(self.adaptor, "token 22")
        stream_23 = RewriteRuleTokenStream(self.adaptor, "token 23")
        stream_24 = RewriteRuleTokenStream(self.adaptor, "token 24")
        stream_formalParameter = RewriteRuleSubtreeStream(self.adaptor, "rule formalParameter")
        stream_type = RewriteRuleSubtreeStream(self.adaptor, "rule type")
        try:
            try:
                # SimpleC.g:35:5: ( type ID '(' ( formalParameter ( ',' formalParameter )* )? ')' -> ^( FUNC_HDR type ID ( formalParameter )+ ) )
                # SimpleC.g:35:9: type ID '(' ( formalParameter ( ',' formalParameter )* )? ')'
                self.following.append(self.FOLLOW_type_in_functionHeader219)
                type11 = self.type()
                self.following.pop()

                stream_type.add(type11.tree)
                ID12 = self.input.LT(1)
                self.match(self.input, ID, self.FOLLOW_ID_in_functionHeader221)

                stream_ID.add(ID12)
                char_literal13 = self.input.LT(1)
                self.match(self.input, 22, self.FOLLOW_22_in_functionHeader223)

                stream_22.add(char_literal13)
                # SimpleC.g:35:21: ( formalParameter ( ',' formalParameter )* )?
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == ID or (INT_TYPE <= LA4_0 <= VOID)) :
                    alt4 = 1
                if alt4 == 1:
                    # SimpleC.g:35:23: formalParameter ( ',' formalParameter )*
                    self.following.append(self.FOLLOW_formalParameter_in_functionHeader227)
                    formalParameter14 = self.formalParameter()
                    self.following.pop()

                    stream_formalParameter.add(formalParameter14.tree)
                    # SimpleC.g:35:39: ( ',' formalParameter )*
                    while True: #loop3
                        alt3 = 2
                        LA3_0 = self.input.LA(1)

                        if (LA3_0 == 23) :
                            alt3 = 1


                        if alt3 == 1:
                            # SimpleC.g:35:41: ',' formalParameter
                            char_literal15 = self.input.LT(1)
                            self.match(self.input, 23, self.FOLLOW_23_in_functionHeader231)

                            stream_23.add(char_literal15)
                            self.following.append(self.FOLLOW_formalParameter_in_functionHeader233)
                            formalParameter16 = self.formalParameter()
                            self.following.pop()

                            stream_formalParameter.add(formalParameter16.tree)


                        else:
                            break #loop3





                char_literal17 = self.input.LT(1)
                self.match(self.input, 24, self.FOLLOW_24_in_functionHeader241)

                stream_24.add(char_literal17)
                # AST Rewrite
                # elements: type, formalParameter, ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 

                retval.tree = root_0

                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", None)


                root_0 = self.adaptor.nil()
                # 36:9: -> ^( FUNC_HDR type ID ( formalParameter )+ )
                # SimpleC.g:36:12: ^( FUNC_HDR type ID ( formalParameter )+ )
                root_1 = self.adaptor.nil()
                root_1 = self.adaptor.becomeRoot(self.adaptor.createFromType(FUNC_HDR, "FUNC_HDR"), root_1)

                self.adaptor.addChild(root_1, stream_type.next())
                self.adaptor.addChild(root_1, stream_ID.next())
                # SimpleC.g:36:31: ( formalParameter )+
                if not (stream_formalParameter.hasNext()):
                    raise RewriteEarlyExitException()

                while stream_formalParameter.hasNext():
                    self.adaptor.addChild(root_1, stream_formalParameter.next())


                stream_formalParameter.reset()

                self.adaptor.addChild(root_0, root_1)






                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end functionHeader

    class formalParameter_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start formalParameter
    # SimpleC.g:39:1: formalParameter : type declarator -> ^( ARG_DEF type declarator ) ;
    def formalParameter(self, ):

        retval = self.formalParameter_return()
        retval.start = self.input.LT(1)

        root_0 = None

        type18 = None

        declarator19 = None


        stream_declarator = RewriteRuleSubtreeStream(self.adaptor, "rule declarator")
        stream_type = RewriteRuleSubtreeStream(self.adaptor, "rule type")
        try:
            try:
                # SimpleC.g:40:5: ( type declarator -> ^( ARG_DEF type declarator ) )
                # SimpleC.g:40:9: type declarator
                self.following.append(self.FOLLOW_type_in_formalParameter281)
                type18 = self.type()
                self.following.pop()

                stream_type.add(type18.tree)
                self.following.append(self.FOLLOW_declarator_in_formalParameter283)
                declarator19 = self.declarator()
                self.following.pop()

                stream_declarator.add(declarator19.tree)
                # AST Rewrite
                # elements: declarator, type
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 

                retval.tree = root_0

                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", None)


                root_0 = self.adaptor.nil()
                # 40:25: -> ^( ARG_DEF type declarator )
                # SimpleC.g:40:28: ^( ARG_DEF type declarator )
                root_1 = self.adaptor.nil()
                root_1 = self.adaptor.becomeRoot(self.adaptor.createFromType(ARG_DEF, "ARG_DEF"), root_1)

                self.adaptor.addChild(root_1, stream_type.next())
                self.adaptor.addChild(root_1, stream_declarator.next())

                self.adaptor.addChild(root_0, root_1)






                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end formalParameter

    class type_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start type
    # SimpleC.g:43:1: type : ( 'int' | 'char' | 'void' | ID );
    def type(self, ):

        retval = self.type_return()
        retval.start = self.input.LT(1)

        root_0 = None

        set20 = None

        set20_tree = None

        try:
            try:
                # SimpleC.g:44:5: ( 'int' | 'char' | 'void' | ID )
                # SimpleC.g:
                root_0 = self.adaptor.nil()

                set20 = self.input.LT(1)
                if self.input.LA(1) == ID or (INT_TYPE <= self.input.LA(1) <= VOID):
                    self.input.consume();
                    self.adaptor.addChild(root_0, self.adaptor.createWithPayload(set20))
                    self.errorRecovery = False

                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recoverFromMismatchedSet(
                        self.input, mse, self.FOLLOW_set_in_type0
                        )
                    raise mse





                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end type

    class block_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start block
    # SimpleC.g:50:1: block : lc= '{' ( variable )* ( stat )* '}' -> ^( BLOCK[$lc,\"BLOCK\"] ( variable )* ( stat )* ) ;
    def block(self, ):

        retval = self.block_return()
        retval.start = self.input.LT(1)

        root_0 = None

        lc = None
        char_literal23 = None
        variable21 = None

        stat22 = None


        lc_tree = None
        char_literal23_tree = None
        stream_25 = RewriteRuleTokenStream(self.adaptor, "token 25")
        stream_26 = RewriteRuleTokenStream(self.adaptor, "token 26")
        stream_variable = RewriteRuleSubtreeStream(self.adaptor, "rule variable")
        stream_stat = RewriteRuleSubtreeStream(self.adaptor, "rule stat")
        try:
            try:
                # SimpleC.g:51:5: (lc= '{' ( variable )* ( stat )* '}' -> ^( BLOCK[$lc,\"BLOCK\"] ( variable )* ( stat )* ) )
                # SimpleC.g:51:9: lc= '{' ( variable )* ( stat )* '}'
                lc = self.input.LT(1)
                self.match(self.input, 25, self.FOLLOW_25_in_block376)

                stream_25.add(lc)
                # SimpleC.g:52:13: ( variable )*
                while True: #loop5
                    alt5 = 2
                    LA5_0 = self.input.LA(1)

                    if (LA5_0 == ID) :
                        LA5_2 = self.input.LA(2)

                        if (LA5_2 == ID) :
                            alt5 = 1


                    elif ((INT_TYPE <= LA5_0 <= VOID)) :
                        alt5 = 1


                    if alt5 == 1:
                        # SimpleC.g:52:13: variable
                        self.following.append(self.FOLLOW_variable_in_block390)
                        variable21 = self.variable()
                        self.following.pop()

                        stream_variable.add(variable21.tree)


                    else:
                        break #loop5


                # SimpleC.g:53:13: ( stat )*
                while True: #loop6
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if (LA6_0 == ID or (INT <= LA6_0 <= FOR) or (21 <= LA6_0 <= 22) or LA6_0 == 25) :
                        alt6 = 1


                    if alt6 == 1:
                        # SimpleC.g:53:13: stat
                        self.following.append(self.FOLLOW_stat_in_block405)
                        stat22 = self.stat()
                        self.following.pop()

                        stream_stat.add(stat22.tree)


                    else:
                        break #loop6


                char_literal23 = self.input.LT(1)
                self.match(self.input, 26, self.FOLLOW_26_in_block416)

                stream_26.add(char_literal23)
                # AST Rewrite
                # elements: stat, variable
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 

                retval.tree = root_0

                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", None)


                root_0 = self.adaptor.nil()
                # 55:9: -> ^( BLOCK[$lc,\"BLOCK\"] ( variable )* ( stat )* )
                # SimpleC.g:55:12: ^( BLOCK[$lc,\"BLOCK\"] ( variable )* ( stat )* )
                root_1 = self.adaptor.nil()
                root_1 = self.adaptor.becomeRoot(self.adaptor.createFromToken(BLOCK, lc, "BLOCK"), root_1)

                # SimpleC.g:55:33: ( variable )*
                while stream_variable.hasNext():
                    self.adaptor.addChild(root_1, stream_variable.next())


                stream_variable.reset();
                # SimpleC.g:55:43: ( stat )*
                while stream_stat.hasNext():
                    self.adaptor.addChild(root_1, stream_stat.next())


                stream_stat.reset();

                self.adaptor.addChild(root_0, root_1)






                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end block

    class stat_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start stat
    # SimpleC.g:58:1: stat : ( forStat | expr ';' | block | assignStat ';' | ';' );
    def stat(self, ):

        retval = self.stat_return()
        retval.start = self.input.LT(1)

        root_0 = None

        char_literal26 = None
        char_literal29 = None
        char_literal30 = None
        forStat24 = None

        expr25 = None

        block27 = None

        assignStat28 = None


        char_literal26_tree = None
        char_literal29_tree = None
        char_literal30_tree = None

        try:
            try:
                # SimpleC.g:58:5: ( forStat | expr ';' | block | assignStat ';' | ';' )
                alt7 = 5
                LA7 = self.input.LA(1)
                if LA7 == FOR:
                    alt7 = 1
                elif LA7 == ID:
                    LA7_2 = self.input.LA(2)

                    if (LA7_2 == EQ) :
                        alt7 = 4
                    elif ((EQEQ <= LA7_2 <= PLUS) or LA7_2 == 21) :
                        alt7 = 2
                    else:
                        nvae = NoViableAltException("58:1: stat : ( forStat | expr ';' | block | assignStat ';' | ';' );", 7, 2, self.input)

                        raise nvae

                elif LA7 == INT or LA7 == 22:
                    alt7 = 2
                elif LA7 == 25:
                    alt7 = 3
                elif LA7 == 21:
                    alt7 = 5
                else:
                    nvae = NoViableAltException("58:1: stat : ( forStat | expr ';' | block | assignStat ';' | ';' );", 7, 0, self.input)

                    raise nvae

                if alt7 == 1:
                    # SimpleC.g:58:7: forStat
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_forStat_in_stat449)
                    forStat24 = self.forStat()
                    self.following.pop()

                    self.adaptor.addChild(root_0, forStat24.tree)


                elif alt7 == 2:
                    # SimpleC.g:59:7: expr ';'
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_expr_in_stat457)
                    expr25 = self.expr()
                    self.following.pop()

                    self.adaptor.addChild(root_0, expr25.tree)
                    char_literal26 = self.input.LT(1)
                    self.match(self.input, 21, self.FOLLOW_21_in_stat459)



                elif alt7 == 3:
                    # SimpleC.g:60:7: block
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_block_in_stat468)
                    block27 = self.block()
                    self.following.pop()

                    self.adaptor.addChild(root_0, block27.tree)


                elif alt7 == 4:
                    # SimpleC.g:61:7: assignStat ';'
                    root_0 = self.adaptor.nil()

                    self.following.append(self.FOLLOW_assignStat_in_stat476)
                    assignStat28 = self.assignStat()
                    self.following.pop()

                    self.adaptor.addChild(root_0, assignStat28.tree)
                    char_literal29 = self.input.LT(1)
                    self.match(self.input, 21, self.FOLLOW_21_in_stat478)



                elif alt7 == 5:
                    # SimpleC.g:62:7: ';'
                    root_0 = self.adaptor.nil()

                    char_literal30 = self.input.LT(1)
                    self.match(self.input, 21, self.FOLLOW_21_in_stat487)



                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end stat

    class forStat_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start forStat
    # SimpleC.g:65:1: forStat : 'for' '(' start= assignStat ';' expr ';' next= assignStat ')' block -> ^( 'for' $start expr $next block ) ;
    def forStat(self, ):

        retval = self.forStat_return()
        retval.start = self.input.LT(1)

        root_0 = None

        string_literal31 = None
        char_literal32 = None
        char_literal33 = None
        char_literal35 = None
        char_literal36 = None
        start = None

        next = None

        expr34 = None

        block37 = None


        string_literal31_tree = None
        char_literal32_tree = None
        char_literal33_tree = None
        char_literal35_tree = None
        char_literal36_tree = None
        stream_21 = RewriteRuleTokenStream(self.adaptor, "token 21")
        stream_FOR = RewriteRuleTokenStream(self.adaptor, "token FOR")
        stream_22 = RewriteRuleTokenStream(self.adaptor, "token 22")
        stream_24 = RewriteRuleTokenStream(self.adaptor, "token 24")
        stream_assignStat = RewriteRuleSubtreeStream(self.adaptor, "rule assignStat")
        stream_block = RewriteRuleSubtreeStream(self.adaptor, "rule block")
        stream_expr = RewriteRuleSubtreeStream(self.adaptor, "rule expr")
        try:
            try:
                # SimpleC.g:66:5: ( 'for' '(' start= assignStat ';' expr ';' next= assignStat ')' block -> ^( 'for' $start expr $next block ) )
                # SimpleC.g:66:9: 'for' '(' start= assignStat ';' expr ';' next= assignStat ')' block
                string_literal31 = self.input.LT(1)
                self.match(self.input, FOR, self.FOLLOW_FOR_in_forStat507)

                stream_FOR.add(string_literal31)
                char_literal32 = self.input.LT(1)
                self.match(self.input, 22, self.FOLLOW_22_in_forStat509)

                stream_22.add(char_literal32)
                self.following.append(self.FOLLOW_assignStat_in_forStat513)
                start = self.assignStat()
                self.following.pop()

                stream_assignStat.add(start.tree)
                char_literal33 = self.input.LT(1)
                self.match(self.input, 21, self.FOLLOW_21_in_forStat515)

                stream_21.add(char_literal33)
                self.following.append(self.FOLLOW_expr_in_forStat517)
                expr34 = self.expr()
                self.following.pop()

                stream_expr.add(expr34.tree)
                char_literal35 = self.input.LT(1)
                self.match(self.input, 21, self.FOLLOW_21_in_forStat519)

                stream_21.add(char_literal35)
                self.following.append(self.FOLLOW_assignStat_in_forStat523)
                next = self.assignStat()
                self.following.pop()

                stream_assignStat.add(next.tree)
                char_literal36 = self.input.LT(1)
                self.match(self.input, 24, self.FOLLOW_24_in_forStat525)

                stream_24.add(char_literal36)
                self.following.append(self.FOLLOW_block_in_forStat527)
                block37 = self.block()
                self.following.pop()

                stream_block.add(block37.tree)
                # AST Rewrite
                # elements: start, next, FOR, block, expr
                # token labels: 
                # rule labels: retval, start, next
                # token list labels: 
                # rule list labels: 

                retval.tree = root_0

                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", None)


                if start is not None:
                    stream_start = RewriteRuleSubtreeStream(self.adaptor, "token start", start.tree)
                else:
                    stream_start = RewriteRuleSubtreeStream(self.adaptor, "token start", None)


                if next is not None:
                    stream_next = RewriteRuleSubtreeStream(self.adaptor, "token next", next.tree)
                else:
                    stream_next = RewriteRuleSubtreeStream(self.adaptor, "token next", None)


                root_0 = self.adaptor.nil()
                # 67:9: -> ^( 'for' $start expr $next block )
                # SimpleC.g:67:12: ^( 'for' $start expr $next block )
                root_1 = self.adaptor.nil()
                root_1 = self.adaptor.becomeRoot(stream_FOR.next(), root_1)

                self.adaptor.addChild(root_1, stream_start.next())
                self.adaptor.addChild(root_1, stream_expr.next())
                self.adaptor.addChild(root_1, stream_next.next())
                self.adaptor.addChild(root_1, stream_block.next())

                self.adaptor.addChild(root_0, root_1)






                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end forStat

    class assignStat_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start assignStat
    # SimpleC.g:70:1: assignStat : ID EQ expr -> ^( EQ ID expr ) ;
    def assignStat(self, ):

        retval = self.assignStat_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID38 = None
        EQ39 = None
        expr40 = None


        ID38_tree = None
        EQ39_tree = None
        stream_EQ = RewriteRuleTokenStream(self.adaptor, "token EQ")
        stream_ID = RewriteRuleTokenStream(self.adaptor, "token ID")
        stream_expr = RewriteRuleSubtreeStream(self.adaptor, "rule expr")
        try:
            try:
                # SimpleC.g:71:5: ( ID EQ expr -> ^( EQ ID expr ) )
                # SimpleC.g:71:9: ID EQ expr
                ID38 = self.input.LT(1)
                self.match(self.input, ID, self.FOLLOW_ID_in_assignStat570)

                stream_ID.add(ID38)
                EQ39 = self.input.LT(1)
                self.match(self.input, EQ, self.FOLLOW_EQ_in_assignStat572)

                stream_EQ.add(EQ39)
                self.following.append(self.FOLLOW_expr_in_assignStat574)
                expr40 = self.expr()
                self.following.pop()

                stream_expr.add(expr40.tree)
                # AST Rewrite
                # elements: EQ, expr, ID
                # token labels: 
                # rule labels: retval
                # token list labels: 
                # rule list labels: 

                retval.tree = root_0

                if retval is not None:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", retval.tree)
                else:
                    stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", None)


                root_0 = self.adaptor.nil()
                # 71:20: -> ^( EQ ID expr )
                # SimpleC.g:71:23: ^( EQ ID expr )
                root_1 = self.adaptor.nil()
                root_1 = self.adaptor.becomeRoot(stream_EQ.next(), root_1)

                self.adaptor.addChild(root_1, stream_ID.next())
                self.adaptor.addChild(root_1, stream_expr.next())

                self.adaptor.addChild(root_0, root_1)






                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end assignStat

    class expr_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start expr
    # SimpleC.g:74:1: expr : condExpr ;
    def expr(self, ):

        retval = self.expr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        condExpr41 = None



        try:
            try:
                # SimpleC.g:74:5: ( condExpr )
                # SimpleC.g:74:9: condExpr
                root_0 = self.adaptor.nil()

                self.following.append(self.FOLLOW_condExpr_in_expr598)
                condExpr41 = self.condExpr()
                self.following.pop()

                self.adaptor.addChild(root_0, condExpr41.tree)



                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end expr

    class condExpr_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start condExpr
    # SimpleC.g:77:1: condExpr : aexpr ( ( '==' | '<' ) aexpr )? ;
    def condExpr(self, ):

        retval = self.condExpr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        string_literal43 = None
        char_literal44 = None
        aexpr42 = None

        aexpr45 = None


        string_literal43_tree = None
        char_literal44_tree = None

        try:
            try:
                # SimpleC.g:78:5: ( aexpr ( ( '==' | '<' ) aexpr )? )
                # SimpleC.g:78:9: aexpr ( ( '==' | '<' ) aexpr )?
                root_0 = self.adaptor.nil()

                self.following.append(self.FOLLOW_aexpr_in_condExpr617)
                aexpr42 = self.aexpr()
                self.following.pop()

                self.adaptor.addChild(root_0, aexpr42.tree)
                # SimpleC.g:78:15: ( ( '==' | '<' ) aexpr )?
                alt9 = 2
                LA9_0 = self.input.LA(1)

                if ((EQEQ <= LA9_0 <= LT)) :
                    alt9 = 1
                if alt9 == 1:
                    # SimpleC.g:78:17: ( '==' | '<' ) aexpr
                    # SimpleC.g:78:17: ( '==' | '<' )
                    alt8 = 2
                    LA8_0 = self.input.LA(1)

                    if (LA8_0 == EQEQ) :
                        alt8 = 1
                    elif (LA8_0 == LT) :
                        alt8 = 2
                    else:
                        nvae = NoViableAltException("78:17: ( '==' | '<' )", 8, 0, self.input)

                        raise nvae

                    if alt8 == 1:
                        # SimpleC.g:78:18: '=='
                        string_literal43 = self.input.LT(1)
                        self.match(self.input, EQEQ, self.FOLLOW_EQEQ_in_condExpr622)


                        string_literal43_tree = self.adaptor.createWithPayload(string_literal43)
                        root_0 = self.adaptor.becomeRoot(string_literal43_tree, root_0)


                    elif alt8 == 2:
                        # SimpleC.g:78:26: '<'
                        char_literal44 = self.input.LT(1)
                        self.match(self.input, LT, self.FOLLOW_LT_in_condExpr627)


                        char_literal44_tree = self.adaptor.createWithPayload(char_literal44)
                        root_0 = self.adaptor.becomeRoot(char_literal44_tree, root_0)



                    self.following.append(self.FOLLOW_aexpr_in_condExpr631)
                    aexpr45 = self.aexpr()
                    self.following.pop()

                    self.adaptor.addChild(root_0, aexpr45.tree)






                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end condExpr

    class aexpr_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start aexpr
    # SimpleC.g:81:1: aexpr : atom ( '+' atom )* ;
    def aexpr(self, ):

        retval = self.aexpr_return()
        retval.start = self.input.LT(1)

        root_0 = None

        char_literal47 = None
        atom46 = None

        atom48 = None


        char_literal47_tree = None

        try:
            try:
                # SimpleC.g:82:5: ( atom ( '+' atom )* )
                # SimpleC.g:82:9: atom ( '+' atom )*
                root_0 = self.adaptor.nil()

                self.following.append(self.FOLLOW_atom_in_aexpr653)
                atom46 = self.atom()
                self.following.pop()

                self.adaptor.addChild(root_0, atom46.tree)
                # SimpleC.g:82:14: ( '+' atom )*
                while True: #loop10
                    alt10 = 2
                    LA10_0 = self.input.LA(1)

                    if (LA10_0 == PLUS) :
                        alt10 = 1


                    if alt10 == 1:
                        # SimpleC.g:82:16: '+' atom
                        char_literal47 = self.input.LT(1)
                        self.match(self.input, PLUS, self.FOLLOW_PLUS_in_aexpr657)


                        char_literal47_tree = self.adaptor.createWithPayload(char_literal47)
                        root_0 = self.adaptor.becomeRoot(char_literal47_tree, root_0)
                        self.following.append(self.FOLLOW_atom_in_aexpr660)
                        atom48 = self.atom()
                        self.following.pop()

                        self.adaptor.addChild(root_0, atom48.tree)


                    else:
                        break #loop10





                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end aexpr

    class atom_return(object):
        def __init__(self):
            self.start = None
            self.stop = None

            self.tree = None


    # $ANTLR start atom
    # SimpleC.g:85:1: atom : ( ID | INT | '(' expr ')' -> expr );
    def atom(self, ):

        retval = self.atom_return()
        retval.start = self.input.LT(1)

        root_0 = None

        ID49 = None
        INT50 = None
        char_literal51 = None
        char_literal53 = None
        expr52 = None


        ID49_tree = None
        INT50_tree = None
        char_literal51_tree = None
        char_literal53_tree = None
        stream_22 = RewriteRuleTokenStream(self.adaptor, "token 22")
        stream_24 = RewriteRuleTokenStream(self.adaptor, "token 24")
        stream_expr = RewriteRuleSubtreeStream(self.adaptor, "rule expr")
        try:
            try:
                # SimpleC.g:86:5: ( ID | INT | '(' expr ')' -> expr )
                alt11 = 3
                LA11 = self.input.LA(1)
                if LA11 == ID:
                    alt11 = 1
                elif LA11 == INT:
                    alt11 = 2
                elif LA11 == 22:
                    alt11 = 3
                else:
                    nvae = NoViableAltException("85:1: atom : ( ID | INT | '(' expr ')' -> expr );", 11, 0, self.input)

                    raise nvae

                if alt11 == 1:
                    # SimpleC.g:86:7: ID
                    root_0 = self.adaptor.nil()

                    ID49 = self.input.LT(1)
                    self.match(self.input, ID, self.FOLLOW_ID_in_atom680)


                    ID49_tree = self.adaptor.createWithPayload(ID49)
                    self.adaptor.addChild(root_0, ID49_tree)



                elif alt11 == 2:
                    # SimpleC.g:87:7: INT
                    root_0 = self.adaptor.nil()

                    INT50 = self.input.LT(1)
                    self.match(self.input, INT, self.FOLLOW_INT_in_atom694)


                    INT50_tree = self.adaptor.createWithPayload(INT50)
                    self.adaptor.addChild(root_0, INT50_tree)



                elif alt11 == 3:
                    # SimpleC.g:88:7: '(' expr ')'
                    char_literal51 = self.input.LT(1)
                    self.match(self.input, 22, self.FOLLOW_22_in_atom708)

                    stream_22.add(char_literal51)
                    self.following.append(self.FOLLOW_expr_in_atom710)
                    expr52 = self.expr()
                    self.following.pop()

                    stream_expr.add(expr52.tree)
                    char_literal53 = self.input.LT(1)
                    self.match(self.input, 24, self.FOLLOW_24_in_atom712)

                    stream_24.add(char_literal53)
                    # AST Rewrite
                    # elements: expr
                    # token labels: 
                    # rule labels: retval
                    # token list labels: 
                    # rule list labels: 

                    retval.tree = root_0

                    if retval is not None:
                        stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", retval.tree)
                    else:
                        stream_retval = RewriteRuleSubtreeStream(self.adaptor, "token retval", None)


                    root_0 = self.adaptor.nil()
                    # 88:20: -> expr
                    self.adaptor.addChild(root_0, stream_expr.next())





                retval.stop = self.input.LT(-1)


                retval.tree = self.adaptor.rulePostProcessing(root_0)
                self.adaptor.setTokenBoundaries(retval.tree, retval.start, retval.stop)

            except RecognitionException, re:
                self.reportError(re)
                self.recover(self.input, re)
        finally:

            pass

        return retval

    # $ANTLR end atom


    # lookup tables for DFA #2

    DFA2_eot = DFA.unpack(
        u"\15\uffff"
        )

    DFA2_eof = DFA.unpack(
        u"\15\uffff"
        )

    DFA2_min = DFA.unpack(
        u"\2\12\1\25\1\12\1\uffff\1\12\1\25\1\27\2\uffff\2\12\1\27"
        )

    DFA2_max = DFA.unpack(
        u"\1\20\1\12\1\26\1\30\1\uffff\1\12\1\31\1\30\2\uffff\1\20\1\12\1"
        u"\30"
        )

    DFA2_accept = DFA.unpack(
        u"\4\uffff\1\1\3\uffff\1\3\1\2\3\uffff"
        )

    DFA2_special = DFA.unpack(
        u"\15\uffff"
        )

            
    DFA2_transition = [
        DFA.unpack(u"\1\1\3\uffff\3\1"),
        DFA.unpack(u"\1\2"),
        DFA.unpack(u"\1\4\1\3"),
        DFA.unpack(u"\1\5\3\uffff\3\5\7\uffff\1\6"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\7"),
        DFA.unpack(u"\1\11\3\uffff\1\10"),
        DFA.unpack(u"\1\12\1\6"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\13\3\uffff\3\13"),
        DFA.unpack(u"\1\14"),
        DFA.unpack(u"\1\12\1\6")
    ]

    # class definition for DFA #2

    DFA2 = DFA
 

    FOLLOW_declaration_in_program85 = frozenset([1, 10, 14, 15, 16])
    FOLLOW_variable_in_declaration105 = frozenset([1])
    FOLLOW_functionHeader_in_declaration115 = frozenset([21])
    FOLLOW_21_in_declaration117 = frozenset([1])
    FOLLOW_functionHeader_in_declaration135 = frozenset([25])
    FOLLOW_block_in_declaration137 = frozenset([1])
    FOLLOW_type_in_variable166 = frozenset([10])
    FOLLOW_declarator_in_variable168 = frozenset([21])
    FOLLOW_21_in_variable170 = frozenset([1])
    FOLLOW_ID_in_declarator199 = frozenset([1])
    FOLLOW_type_in_functionHeader219 = frozenset([10])
    FOLLOW_ID_in_functionHeader221 = frozenset([22])
    FOLLOW_22_in_functionHeader223 = frozenset([10, 14, 15, 16, 24])
    FOLLOW_formalParameter_in_functionHeader227 = frozenset([23, 24])
    FOLLOW_23_in_functionHeader231 = frozenset([10, 14, 15, 16])
    FOLLOW_formalParameter_in_functionHeader233 = frozenset([23, 24])
    FOLLOW_24_in_functionHeader241 = frozenset([1])
    FOLLOW_type_in_formalParameter281 = frozenset([10])
    FOLLOW_declarator_in_formalParameter283 = frozenset([1])
    FOLLOW_set_in_type0 = frozenset([1])
    FOLLOW_25_in_block376 = frozenset([10, 12, 13, 14, 15, 16, 21, 22, 25, 26])
    FOLLOW_variable_in_block390 = frozenset([10, 12, 13, 14, 15, 16, 21, 22, 25, 26])
    FOLLOW_stat_in_block405 = frozenset([10, 12, 13, 21, 22, 25, 26])
    FOLLOW_26_in_block416 = frozenset([1])
    FOLLOW_forStat_in_stat449 = frozenset([1])
    FOLLOW_expr_in_stat457 = frozenset([21])
    FOLLOW_21_in_stat459 = frozenset([1])
    FOLLOW_block_in_stat468 = frozenset([1])
    FOLLOW_assignStat_in_stat476 = frozenset([21])
    FOLLOW_21_in_stat478 = frozenset([1])
    FOLLOW_21_in_stat487 = frozenset([1])
    FOLLOW_FOR_in_forStat507 = frozenset([22])
    FOLLOW_22_in_forStat509 = frozenset([10])
    FOLLOW_assignStat_in_forStat513 = frozenset([21])
    FOLLOW_21_in_forStat515 = frozenset([10, 12, 22])
    FOLLOW_expr_in_forStat517 = frozenset([21])
    FOLLOW_21_in_forStat519 = frozenset([10])
    FOLLOW_assignStat_in_forStat523 = frozenset([24])
    FOLLOW_24_in_forStat525 = frozenset([25])
    FOLLOW_block_in_forStat527 = frozenset([1])
    FOLLOW_ID_in_assignStat570 = frozenset([11])
    FOLLOW_EQ_in_assignStat572 = frozenset([10, 12, 22])
    FOLLOW_expr_in_assignStat574 = frozenset([1])
    FOLLOW_condExpr_in_expr598 = frozenset([1])
    FOLLOW_aexpr_in_condExpr617 = frozenset([1, 17, 18])
    FOLLOW_EQEQ_in_condExpr622 = frozenset([10, 12, 22])
    FOLLOW_LT_in_condExpr627 = frozenset([10, 12, 22])
    FOLLOW_aexpr_in_condExpr631 = frozenset([1])
    FOLLOW_atom_in_aexpr653 = frozenset([1, 19])
    FOLLOW_PLUS_in_aexpr657 = frozenset([10, 12, 22])
    FOLLOW_atom_in_aexpr660 = frozenset([1, 19])
    FOLLOW_ID_in_atom680 = frozenset([1])
    FOLLOW_INT_in_atom694 = frozenset([1])
    FOLLOW_22_in_atom708 = frozenset([10, 12, 22])
    FOLLOW_expr_in_atom710 = frozenset([24])
    FOLLOW_24_in_atom712 = frozenset([1])

