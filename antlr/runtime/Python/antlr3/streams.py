"""ANTLR3 runtime package"""

# begin[licence]
#
# [The "BSD licence"]
# Copyright (c) 2005-2006 Terence Parr
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# end[licence]

import codecs
from StringIO import StringIO

from antlr3.constants import DEFAULT_CHANNEL, EOF
from antlr3.tokens import Token, EOF_TOKEN


############################################################################
#
# basic interfaces
#   IntStream
#    +- CharStream
#    \- TokenStream7
#
# subclasses must implemented all methods
#
############################################################################

class IntStream(object):
    """
    @brief Base interface for streams of integer values.

    A simple stream of integers used when all I care about is the char
    or token type sequence (such as interpretation).
    """
    
    def consume(self):
        raise NotImplementedError
    

    def LA(self, i):
        """Get int at current input pointer + i ahead where i=1 is next int.

        Negative indexes are allowed.  LA(-1) is previous token (token
	just matched).  LA(-i) where i is before first token should
	yield -1, invalid char / EOF.
	"""
        
        raise NotImplementedError
        

    def mark(self):
        """
        Tell the stream to start buffering if it hasn't already.  Return
        current input position, index(), or some other marker so that
        when passed to rewind() you get back to the same spot.
        rewind(mark()) should not affect the input cursor.  The Lexer
        track line/col info as well as input index so its markers are
        not pure input indexes.  Same for tree node streams.
        """

        raise NotImplementedError


    def index(self):
        """
        Return the current input symbol index 0..n where n indicates the
        last symbol has been read.  The index is the symbol about to be
        read not the most recently read symbol.
        """

        raise NotImplementedError


    def rewind(self, marker=None):
        """
        Reset the stream so that next call to index would return marker.
        The marker will usually be index() but it doesn't have to be.  It's
        just a marker to indicate what state the stream was in.  This is
        essentially calling release() and seek().  If there are markers
        created after this marker argument, this routine must unroll them
        like a stack.  Assume the state the stream was in when this marker
        was created.

        If marker is None:
        Rewind to the input position of the last marker.
        Used currently only after a cyclic DFA and just
        before starting a sem/syn predicate to get the
        input position back to the start of the decision.
        Do not "pop" the marker off the state.  mark(i)
        and rewind(i) should balance still. It is
        like invoking rewind(last marker) but it should not "pop"
        the marker off.  It's like seek(last marker's input position).       
	"""

        raise NotImplementedError


    def release(self, marker=None):
        """
        You may want to commit to a backtrack but don't want to force the
        stream to keep bookkeeping objects around for a marker that is
        no longer necessary.  This will have the same behavior as
        rewind() except it releases resources without the backward seek.
        This must throw away resources for all markers back to the marker
        argument.  So if you're nested 5 levels of mark(), and then release(2)
        you have to release resources for depths 2..5.
	"""

        raise NotImplementedError


    def seek(self, index):
        """
        Set the input cursor to the position indicated by index.  This is
        normally used to seek ahead in the input stream.  No buffering is
        required to do this unless you know your stream will use seek to
        move backwards such as when backtracking.

        This is different from rewind in its multi-directional
        requirement and in that its argument is strictly an input cursor
        (index).

        For char streams, seeking forward must update the stream state such
        as line number.  For seeking backwards, you will be presumably
        backtracking using the mark/rewind mechanism that restores state and
        so this method does not need to update state when seeking backwards.

        Currently, this method is only used for efficient backtracking using
        memoization, but in the future it may be used for incremental parsing.

        The index is 0..n-1.  A seek to position i means that LA(1) will
        return the ith symbol.  So, seeking to 0 means LA(1) will return the
        first element in the stream. 
        """

        raise NotImplementedError


    def size(self):
        """
        Only makes sense for streams that buffer everything up probably, but
        might be useful to display the entire stream or for testing.  This
        value includes a single EOF.
	"""

        raise NotImplementedError



