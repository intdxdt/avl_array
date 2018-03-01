class Node(object):
    def __init__(self, value=None, parent=None, left_child=None, right_child=None, height=0):
        """
        A node inside a `SearchTree`.
        """
        self.value = value,
        self.parent = parent,
        self.left_child = left_child,
        self.right_child = right_child,
        self.height = height,


class SearchTree(object):
    def __init__(self):
        """
        A simple AVL tree.
        """
        self.nodes = []
        self.root = None

    def is_empty(self):
        """Test if this tree is empty."""
        return self.root is None

    def contains(self, value):
        index = self.get_node(value)
        if index is None:
            return False
        return self.nodes[index].value == value

    def insert(self, value):
        node = self.create_node(value)
        if node is not None:
            self.nodes.append(node)
            # inserted the root
            if len(self.nodes) == 1:
                self.root = 0
            last_added = len(self.nodes) - 1
            self.update_heights(last_added)
            index = last_added
            while index is not None:
                if not self.is_balanced(index):
                    self.rebalance(index)
                index = self.nodes[index].parent

    def get_node(self, value):
        current_index = self.root
        previous_index = None
        index = current_index
        while index is not None:
            previous_index = current_index
            if value > self.nodes[index].value:
                current_index = self.nodes[index].right_child
            elif value < self.nodes[index].value:
                current_index = self.nodes[index].left_child
            else:
                # the value already exists in the tree - return the index of
                # the corresponding node
                return current_index

            index = current_index

        # return the index of the node containing the smallest value
        # greater than `value`
        return previous_index

    def create_node(self, value):
        parent = self.get_node(value)
        if parent is not None:
            index = parent
            if self.nodes[index].value == value:
                return None  # no need to create the node
            else:
                if self.nodes[index].value < value:
                    self.nodes[index].right_child = len(self.nodes)
                else:
                    self.nodes[index].left_child = len(self.nodes)

        return Node(
            value=value,
            parent=parent,
            left_child=None,
            right_child=None,
            height=0
        )

    def update_heights(self, start_index):
        if not self.nodes.is_empty():
            child_index = start_index
            while self.nodes[child_index].parent is not None:
                ancestor_index = self.nodes[child_index].parent
                self.nodes[ancestor_index].height = self.compute_height(
                    self.nodes[ancestor_index].left_child,
                    self.nodes[ancestor_index].right_child
                )
                child_index = ancestor_index

            # update the height of the root
            self.nodes[self.root].height = self.compute_height(
                self.nodes[self.root].left_child,
                self.nodes[self.root].right_child
            )

    def compute_height(self, l_subtree, r_subtree):
        left_height, right_height = (0, 0)
        if l_subtree is not None:
            index = l_subtree
            left_height = self.nodes[index].height + 1

        if r_subtree is not None:
            index = r_subtree
            right_height = self.nodes[index].height + 1

        return max(left_height, right_height)

    def balance_factor(self, node):
        left_height, right_height = (-1, -1)
        if node.left_child is not None:
            left_child = node.left_child
            left_height = self.nodes[left_child].height

        if node.right_child is not None:
            right_child = node.right_child
            right_height = self.nodes[right_child].height

        return left_height - right_height

    def left_rotation(self, index):
        if self.nodes[index].right_child is not None:
            right_index = self.nodes[index].right_child
            # The right child of `index` becomes the parent of `index`.
            # Therefore, `index` must become the left child of `right_index`
            # (its value is lower than that of `right_index`). If `index`
            # becomes the left child of `right_index`, that means the 'old'
            # left child of `right_index` must become the new right child of
            # `index`.
            #
            #       A (index)          (right_index) B
            #     /  \            =>               /  \
            #    X    B (right_index)     (index) A    C
            #       /  \                        /  \
            #      Y    C                      X   Y
            self.nodes[index].right_child = self.nodes[right_index].left_child
            # If the right child of `index` is None, that means the old right
            # child of index did not have a left subtree.
            if self.nodes[index].right_child is not None:
                new_right_index = self.nodes[index].right_child
                self.nodes[new_right_index].parent = index

            self.nodes[right_index].left_child = index
            parent = self.nodes[index].parent
            if parent is not None:
                parent_index = parent
                if self.nodes[parent_index].left_child == index:
                    self.nodes[parent_index].left_child = right_index
                else:
                    self.nodes[parent_index].right_child = right_index

            else:
                # change the root
                self.root = right_index

            self.nodes[index].height = self.compute_height(
                self.nodes[index].left_child,
                self.nodes[index].right_child
            )
            self.nodes[right_index].height = self.compute_height(
                self.nodes[right_index].left_child,
                self.nodes[right_index].right_child
            )
            self.nodes[right_index].parent = self.nodes[index].parent
            self.nodes[index].parent = right_index
            self.update_heights(index)

    def right_rotation(self, index):
        if self.nodes[index].left_child is not None:
            left_index = self.nodes[index].left_child
            # See the comments for `left_rotation` (this is a mirrored
            # implementation of `left_rotation`)
            #
            #         (index)  A                  B (left_index)
            #                /  \       =>      /  \
            # (left_index)  B    X             C     A (index)
            #             /  \                     /  \
            #            C   Y                    Y   X
            self.nodes[index].left_child = self.nodes[left_index].right_child
            if self.nodes[index].left_child is not None:
                new_left_index = self.nodes[index].left_child
                self.nodes[new_left_index].parent = index

            self.nodes[left_index].right_child = index
            parent = self.nodes[index].parent
            if parent is not None:
                parent_index = parent
                if self.nodes[parent_index].left_child == index:
                    self.nodes[parent_index].left_child = left_index
                else:
                    self.nodes[parent_index].right_child = left_index
            else:
                # change the root
                self.root = left_index

            self.nodes[index].height = self.compute_height(
                self.nodes[index].left_child,
                self.nodes[index].right_child
            )
            self.nodes[left_index].height = self.compute_height(
                self.nodes[left_index].left_child,
                self.nodes[left_index].right_child
            )
            self.nodes[left_index].parent = self.nodes[index].parent
            self.nodes[index].parent = left_index
            self.update_heights(index)

    def right_left_rotation(self, index):
        if self.nodes[index].right_child is not None:
            right_index = self.nodes[index].right_child
            self.right_rotation(right_index)
            self.left_rotation(index)

    def left_right_rotation(self, index):
        if self.nodes[index].left_child is not None:
            left_index = self.nodes[index].left_child
            self.left_rotation(left_index)
            self.right_rotation(index)

    def rebalance(self, index):
        balance_factor = self.balance_factor(self.nodes[index])
        if balance_factor == -2:
            # right-heavy tree
            right_index = self.nodes[index].right_child
            if self.balance_factor(self.nodes[right_index]) == -1:
                self.left_rotation(index)
            else:
                self.right_left_rotation(index)

        elif balance_factor == 2:
            # left-heavy
            left_index = self.nodes[index].left_child
            if self.balance_factor(self.nodes[left_index]) == 1:
                self.right_rotation(index)
            else:
                self.left_right_rotation(index)

        elif balance_factor < -2 or balance_factor > 2:
            # this should not happen - the tree is normally rebalanced
            # whenever the balance factor of one of its nodes becomes -2 or 2
            raise Exception("Invalid balance factor for {}: {}".format(index, balance_factor))

    def is_balanced(self, index):
        return abs(self.balance_factor(self.nodes[index])) < 2


