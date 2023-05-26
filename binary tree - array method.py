tree = [''] * 15


def root(key):
    if tree[0] != '':
        print("Tree already had root")
    else:
        tree[0] = key


def set_left(key, parent):
    if tree[parent] == '':
        print("Can't set child at", (parent * 2) + 1, ", no parent found")
    else:
        tree[(parent * 2) + 1] = key


def set_right(key, parent):
    if tree[parent] == '':
        print("Can't set child at", (parent * 2) + 2, ", no parent found")
    else:
        tree[(parent * 2) + 2] = key


def print_tree():
    print(tree)


root('+')
set_left('-', 0)
set_right('x', 0)
set_left('8', 1)
set_right('x', 1)
set_right('y',3)
print_tree()