class CharStream(IntStream):
    """
    @brief A source of characters for an ANTLR lexer.

    This is an abstract class that must be implemented by a subclass.
    
    """

    # pylint does not realize that this is an interface, too
    #pylint: disable-msg=W0223
    
    EOF = -1


    def substring(self, start, stop):
        """
        For infinite streams, you don't need this; primarily I'm providing
        a useful interface for action code.  Just make sure actions don't
        use this on streams that don't support it.
        """

        raise NotImplementedError
        
    
    def LT(self, i):
        """
        Get the ith character of lookahead.  This is the same usually as
        LA(i).  This will be used for labels in the generated
        lexer code.  I'd prefer to return a char here type-wise, but it's
        probably better to be 32-bit clean and be consistent with LA.
        """

        raise NotImplementedError


    def getLine(self):
        """ANTLR tracks the line information automatically"""

        raise NotImplementedError


    def setLine(self, line):
        """
        Because this stream can rewind, we need to be able to reset the line
        """

        raise NotImplementedError


    def getCharPositionInLine(self):
        """
        The index of the character relative to the beginning of the line 0..n-1
        """

        raise NotImplementedError


    def setCharPositionInLine(self, pos):
        raise NotImplementedError


class TokenStream(IntStream):
    """

    @brief A stream of tokens accessing tokens from a TokenSource

    This is an abstract class that must be implemented by a subclass.
    
    """
    
    # pylint does not realize that this is an interface, too
    #pylint: disable-msg=W0223
    
    def LT(self, k):
        """
        Get Token at current input pointer + i ahead where i=1 is next Token.
        i<0 indicates tokens in the past.  So -1 is previous token and -2 is
        two tokens ago. LT(0) is undefined.  For i>=n, return Token.EOFToken.
        Return null for LT(0) and any index that results in an absolute address
        that is negative.
	"""

        raise NotImplementedError


    def get(self, i):
        """
        Get a token at an absolute index i; 0..n-1.  This is really only
        needed for profiling and debugging and token stream rewriting.
        If you don't want to buffer up tokens, then this method makes no
        sense for you.  Naturally you can't use the rewrite stream feature.
        I believe DebugTokenStream can easily be altered to not use
        this method, removing the dependency.
        """

        raise NotImplementedError


    def getTokenSource(self):
        """
        Where is this stream pulling tokens from?  This is not the name, but
        the object that provides Token objects.
	"""

        raise NotImplementedError


    def toString(self, start=None, stop=None):
        """
        Return the text of all tokens from start to stop, inclusive.
        If the stream does not buffer all the tokens then it can just
        return "" or null;  Users should not access $ruleLabel.text in
        an action of course in that case.

        Because the user is not required to use a token with an index stored
        in it, we must provide a means for two token objects themselves to
        indicate the start/end location.  Most often this will just delegate
        to the other toString(int,int).  This is also parallel with
        the TreeNodeStream.toString(Object,Object).
	"""

        raise NotImplementedError

        
############################################################################
#
# character streams for use in lexers
#   CharStream
#   \- ANTLRStringStream
#
############################################################################