class SearchTreeIter(object):
    def __init__(self, nodes, root):
        self.nodes = nodes
        self.current_node = self.get_leftmost(nodes, root)

    @staticmethod
    def get_leftmost(nodes, root):
        """Return the index of the leftmost node of the subtree rooted at `root`."""
        if root is not None:
            leftmost_node = root
            while nodes[leftmost_node].left_child is not None:
                leftmost_node = nodes[leftmost_node].left_child
            return leftmost_node
        return None

    def __iter__(self):
        return self

    def next(self):
        if self.current_node is None:
            raise StopIteration()

        node_index = self.current_node
        node = self.nodes[node_index]
        result = node.value
        if node.right_child is not None:
            # find the lowest value in the right subtree of `node`, so
            # `self.current_node` becomes the node containing the
            # lowest value greater than the value inside `node`
            self.current_node = SearchTreeIter.get_leftmost(
                self.nodes,
                node.right_child
            )
        else:
            # find the first ancestor which holds a value greater
            # than the one stored by `self.current_node`
            while node.parent is not None and self.nodes[node.parent].value < node.value:
                self.current_node = node.parent
                node = self.nodes[self.current_node]

            self.current_node = node.parent

        return result


if __name__ == '__main__':
    o = [i for i in SearchTreeIter(10)]
    print o
