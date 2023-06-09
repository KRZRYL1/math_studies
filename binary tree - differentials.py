# import collections
from copy import deepcopy


class Tree:
    # ------------------------------- zagnieżdżona klasa Position -------------------------------
    class Position:

        def element(self):
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            return not (self == other)  # opposite of __eq__

    # ---------- abstrakcyjne metody do zdefiniowania w podklasie ----------
    def root(self):
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p):
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p):
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p):
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self):
        raise NotImplementedError('must be implemented by subclass')

    # ---------- konkretne metody ----------
    def is_root(self, p):
        return self.root() == p

    def is_leaf(self, p):
        return self.num_children(p) == 0

    def is_empty(self):
        return len(self) == 0

    def depth(self, p):
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height1(self):  # works, but O(n^2) worst-case time
        return max(self.depth(p) for p in self.positions() if self.is_leaf(p))

    def _height2(self, p):  # time is linear in size of subtree
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height2(c) for c in self.children(p))

    def height(self, p=None):
        if p is None:
            p = self.root()
        return self._height2(p)  # start _height2 recursion

    def __iter__(self):
        for p in self.positions():
            yield p.element()

    def positions(self):
        return self.preorder()  #

    def preorder(self):
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):  #
                yield p

    def _subtree_preorder(self, p):
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def postorder(self):
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):  # start recursion
                yield p

    def _subtree_postorder(self, p):
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p


class BinaryTree(Tree):
    # --------------------- dodatkowe metody abstrakcyjne ---------------------
    def left(self, p):
        raise NotImplementedError('must be implemented by subclass')

    def right(self, p):
        raise NotImplementedError('must be implemented by subclass')

    # ---------- metody konkretne zaimplemetowane w tej klasie ----------
    def sibling(self, p):
        parent = self.parent(p)
        if parent is None:  # p must be the root
            return None  # root has no sibling
        else:
            if p == self.left(parent):
                return self.right(parent)  # possibly None
            else:
                return self.left(parent)  # possibly None

    def children(self, p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def inorder(self):
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        if self.left(p) is not None:  # if left child exists, traverse its subtree
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p  # visit p between its subtrees
        if self.right(p) is not None:  # if right child exists, traverse its subtree
            for other in self._subtree_inorder(self.right(p)):
                yield other

    def positions(self):
        return self.inorder()  # make inorder the default


class LinkedBinaryTree(BinaryTree):
    # -------------------------- zagnieżdżona klasa Node --------------------------
    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    # -------------------------- zagnieżdżona klasa Position --------------------------
    class Position(BinaryTree.Position):

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

    # ------------------------------- metody użytkowe -------------------------------
    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        return self.Position(self, node) if node is not None else None

    # -------------------------- konstruktor drzewa --------------------------
    def __init__(self):
        self._root = None
        self._size = 0

    # -------------------------- metody publiczne --------------------------
    def __len__(self):
        return self._size

    def root(self):
        return self._make_position(self._root)

    def parent(self, p):
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        node = self._validate(p)
        count = 0
        if node._left is not None:  # left child exists
            count += 1
        if node._right is not None:  # right child exists
            count += 1
        return count

    # -------------------------- metody niepubliczne --------------------------
    def _add_root(self, e):
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        node._left = self._Node(e, node)  # node is its parent
        return self._make_position(node._left)

    def _add_right(self, p, e):
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        node._right = self._Node(e, node)  # node is its parent
        return self._make_position(node._right)

    def _replace(self, p, e):
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('Position has two children')
        child = node._left if node._left else node._right  # might be None
        if child is not None:
            child._parent = node._parent  # child's grandparent becomes parent
        if node is self._root:
            self._root = child  # child becomes root
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node  # convention for deprecated node
        return node._element

    def _attach(self, p, t1, t2):
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):  # all 3 trees must be same type
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():  # attached t1 as left subtree of node
            t1._root._parent = node
            node._left = t1._root
            t1._root = None  # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():  # attached t2 as right subtree of node
            t2._root._parent = node
            node._right = t2._root
            t2._root = None  # set t2 instance to empty
            t2._size = 0