class ANTLRStringStream(CharStream):
    """
    @brief CharStream that pull data from a unicode string.
    
    A pretty quick CharStream that pulls all data from an array
    directly.  Every method call counts in the lexer.

    """

    
    def __init__(self, data):
        """
        @param data This should be a unicode string holding the data you want
           to parse. If you pass in a byte string, the Lexer will choke on
           non-ascii data.
           
        """
        
        CharStream.__init__(self)
        
  	# The data being scanned
        self.data = data

	# How many characters are actually in the buffer
        self.n = len(data)

 	# 0..n-1 index into string of next char
        self.p = 0

	# line number 1..n within the input
        self.line = 1

 	# The index of the character relative to the beginning of the
        # line 0..n-1
        self.charPositionInLine = 0

	# A list of CharStreamState objects that tracks the stream state
        # values line, charPositionInLine, and p that can change as you
        # move through the input stream.  Indexed from 0..markDepth-1.
        self._markers = [ ]
        self.lastMarker = None
        self.markDepth = 0
        

    def reset(self):
        """
        Reset the stream so that it's in the same state it was
        when the object was created *except* the data array is not
        touched.
        """
        
        self.p = 0
        self.line = 1
        self.charPositionInLine = 0
        self._markers = [ ]


    def consume(self):
        if self.p < self.n:
            self.charPositionInLine += 1
            if self.data[self.p] == '\n':
                self.line += 1
                self.charPositionInLine = 0

            self.p += 1


    def LA(self, i):
        if i == 0:
            return 0 # undefined

        if i < 0:
            i += 1 # e.g., translate LA(-1) to use offset i=0; then data[p+0-1]
            if self.p+i-1 < 0:
                return EOF # invalid; no char before first char

        if self.p+i-1 >= self.n:
            return EOF

        return self.data[self.p+i-1]

    LT = LA

    def index(self):
        """
        Return the current input symbol index 0..n where n indicates the
        last symbol has been read.  The index is the index of char to
        be returned from LA(1).
        """
        
        return self.p


    def size(self):
        return self.n


    def mark(self):
        state = (self.p, self.line, self.charPositionInLine)
        try:
            self._markers[self.markDepth] = state
        except IndexError:
            self._markers.append(state)
        self.markDepth += 1
        
        self.lastMarker = self.markDepth
        
        return self.lastMarker


    def rewind(self, marker=None):
        if marker is None:
            marker = self.lastMarker

        p, line, charPositionInLine = self._markers[marker-1]

        self.seek(p)
        self.line = line
        self.charPositionInLine = charPositionInLine
        self.release(marker)


    def release(self, marker=None):
        if marker is None:
            marker = self.lastMarker

        self.markDepth = marker-1


    def seek(self, index):
        """
        consume() ahead until p==index; can't just set p=index as we must
        update line and charPositionInLine.
        """
        
        if index <= self.p:
            self.p = index # just jump; don't update stream state (line, ...)
            return

        # seek forward, consume until p hits index
        while self.p < index:
            self.consume()


    def substring(self, start, stop):
        return self.data[start:stop+1]


    def getLine(self):
        """Using setter/getter methods is deprecated. Use o.line instead."""
        return self.line


    def getCharPositionInLine(self):
        """Using setter/getter methods is deprecated. Use o.charPositionInLine instead."""
        return self.charPositionInLine


    def setLine(self, line):
        """Using setter/getter methods is deprecated. Use o.line instead."""
        self.line = line


    def setCharPositionInLine(self, pos):
        """Using setter/getter methods is deprecated. Use o.charPositionInLine instead."""
        self.charPositionInLine = pos


class ANTLRFileStream(ANTLRStringStream):
    """
    @brief CharStream that opens a file to read the data.
    
    This is a char buffer stream that is loaded from a file
    all at once when you construct the object.
    """

    def __init__(self, fileName, encoding=None):
        """
        @param fileName The path to the file to be opened. The file will be
           opened with mode 'rb'.

        @param encoding If you set the optional encoding argument, then the
           data will be decoded on the fly.
           
        """
        
        self.fileName = fileName

        fp = codecs.open(fileName, 'rb', encoding)
        try:
            data = fp.read()
        finally:
            fp.close()
            
        ANTLRStringStream.__init__(self, data)


    def getSourceName(self):
        """Deprecated, access o.fileName directly."""
        
        return self.fileName


class ANTLRInputStream(ANTLRStringStream):
    """
    @brief CharStream that reads data from a file-like object.

    This is a char buffer stream that is loaded from a file like object
    all at once when you construct the object.
    
    All input is consumed from the file, but it is not closed.
    """

    def __init__(self, file, encoding=None):
        """
        @param file A file-like object holding your input. Only the read()
           method must be implemented.

        @param encoding If you set the optional encoding argument, then the
           data will be decoded on the fly.
           
        """
        
        if encoding is not None:
            # wrap input in a decoding reader
            reader = codecs.lookup(encoding)[2]
            file = reader(file)

        data = file.read()
            
        ANTLRStringStream.__init__(self, data)


