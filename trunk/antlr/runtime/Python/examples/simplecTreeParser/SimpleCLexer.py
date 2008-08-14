# $ANTLR 3.0.1 SimpleC.g 2008-07-31 14:01:33

from antlr3 import *
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
T26=26
INT_TYPE=14
T25=25
ID=10
Tokens=27
T24=24
EOF=-1
T23=23
T22=22
T21=21
FUNC_DECL=7
ARG_DEF=5
WS=20
BLOCK=9
PLUS=19
VOID=16
EQ=11
VAR_DEF=4
EQEQ=17

class SimpleCLexer(Lexer):

    grammarFileName = "SimpleC.g"

    def __init__(self, input=None):
        Lexer.__init__(self, input)





    # $ANTLR start T21
    def mT21(self, ):

        try:
            self.type = T21

            # SimpleC.g:7:5: ( ';' )
            # SimpleC.g:7:7: ';'
            self.match(u';')





        finally:

            pass

    # $ANTLR end T21



    # $ANTLR start T22
    def mT22(self, ):

        try:
            self.type = T22

            # SimpleC.g:8:5: ( '(' )
            # SimpleC.g:8:7: '('
            self.match(u'(')





        finally:

            pass

    # $ANTLR end T22



    # $ANTLR start T23
    def mT23(self, ):

        try:
            self.type = T23

            # SimpleC.g:9:5: ( ',' )
            # SimpleC.g:9:7: ','
            self.match(u',')





        finally:

            pass

    # $ANTLR end T23



    # $ANTLR start T24
    def mT24(self, ):

        try:
            self.type = T24

            # SimpleC.g:10:5: ( ')' )
            # SimpleC.g:10:7: ')'
            self.match(u')')





        finally:

            pass

    # $ANTLR end T24



    # $ANTLR start T25
    def mT25(self, ):

        try:
            self.type = T25

            # SimpleC.g:11:5: ( '{' )
            # SimpleC.g:11:7: '{'
            self.match(u'{')





        finally:

            pass

    # $ANTLR end T25



    # $ANTLR start T26
    def mT26(self, ):

        try:
            self.type = T26

            # SimpleC.g:12:5: ( '}' )
            # SimpleC.g:12:7: '}'
            self.match(u'}')





        finally:

            pass

    # $ANTLR end T26



    # $ANTLR start FOR
    def mFOR(self, ):

        try:
            self.type = FOR

            # SimpleC.g:91:5: ( 'for' )
            # SimpleC.g:91:7: 'for'
            self.match("for")






        finally:

            pass

    # $ANTLR end FOR



    # $ANTLR start INT_TYPE
    def mINT_TYPE(self, ):

        try:
            self.type = INT_TYPE

            # SimpleC.g:92:10: ( 'int' )
            # SimpleC.g:92:12: 'int'
            self.match("int")






        finally:

            pass

    # $ANTLR end INT_TYPE



    # $ANTLR start CHAR
    def mCHAR(self, ):

        try:
            self.type = CHAR

            # SimpleC.g:93:5: ( 'char' )
            # SimpleC.g:93:7: 'char'
            self.match("char")






        finally:

            pass

    # $ANTLR end CHAR



    # $ANTLR start VOID
    def mVOID(self, ):

        try:
            self.type = VOID

            # SimpleC.g:94:5: ( 'void' )
            # SimpleC.g:94:7: 'void'
            self.match("void")






        finally:

            pass

    # $ANTLR end VOID



    # $ANTLR start ID
    def mID(self, ):

        try:
            self.type = ID

            # SimpleC.g:96:5: ( ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_' )* )
            # SimpleC.g:96:9: ( 'a' .. 'z' | 'A' .. 'Z' | '_' ) ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_' )*
            if (u'A' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (u'a' <= self.input.LA(1) <= u'z'):
                self.input.consume();

            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse


            # SimpleC.g:96:33: ( 'a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_' )*
            while True: #loop1
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if ((u'0' <= LA1_0 <= u'9') or (u'A' <= LA1_0 <= u'Z') or LA1_0 == u'_' or (u'a' <= LA1_0 <= u'z')) :
                    alt1 = 1


                if alt1 == 1:
                    # SimpleC.g:
                    if (u'0' <= self.input.LA(1) <= u'9') or (u'A' <= self.input.LA(1) <= u'Z') or self.input.LA(1) == u'_' or (u'a' <= self.input.LA(1) <= u'z'):
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    break #loop1






        finally:

            pass

    # $ANTLR end ID



    # $ANTLR start INT
    def mINT(self, ):

        try:
            self.type = INT

            # SimpleC.g:99:5: ( ( '0' .. '9' )+ )
            # SimpleC.g:99:7: ( '0' .. '9' )+
            # SimpleC.g:99:7: ( '0' .. '9' )+
            cnt2 = 0
            while True: #loop2
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if ((u'0' <= LA2_0 <= u'9')) :
                    alt2 = 1


                if alt2 == 1:
                    # SimpleC.g:99:8: '0' .. '9'
                    self.matchRange(u'0', u'9')



                else:
                    if cnt2 >= 1:
                        break #loop2

                    eee = EarlyExitException(2, self.input)
                    raise eee

                cnt2 += 1






        finally:

            pass

    # $ANTLR end INT



    # $ANTLR start EQ
    def mEQ(self, ):

        try:
            self.type = EQ

            # SimpleC.g:102:6: ( '=' )
            # SimpleC.g:102:8: '='
            self.match(u'=')





        finally:

            pass

    # $ANTLR end EQ



    # $ANTLR start EQEQ
    def mEQEQ(self, ):

        try:
            self.type = EQEQ

            # SimpleC.g:103:6: ( '==' )
            # SimpleC.g:103:8: '=='
            self.match("==")






        finally:

            pass

    # $ANTLR end EQEQ



    # $ANTLR start LT
    def mLT(self, ):

        try:
            self.type = LT

            # SimpleC.g:104:6: ( '<' )
            # SimpleC.g:104:8: '<'
            self.match(u'<')





        finally:

            pass

    # $ANTLR end LT



    # $ANTLR start PLUS
    def mPLUS(self, ):

        try:
            self.type = PLUS

            # SimpleC.g:105:6: ( '+' )
            # SimpleC.g:105:8: '+'
            self.match(u'+')





        finally:

            pass

    # $ANTLR end PLUS



    # $ANTLR start WS
    def mWS(self, ):

        try:
            self.type = WS

            # SimpleC.g:107:5: ( ( ' ' | '\\t' | '\\r' | '\\n' )+ )
            # SimpleC.g:107:9: ( ' ' | '\\t' | '\\r' | '\\n' )+
            # SimpleC.g:107:9: ( ' ' | '\\t' | '\\r' | '\\n' )+
            cnt3 = 0
            while True: #loop3
                alt3 = 2
                LA3_0 = self.input.LA(1)

                if ((u'\t' <= LA3_0 <= u'\n') or LA3_0 == u'\r' or LA3_0 == u' ') :
                    alt3 = 1


                if alt3 == 1:
                    # SimpleC.g:
                    if (u'\t' <= self.input.LA(1) <= u'\n') or self.input.LA(1) == u'\r' or self.input.LA(1) == u' ':
                        self.input.consume();

                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse




                else:
                    if cnt3 >= 1:
                        break #loop3

                    eee = EarlyExitException(3, self.input)
                    raise eee

                cnt3 += 1


            #action start
            self.channel=HIDDEN 
            #action end




        finally:

            pass

    # $ANTLR end WS



    def mTokens(self):
        # SimpleC.g:1:8: ( T21 | T22 | T23 | T24 | T25 | T26 | FOR | INT_TYPE | CHAR | VOID | ID | INT | EQ | EQEQ | LT | PLUS | WS )
        alt4 = 17
        LA4 = self.input.LA(1)
        if LA4 == u';':
            alt4 = 1
        elif LA4 == u'(':
            alt4 = 2
        elif LA4 == u',':
            alt4 = 3
        elif LA4 == u')':
            alt4 = 4
        elif LA4 == u'{':
            alt4 = 5
        elif LA4 == u'}':
            alt4 = 6
        elif LA4 == u'f':
            LA4_7 = self.input.LA(2)

            if (LA4_7 == u'o') :
                LA4_17 = self.input.LA(3)

                if (LA4_17 == u'r') :
                    LA4_23 = self.input.LA(4)

                    if ((u'0' <= LA4_23 <= u'9') or (u'A' <= LA4_23 <= u'Z') or LA4_23 == u'_' or (u'a' <= LA4_23 <= u'z')) :
                        alt4 = 11
                    else:
                        alt4 = 7
                else:
                    alt4 = 11
            else:
                alt4 = 11
        elif LA4 == u'i':
            LA4_8 = self.input.LA(2)

            if (LA4_8 == u'n') :
                LA4_18 = self.input.LA(3)

                if (LA4_18 == u't') :
                    LA4_24 = self.input.LA(4)

                    if ((u'0' <= LA4_24 <= u'9') or (u'A' <= LA4_24 <= u'Z') or LA4_24 == u'_' or (u'a' <= LA4_24 <= u'z')) :
                        alt4 = 11
                    else:
                        alt4 = 8
                else:
                    alt4 = 11
            else:
                alt4 = 11
        elif LA4 == u'c':
            LA4_9 = self.input.LA(2)

            if (LA4_9 == u'h') :
                LA4_19 = self.input.LA(3)

                if (LA4_19 == u'a') :
                    LA4_25 = self.input.LA(4)

                    if (LA4_25 == u'r') :
                        LA4_29 = self.input.LA(5)

                        if ((u'0' <= LA4_29 <= u'9') or (u'A' <= LA4_29 <= u'Z') or LA4_29 == u'_' or (u'a' <= LA4_29 <= u'z')) :
                            alt4 = 11
                        else:
                            alt4 = 9
                    else:
                        alt4 = 11
                else:
                    alt4 = 11
            else:
                alt4 = 11
        elif LA4 == u'v':
            LA4_10 = self.input.LA(2)

            if (LA4_10 == u'o') :
                LA4_20 = self.input.LA(3)

                if (LA4_20 == u'i') :
                    LA4_26 = self.input.LA(4)

                    if (LA4_26 == u'd') :
                        LA4_30 = self.input.LA(5)

                        if ((u'0' <= LA4_30 <= u'9') or (u'A' <= LA4_30 <= u'Z') or LA4_30 == u'_' or (u'a' <= LA4_30 <= u'z')) :
                            alt4 = 11
                        else:
                            alt4 = 10
                    else:
                        alt4 = 11
                else:
                    alt4 = 11
            else:
                alt4 = 11
        elif LA4 == u'A' or LA4 == u'B' or LA4 == u'C' or LA4 == u'D' or LA4 == u'E' or LA4 == u'F' or LA4 == u'G' or LA4 == u'H' or LA4 == u'I' or LA4 == u'J' or LA4 == u'K' or LA4 == u'L' or LA4 == u'M' or LA4 == u'N' or LA4 == u'O' or LA4 == u'P' or LA4 == u'Q' or LA4 == u'R' or LA4 == u'S' or LA4 == u'T' or LA4 == u'U' or LA4 == u'V' or LA4 == u'W' or LA4 == u'X' or LA4 == u'Y' or LA4 == u'Z' or LA4 == u'_' or LA4 == u'a' or LA4 == u'b' or LA4 == u'd' or LA4 == u'e' or LA4 == u'g' or LA4 == u'h' or LA4 == u'j' or LA4 == u'k' or LA4 == u'l' or LA4 == u'm' or LA4 == u'n' or LA4 == u'o' or LA4 == u'p' or LA4 == u'q' or LA4 == u'r' or LA4 == u's' or LA4 == u't' or LA4 == u'u' or LA4 == u'w' or LA4 == u'x' or LA4 == u'y' or LA4 == u'z':
            alt4 = 11
        elif LA4 == u'0' or LA4 == u'1' or LA4 == u'2' or LA4 == u'3' or LA4 == u'4' or LA4 == u'5' or LA4 == u'6' or LA4 == u'7' or LA4 == u'8' or LA4 == u'9':
            alt4 = 12
        elif LA4 == u'=':
            LA4_13 = self.input.LA(2)

            if (LA4_13 == u'=') :
                alt4 = 14
            else:
                alt4 = 13
        elif LA4 == u'<':
            alt4 = 15
        elif LA4 == u'+':
            alt4 = 16
        elif LA4 == u'\t' or LA4 == u'\n' or LA4 == u'\r' or LA4 == u' ':
            alt4 = 17
        else:
            nvae = NoViableAltException("1:1: Tokens : ( T21 | T22 | T23 | T24 | T25 | T26 | FOR | INT_TYPE | CHAR | VOID | ID | INT | EQ | EQEQ | LT | PLUS | WS );", 4, 0, self.input)

            raise nvae

        if alt4 == 1:
            # SimpleC.g:1:10: T21
            self.mT21()



        elif alt4 == 2:
            # SimpleC.g:1:14: T22
            self.mT22()



        elif alt4 == 3:
            # SimpleC.g:1:18: T23
            self.mT23()



        elif alt4 == 4:
            # SimpleC.g:1:22: T24
            self.mT24()



        elif alt4 == 5:
            # SimpleC.g:1:26: T25
            self.mT25()



        elif alt4 == 6:
            # SimpleC.g:1:30: T26
            self.mT26()



        elif alt4 == 7:
            # SimpleC.g:1:34: FOR
            self.mFOR()



        elif alt4 == 8:
            # SimpleC.g:1:38: INT_TYPE
            self.mINT_TYPE()



        elif alt4 == 9:
            # SimpleC.g:1:47: CHAR
            self.mCHAR()



        elif alt4 == 10:
            # SimpleC.g:1:52: VOID
            self.mVOID()



        elif alt4 == 11:
            # SimpleC.g:1:57: ID
            self.mID()



        elif alt4 == 12:
            # SimpleC.g:1:60: INT
            self.mINT()



        elif alt4 == 13:
            # SimpleC.g:1:64: EQ
            self.mEQ()



        elif alt4 == 14:
            # SimpleC.g:1:67: EQEQ
            self.mEQEQ()



        elif alt4 == 15:
            # SimpleC.g:1:72: LT
            self.mLT()



        elif alt4 == 16:
            # SimpleC.g:1:75: PLUS
            self.mPLUS()



        elif alt4 == 17:
            # SimpleC.g:1:80: WS
            self.mWS()








 