class ExpressionTree(LinkedBinaryTree):

    def __init__(self, token, left=None, right=None):
        super().__init__()  # LinkedBinaryTree initialization
        if not isinstance(token, str):
            raise TypeError('Token must be a string')
        self._add_root(token)  # use inherited, nonpublic method
        if left is not None:  # presumably three-parameter form
            if token not in '+-*/^':
                raise ValueError('token must be valid operator')
            self._attach(self.root(), left, right)  # use inherited, nonpublic method

    def __str__(self):
        pieces = []  # sequence of piecewise strings to compose
        self._parenthesize_recur(self.root(), pieces)
        return ''.join(pieces)

    def _parenthesize_recur(self, p, result):
        if self.is_leaf(p):
            result.append(str(p.element()))  # leaf value as a string
        else:
            result.append('(')  # opening parenthesis
            self._parenthesize_recur(self.left(p), result)  # left subtree
            result.append(p.element())  # operator
            self._parenthesize_recur(self.right(p), result)  # right subtree
            result.append(')')  # closing parenthesis

    def evaluate(self):
        return self._evaluate_recur(self.root())

    def derivative(self, symbol='x'):
        return self._r_deriv(self.root(), symbol)

    def deval(self, symbol='x', value=0.0):
        return self._r_deval(self.root(), symbol, value)

    def _r_deval(self, p, symbol, value):
        if self.is_leaf(p):
            return float(p.element()) if p.element() != symbol else value
        else:
            op = p.element()
            left_val = self._r_deval(self.left(p), symbol, value)
            right_val = self._r_deval(self.right(p), symbol, value)
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '/':
                return left_val / right_val
            elif op == '^':
                return left_val ** right_val
            else:
                return left_val * right_val

    def _r_rebuild(self, p):
        if self.is_leaf(p):
            return ExpressionTree(p.element())
        else:
            return ExpressionTree(p.element(), self._r_rebuild(self.left(p)), self._r_rebuild(self.right(p)))

    #Functions defining derivating and simplifying expressions

    def _add_simp(self, L, R):
        if L.root().element().isnumeric() and R.root().element().isnumeric():
            return ExpressionTree(str(float(L.root().element()) + float(R.root().element())))
        elif L.root().element() == '0' or L.root().element() == '0.0':
            return R
        elif R.root().element() == '0' or R.root().element() == '0.0':
            return L
        else:
            return ExpressionTree('+', L, R)

    def _sub_simp(self, L, R):
        if L.root().element().isnumeric() and R.root().element().isnumeric():
            return ExpressionTree(str(float(L.root().element()) - float(R.root().element())))
        elif L.root().element() == '0' or L.root().element() == '0.0':
            return ExpressionTree('*', ExpressionTree('-1'), R)
        elif R.root().element() == '0' or R.root().element() == '0.0':
            return L
        else:
            return ExpressionTree('-', L, R)

    def _mul_simp(self, L, R):
        if L.root().element().isnumeric() and R.root().element().isnumeric():
            return ExpressionTree(str(float(L.root().element()) * float(R.root().element())))
        elif L.root().element() == '0' or L.root().element() == '0.0':
            return ExpressionTree('0')
        elif R.root().element() == '0' or R.root().element() == '0.0':
            return ExpressionTree('0')
        elif L.root().element() == '1' or L.root().element() == '1.0':
            return R
        elif R.root().element() == '1' or R.root().element() == '1.0':
            return L
        else:
            return ExpressionTree('*', L, R)

    def _div_simp(self, L, R):
        if L.root().element().isnumeric() and R.root().element().isnumeric():
            return ExpressionTree(str(float(L.root().element()) / float(R.root().element())))
        elif L == '0' or L == '0.0':
            return ExpressionTree('0')
        elif R.root().element() == '1' or R.root().element() == '1.0':
            return L
        elif R.root().element() == '-1' or R.root().element() == '-1.0':
            return ExpressionTree('*', '-1', L)
        else:
            return ExpressionTree('/', L, R)

    def _pow_simp(self, L, R):
        if L.root().element().isnumeric() and R.root().element().isnumeric():
            return ExpressionTree(str(float(L.root().element()) ** float(R.root().element())))
        elif L.root().element() == '1' or L.root().element() == '1.0':
            return ExpressionTree('1')
        elif (L.root().element() == '0' or L.root().element() == '0.0') and (
                R.root().element() != '0' or R.root().element() == '0.0'):
            return ExpressionTree('0')
        elif (R.root().element() == '0' or R.root().element() == '0.0'):
            return ExpressionTree('1')
        elif (R.root().element() == '1' or R.root().element() == '1.0'):
            return L
        else:
            return ExpressionTree('^', L, R)

    def _r_deriv(self, p, symbol):
        if self.is_leaf(p):
            return ExpressionTree('1' if p.element() == symbol else '0')
        else:
            op = p.element()
            if op == '+':
                L = self._r_deriv(self.left(p), symbol)
                R = self._r_deriv(self.right(p), symbol)
                return self._add_simp(L, R)

            if op == '-':
                L = self._r_deriv(self.left(p), symbol)
                R = self._r_deriv(self.right(p), symbol)
                return self._sub_simp(L, R)

            if op == '*':
                LL = self._r_deriv(self.left(p), symbol)
                LR = self._r_rebuild(self.right(p))

                L = self._mul_simp(LL, LR)

                RL = self._r_rebuild(self.left(p))
                RR = self._r_deriv(self.right(p), symbol)

                R = self._mul_simp(RL, RR)

                return self._add_simp(L, R)

            if op == '/':
                LL = self._r_deriv(self.left(p), symbol)
                LR = self._r_rebuild(self.right(p))

                L = self._mul_simp(LL, LR)

                RL = self._r_rebuild(self.left(p))
                RR = self._r_deriv(self.right(p), symbol)

                R = self._mul_simp(RL, RR)

                U = self._sub_simp(L, R)

                DL = self._r_rebuild(self.right(p))

                D = self._pow_simp(DL, ExpressionTree('2'))

                return self._div_simp(U, D)

            if op == '^':
                n = self._r_rebuild(self.right(p))
                n_1L = deepcopy(n)
                n_1 = self._sub_simp(n_1L, ExpressionTree('1'))

                LP = self._pow_simp(self._r_rebuild(self.left(p)), n_1)

                L = self._mul_simp(n, LP)

                P = self._r_deriv(self.left(p), symbol)

                return self._mul_simp(L, P)

    def _evaluate_recur(self, p):
        if self.is_leaf(p):
            return float(p.element())  # we assume element is numeric
        else:
            op = p.element()
            left_val = self._evaluate_recur(self.left(p))
            right_val = self._evaluate_recur(self.right(p))
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '/':
                return left_val / right_val
            elif op == '^':
                return left_val ** right_val
            else:  # treat '*' as multiplication
                return left_val * right_val