# I guess the ANTLR prefix exists only to avoid a name clash with some Java
# mumbojumbo. A plain "StringStream" looks better to me, which should be
# the preferred name in Python.
StringStream = ANTLRStringStream
FileStream = ANTLRFileStream
InputStream = ANTLRInputStream


############################################################################
#
# Token streams
#   TokenStream
#   +- CommonTokenStream
#   \- TokenRewriteStream
#
############################################################################


class CommonTokenStream(TokenStream):
    """
    @brief The most common stream of tokens
    
    The most common stream of tokens is one where every token is buffered up
    and tokens are prefiltered for a certain channel (the parser will only
    see these tokens and cannot change the filter channel number during the
    parse).
    """

    def __init__(self, tokenSource=None, channel=DEFAULT_CHANNEL):
        """
        @param tokenSource A TokenSource instance (usually a Lexer) to pull
            the tokens from.

        @param channel Skip tokens on any channel but this one; this is how we
            skip whitespace...
            
        """
        
        TokenStream.__init__(self)
        
        self.tokenSource = tokenSource

	# Record every single token pulled from the source so we can reproduce
        # chunks of it later.
        self.tokens = []

	# Map<tokentype, channel> to override some Tokens' channel numbers
        self.channelOverrideMap = {}

	# Set<tokentype>; discard any tokens with this type
        self.discardSet = set()

	# Skip tokens on any channel but this one; this is how we skip whitespace...
        self.channel = channel

	# By default, track all incoming tokens
        self.discardOffChannelTokens = False

	# The index into the tokens list of the current token (next token
        # to consume).  p==-1 indicates that the tokens list is empty
        self.p = -1

        # Remember last marked position
        self.lastMarker = None
        

    def setTokenSource(self, tokenSource):
        """Reset this token stream by setting its token source."""
        
        self.tokenSource = tokenSource
        self.tokens = []
        self.p = -1
        self.channel = DEFAULT_CHANNEL


    def fillBuffer(self):
        """
        Load all tokens from the token source and put in tokens.
	This is done upon first LT request because you might want to
        set some token type / channel overrides before filling buffer.
        """
        

        index = 0
        t = self.tokenSource.nextToken()
        while t is not None and t.type != EOF:
            discard = False
            
            if self.discardSet is not None and t.type in self.discardSet:
                discard = True

            elif self.discardOffChannelTokens and t.channel != self.channel:
                discard = True

            # is there a channel override for token type?
            try:
                overrideChannel = self.channelOverrideMap[t.type]
                
            except KeyError:
                # no override for this type
                pass
            
            else:
                if overrideChannel == self.channel:
                    t.channel = overrideChannel
                else:
                    discard = True
            
            if not discard:
                t.index = index
                self.tokens.append(t)
                index += 1

            t = self.tokenSource.nextToken()
       
        # leave p pointing at first token on channel
        self.p = 0
        self.p = self.skipOffTokenChannels(self.p)


    def consume(self):
        """
        Move the input pointer to the next incoming token.  The stream
        must become active with LT(1) available.  consume() simply
        moves the input pointer so that LT(1) points at the next
        input symbol. Consume at least one token.

        Walk past any token not on the channel the parser is listening to.
        """
        
        if self.p < len(self.tokens):
            self.p += 1

            self.p = self.skipOffTokenChannels(self.p) # leave p on valid token


    def skipOffTokenChannels(self, i):
        """
        Given a starting index, return the index of the first on-channel
        token.
        """

        n = len(self.tokens)
        while i < n and self.tokens[i].channel != self.channel:
            i += 1

        return i


    def skipOffTokenChannelsReverse(self, i):
        while i >= 0 and self.tokens[i].channel != self.channel:
            i -= 1

        return i


    def setTokenTypeChannel(self, ttype, channel):
        """
        A simple filter mechanism whereby you can tell this token stream
        to force all tokens of type ttype to be on channel.  For example,
        when interpreting, we cannot exec actions so we need to tell
        the stream to force all WS and NEWLINE to be a different, ignored
        channel.
	"""
        
        self.channelOverrideMap[ttype] = channel


    def discardTokenType(self, ttype):
        self.discardSet.add(ttype)


    def getTokens(self, start=None, stop=None, types=None):
        """
        Given a start and stop index, return a list of all tokens in
        the token type set.  Return None if no tokens were found.  This
        method looks at both on and off channel tokens.
        """

        if self.p == -1:
            self.fillBuffer()

        if stop is None or stop >= len(self.tokens):
            stop = len(self.tokens) - 1
            
        if start is None or stop < 0:
            start = 0

        if start > stop:
            return None

        if isinstance(types, (int, long)):
            # called with a single type, wrap into set
            types = set([types])
            
        filteredTokens = [
            token for token in self.tokens[start:stop]
            if types is None or token.type in types
            ]

        if len(filteredTokens) == 0:
            return None

        return filteredTokens


    def LT(self, k):
        """
        Get the ith token from the current position 1..n where k=1 is the
        first symbol of lookahead.
        """

        if self.p == -1:
            self.fillBuffer()

        if k == 0:
            return None

        if k < 0:
            return self.LB(-k)
                
        if self.p + k - 1 >= len(self.tokens):
            return EOF_TOKEN

        i = self.p
        n = 1
        # find k good tokens
        while n < k:
            # skip off-channel tokens
            i = self.skipOffTokenChannels(i+1) # leave p on valid token
            n += 1
        
        if i >= len(self.tokens):
            return EOF_TOKEN

        return self.tokens[i]


    def LB(self, k):
        """Look backwards k tokens on-channel tokens"""

        if self.p == -1:
            self.fillBuffer()

        if k == 0:
            return None

        if self.p - k < 0:
            return None

        i = self.p
        n = 1
        # find k good tokens looking backwards
        while n <= k:
            # skip off-channel tokens
            i = self.skipOffTokenChannelsReverse(i-1) # leave p on valid token
            n += 1

        if i < 0:
            return None
            
        return self.tokens[i]


    def get(self, i):
        """
        Return absolute token i; ignore which channel the tokens are on;
        that is, count all tokens not just on-channel tokens.
        """

        return self.tokens[i]


    def LA(self, i):
        return self.LT(i).type


    def mark(self):
        self.lastMarker = self.index()
        return self.lastMarker
    

    def release(self, marker=None):
        # no resources to release
        pass
    

    def size(self):
        return len(self.tokens)


    def index(self):
        return self.p


    def rewind(self, marker=None):
        if marker is None:
            marker = self.lastMarker
            
        self.seek(marker)


    def seek(self, index):
        self.p = index


    def getTokenSource(self):
        return self.tokenSource


    def toString(self, start=None, stop=None):
        if self.p == -1:
            self.fillBuffer()

        if start is None:
            start = 0
        elif not isinstance(start, int):
            start = start.index

        if stop is None:
            stop = len(self.tokens) - 1
        elif not isinstance(stop, int):
            stop = stop.index
        
        if stop >= len(self.tokens):
            stop = len(self.tokens) - 1

        return ''.join([t.text for t in self.tokens[start:stop+1]])


