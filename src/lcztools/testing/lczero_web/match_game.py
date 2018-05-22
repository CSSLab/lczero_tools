import posixpath
import requests
import bs4
import re
from lcztools import LeelaBoard
from lcztools.util import lazy_property
import chess
import chess.pgn

class WebMatchGame:
    BASE_URL = 'http://www.lczero.org/match_game'
    def __init__(self, url):
        '''Create a web match game object.
        
        URL may be the full URL, such as 'http://www.lczero.org/match_game/298660'
        or just a portion, like '298660'. Only the last portion is used'''
        url = url.rstrip('/').rsplit('/', 1)[-1]
        self.url = posixpath.join(self.BASE_URL, url)

    @lazy_property
    def text(self):
        return requests.get(self.url).text
    
    @lazy_property
    def soup(self):
        return bs4.BeautifulSoup(self.text)
    
    @lazy_property
    def movelist(self):
        movelist = re.search(r"pgnString: '(.*)'", self.text).group(1) \
            .replace(r'\n', '') \
            .replace(r'\x2b', '+') \
            .replace(r'.', '. ') \
            .split()
        return movelist        
    
    @lazy_property
    def sans(self):
        '''This returns a list of san moves'''
        # Filter out move numbers and result
        sans = [m for m in self.movelist if re.match(r'^[^\d\*]', m)]
        return sans
    
    @lazy_property
    def result(self):
        return self.movelist[-1]
    
    @lazy_property
    def board(self):
        board = chess.Board()
        for san in self.sans:
            board.push_san(san)
        return board

    @lazy_property
    def leela_board(self):
        board = LeelaBoard()
        for san in self.sans:
            board.push_san(san)
        return board

    @lazy_property
    def pgn_game(self):
        return chess.pgn.Game.from_board(self.board)
        
    @lazy_property
    def pgn(self):
        return str(self.pgn_game)
    
    def get_leela_board_at(self, movenum=1, halfmoves=0):
        '''Get Leela board at given move number (*prior* to move)
        
        get_leela_board_at(12, 0): This will get the board on the 12th move, at white's turn
        get_leela_board_at(12, 1): This will get the board on the 12th move, at black's turn
        get_leela_board_at(halfmoves=3): This will return the 4th position (after 3 half-moves)
        '''
        halfmoves = 2*(movenum-1) + halfmoves
        if halfmoves > len(self.sans):
            raise Exception('Not that many moves in game')
        board = LeelaBoard()
        for idx, san in enumerate(self.sans):
            if idx<halfmoves:
                board.push_san(san)
        return board
    
        
    
        