# coding=utf-8

import tone

from .node import Node

from . import MOVE_STATE_FULL
from . import MOVE_STATE_WIN
from . import MOVE_STATE_NONE
from . import CHESS_BLACK
from . import CHESS_WHITE


logger = tone.utils.get_logger()


class Game(object):

    def __init__(self):
        self.root = None
        self.reset()

    def move(self, where=None):
        if self.head.is_finished():
            return MOVE_STATE_WIN

        if where:
            node = self.head.move(where)
        else:
            node = self.head.next_move()
        if not isinstance(node, Node):
            return node

        # logger.debug("{:0.2f} - {}".format(node.score.score, node.score.finished))

        self.head = node
        if self.head.is_finished():
            return MOVE_STATE_WIN

    def reset(self):
        from .minmax import MinMaxNode as Node

        self.depth = 1
        self.span = 1
        self.top = 1000
        self.root = Node(
            depth=self.depth,
            span=self.span,
            top=self.top)
        self.head = self.root

    def undo(self):
        if self.head == self.root:
            return None
        if self.head.parent:
            self.head = self.head.parent
        if self.head.parent:
            self.head = self.head.parent

    def save(self, filename):
        from . import functions
        functions.save_pickle(self, filename)

    def load(self, filename):
        from . import functions
        model = functions.load_pickle(filename)
        if not isinstance(model, Game):
            return False

        self.root = model.root
        self.head = model.head

        return True