class RewriteOperation(object):
    """@brief Internal helper class."""
    
    def __init__(self, index, text):
        self.index = index
        self.text = text

    def execute(self, buf):
        """Execute the rewrite operation by possibly adding to the buffer.
        Return the index of the next token to operate on.
        """

        return self.index

    def toString(self):
        opName = self.__class__.__name__
        return opName+"@"+self.index+'"'+self.text+'"'

    __str__ = toString


class InsertBeforeOp(RewriteOperation):
    """@brief Internal helper class."""

    def execute(self, buf):
        buf.write(self.text)
        return self.index


class ReplaceOp(RewriteOperation):
    """
    @brief Internal helper class.
    
    I'm going to try replacing range from x..y with (y-x)+1 ReplaceOp
    instructions.
    """

    def __init__(self, first, last, text):
        RewriteOperation.__init__(self, first, text)
        self.lastIndex = last


    def execute(self, buf):
        if self.text is not None:
            buf.write(self.text)

        return self.lastIndex + 1


class TokenRewriteStream(CommonTokenStream):
    """@brief CommonTokenStream that can be modified.

    Useful for dumping out the input stream after doing some
    augmentation or other manipulations.

    You can insert stuff, replace, and delete chunks.  Note that the
    operations are done lazily--only if you convert the buffer to a
    String.  This is very efficient because you are not moving data around
    all the time.  As the buffer of tokens is converted to strings, the
    toString() method(s) check to see if there is an operation at the
    current index.  If so, the operation is done and then normal String
    rendering continues on the buffer.  This is like having multiple Turing
    machine instruction streams (programs) operating on a single input tape. :)

    Since the operations are done lazily at toString-time, operations do not
    screw up the token index values.  That is, an insert operation at token
    index i does not change the index values for tokens i+1..n-1.

    Because operations never actually alter the buffer, you may always get
    the original token stream back without undoing anything.  Since
    the instructions are queued up, you can easily simulate transactions and
    roll back any changes if there is an error just by removing instructions.
    For example,

     CharStream input = new ANTLRFileStream("input");
     TLexer lex = new TLexer(input);
     TokenRewriteStream tokens = new TokenRewriteStream(lex);
     T parser = new T(tokens);
     parser.startRule();

     Then in the rules, you can execute
        Token t,u;
        ...
        input.insertAfter(t, "text to put after t");}
        input.insertAfter(u, "text after u");}
        System.out.println(tokens.toString());

    Actually, you have to cast the 'input' to a TokenRewriteStream. :(

    You can also have multiple "instruction streams" and get multiple
    rewrites from a single pass over the input.  Just name the instruction
    streams and use that name again when printing the buffer.  This could be
    useful for generating a C file and also its header file--all from the
    same buffer:

        tokens.insertAfter("pass1", t, "text to put after t");}
        tokens.insertAfter("pass2", u, "text after u");}
        System.out.println(tokens.toString("pass1"));
        System.out.println(tokens.toString("pass2"));

    If you don't use named rewrite streams, a "default" stream is used as
    the first example shows.
    """
    
    DEFAULT_PROGRAM_NAME = "default"
    MIN_TOKEN_INDEX = 0

    def __init__(self, tokenSource=None, channel=DEFAULT_CHANNEL):
        CommonTokenStream.__init__(self, tokenSource, channel)

        # You may have multiple, named streams of rewrite operations.
        # I'm calling these things "programs."
        #  Maps String (name) -> rewrite (List)
        self.programs = {}
        self.programs[self.DEFAULT_PROGRAM_NAME] = []
        
 	# Map String (program name) -> Integer index
        self.lastRewriteTokenIndexes = {}
        

    def rollback(self, *args):
        """
        Rollback the instruction stream for a program so that
        the indicated instruction (via instructionIndex) is no
        longer in the stream.  UNTESTED!
        """

        if len(args) == 2:
            programName = args[0]
            instructionIndex = args[1]
        elif len(args) == 1:
            programName = self.DEFAULT_PROGRAM_NAME
            instructionIndex = args[0]
        else:
            raise TypeError("Invalid arguments")
        
        p = self.programs.get(programName, None)
        if p is not None:
            self.programs[programName] = p[self.MIN_TOKEN_INDEX:instructionIndex]


    def deleteProgram(self, programName=DEFAULT_PROGRAM_NAME):
        """Reset the program so that no instructions exist"""
            
        self.rollback(programName, self.MIN_TOKEN_INDEX)


    def addToSortedRewriteList(self, *args):
        """
        Add an instruction to the rewrite instruction list ordered by
        the instruction number (do not use a binary search for bad efficiency).
        The list is ordered so that toString() can be done efficiently.

        When there are multiple instructions at the same index, the instructions
        must be ordered to ensure proper behavior.  For example, a delete at
        index i must kill any replace operation at i.  Insert-before operations
        must come before any replace / delete instructions.  If there are
        multiple insert instructions for a single index, they are done in
        reverse insertion order so that "insert foo" then "insert bar" yields
        "foobar" in front rather than "barfoo".  This is convenient because
        I can insert new InsertOp instructions at the index returned by
        the binary search.  A ReplaceOp kills any previous replace op.  Since
        delete is the same as replace with null text, i can check for
        ReplaceOp and cover DeleteOp at same time. :)
        """

        if len(args) == 2:
            programName = args[0]
            op = args[1]
        elif len(args) == 1:
            programName = self.DEFAULT_PROGRAM_NAME
            op = args[0]
        else:
            raise TypeError("Invalid arguments")
        
        rewrites = self.getProgram(programName)
        #System.out.println("### add "+op+"; rewrites="+rewrites)

        # first insert position for operation
        for pos, searchOp in enumerate(rewrites):
            if searchOp.index == op.index:
                # now pos is the index in rewrites of first op with op.index
                #System.out.println("first op with op.index: pos="+pos)

                # an instruction operating already on that index was found;
                # make this one happen after all the others
                #System.out.println("found instr for index="+op.index)
                if isinstance(op, ReplaceOp):
                    replaced = False
                    i = pos
                    # look for an existing replace
                    while i < len(rewrites):
                        prevOp = rewrites[pos]
                        if prevOp.index != op.index:
                            break

                        if isinstance(prevOp, ReplaceOp):
                            rewrites[pos] = op # replace old with new
                            replaced = True
                            break

                        # keep going; must be an insert
                        i += 1
                        
                    if not replaced:
                        # add replace op to the end of all the inserts
                        rewrites.insert(i, op)

                else:
                    # inserts are added in front of existing inserts
                    rewrites.insert(pos, op)

                break

            elif searchOp.index > op.index:
                #System.out.println("no instruction at pos=="+pos)
                rewrites.insert(pos, op)
                break
            
        else:
            # new op is past any existing op, append to end
            rewrites.append(op)
            
        #System.out.println("after, rewrites="+rewrites)


    def insertAfter(self, *args):
        if len(args) == 2:
            programName = self.DEFAULT_PROGRAM_NAME
            index = args[0]
            text = args[1]
            
        elif len(args) == 3:
            programName = args[0]
            index = args[1]
            text = args[2]

        else:
            raise TypeError("Invalid arguments")

        if isinstance(index, Token):
            # index is a Token, grap the stream index from it
            index = index.index

        # to insert after, just insert before next index (even if past end)
        self.insertBefore(programName, index+1, text)


    def insertBefore(self, *args):
        if len(args) == 2:
            programName = self.DEFAULT_PROGRAM_NAME
            index = args[0]
            text = args[1]
            
        elif len(args) == 3:
            programName = args[0]
            index = args[1]
            text = args[2]

        else:
            raise TypeError("Invalid arguments")

        if isinstance(index, Token):
            # index is a Token, grap the stream index from it
            index = index.index

        self.addToSortedRewriteList(
            programName,
            InsertBeforeOp(index, text)
            )


    def replace(self, *args):
        if len(args) == 2:
            programName = self.DEFAULT_PROGRAM_NAME
            first = args[0]
            last = args[0]
            text = args[1]
            
        elif len(args) == 3:
            programName = self.DEFAULT_PROGRAM_NAME
            first = args[0]
            last = args[1]
            text = args[2]
            
        elif len(args) == 4:
            programName = args[0]
            first = args[1]
            last = args[2]
            text = args[3]

        else:
            raise TypeError("Invalid arguments")

        if isinstance(first, Token):
            # first is a Token, grap the stream index from it
            first = first.index

        if isinstance(last, Token):
            # last is a Token, grap the stream index from it
            last = last.index

        if first > last or first < 0 or last < 0:
            return
        
        self.addToSortedRewriteList(
            programName,
            ReplaceOp(first, last, text)
            )
        

    def delete(self, *args):
        self.replace(*(list(args) + [None]))


    def getLastRewriteTokenIndex(self, programName=DEFAULT_PROGRAM_NAME):
        return self.lastRewriteTokenIndexes.get(programName, -1)


    def setLastRewriteTokenIndex(self, programName, i):
        self.lastRewriteTokenIndexes[programName] = i


    def getProgram(self, name):
        p = self.programs.get(name, None)
        if p is  None:
            p = self.initializeProgram(name)

        return p


    def initializeProgram(self, name):
        p = []
        self.programs[name] = p
        return p


    def toOriginalString(self, start=None, end=None):
        if start is None:
            start = self.MIN_TOKEN_INDEX
        if end is None:
            end = self.size() - 1
        
        buf = StringIO()
        i = start
        while i >= self.MIN_TOKEN_INDEX and i <= end and i < len(self.tokens):
            buf.write(self.get(i).text)
            i += 1

        return buf.getvalue()


    def toString(self, *args):
        if len(args) == 0:
            programName = self.DEFAULT_PROGRAM_NAME
            start = self.MIN_TOKEN_INDEX
            end = self.size() - 1
            
        elif len(args) == 1:
            programName = args[0]
            start = self.MIN_TOKEN_INDEX
            end = self.size() - 1

        elif len(args) == 2:
            programName = self.DEFAULT_PROGRAM_NAME
            start = args[0]
            end = args[1]
            
        rewrites = self.programs.get(programName)
        if rewrites is None or len(rewrites) == 0:
            # no instructions to execute
            return self.toOriginalString(start, end)
        
        buf = StringIO()

        # Index of first rewrite we have not done
        rewriteOpIndex = 0

        tokenCursor = start
        while ( tokenCursor >= self.MIN_TOKEN_INDEX
                and tokenCursor <= end
                and tokenCursor < len(self.tokens)
                ):
            #System.out.println("tokenCursor="+tokenCursor);
            # execute instructions associated with this token index
            if rewriteOpIndex < len(rewrites):
                op = rewrites[rewriteOpIndex]

                # skip all ops at lower index
                while ( op.index < tokenCursor
                        and rewriteOpIndex < len(rewrites)
                        ):
                    rewriteOpIndex += 1
                    if rewriteOpIndex < len(rewrites):
                        op = rewrites[rewriteOpIndex]

                # while we have ops for this token index, exec them
                while ( tokenCursor == op.index
                        and rewriteOpIndex < len(rewrites)
                        ):
                    #System.out.println("execute "+op+" at instruction "+rewriteOpIndex);
                    tokenCursor = op.execute(buf)
                    #System.out.println("after execute tokenCursor = "+tokenCursor);
                    rewriteOpIndex += 1
                    if rewriteOpIndex < len(rewrites):
                        op = rewrites[rewriteOpIndex]

            # dump the token at this index
            if tokenCursor <= end:
                buf.write(self.get(tokenCursor).text)
                tokenCursor += 1
        
        # now see if there are operations (append) beyond last token index
        for opi in range(rewriteOpIndex, len(rewrites)):
            op = rewrites[opi]
            
            if op.index >= self.size():
                op.execute(buf) # must be insertions if after last token

            #System.out.println("execute "+op+" at "+opi);
            #op.execute(buf); # must be insertions if after last token


        return buf.getvalue()

    __str__ = toString
    

    def toDebugString(self, start=None, end=None):
        if start is None:
            start = self.MIN_TOKEN_INDEX
        if end is None:
            end = self.size() - 1
        
        buf = StringIO()
        i = start
        while i >= self.MIN_TOKEN_INDEX and i <= end and i < len(self.tokens):
            buf.write(self.get(i))
            i += 1

        return buf.getvalue()