def tokenize(raw):
    SYMBOLS = set('+-*/()^ ')

    mark = 0
    tokens = []
    n = len(raw)
    for j in range(n):
        if raw[j] in SYMBOLS:
            if mark != j:
                tokens.append(raw[mark:j])  # complete preceding token
            if raw[j] != ' ':
                tokens.append(raw[j])  # include this token
            mark = j + 1  # update mark to being at next index
    if mark != n:
        tokens.append(raw[mark:n])  # complete preceding token
    return tokens


def build_expression_tree(input_str):
    tokens = tokenize(input_str)
    S = []  # we use Python list as stack
    for t in tokens:
        # print(' , '.join([str(i) for i in S]))
        # print(type(t))
        if t in '+-*/^':  # t is an operator symbol
            S.append(t)  # push the operator symbol
        elif t not in '()':  # consider t to be a literal
            S.append(ExpressionTree(t))  # push trivial tree storing value
        elif t == ')':  # compose a new tree from three constituent parts
            right = S.pop()  # right subtree as per LIFO
            op = S.pop()  # operator symbol
            left = S.pop()  # left subtree
            # print(*(type(i) for i in (right,op,left)))
            S.append(ExpressionTree(op, left, right))  # repush tree
        # we ignore a left parenthesis
    return S.pop()


if __name__ == "__main__":
    expr = build_expression_tree('(((x+2)*(2*z))/2)')
    print('Expression: ', expr)
    dexp = expr.derivative(symbol='z')
    print('Derivative: ', dexp)
    x = 3
    print('Evaluation of derivative for x=' + str(x) + ':', dexp.deval('x', x))
