import unittest
import unittest
import random

from avl import SearchTree


def equal(o):
    return o[0] == o[1]


class TestAVL(unittest.TestCase):
    def test_empty_tree(self):
        tree = SearchTree()
        self.assertEqual(tree.is_empty(), True)
        self.assertEqual(tree.nodes, [])
        self.assertEqual(tree.root, None)

    def test_insert_node(self):
        tree = SearchTree()
        v = [20, 11, 25, 12, 8]
        for value in v:
            tree.insert(value)
            # the tree should always be balanced
            for node_index in xrange(0, len(tree.nodes)):
                self.assertTrue(tree.is_balanced(node_index))

        self.assertEqual(tree.is_empty(), False)
        self.assertEqual(tree.root, 0)  # the root is 20
        for index, value in enumerate(v):
            self.assertEqual(tree.nodes[index].value, value)
            self.assertTrue(tree.contains(value))

        v.sort()
        self.assertTrue(all(map(equal, zip(list(tree.iter()), v))))
        tree.insert(7)
        self.assertEqual(tree.nodes[4].height, 1)

    def test_random_values(self):
        v = []
        for _ in xrange(0, 1000):
            v.append(random.randint(0, 10000000))

        print '....'
        tree = SearchTree()
        for value in v:
            tree.insert(value)
            # the tree should always be balanced
            for node_index in xrange(0, len(tree.nodes)):
                self.assertTrue(tree.is_balanced(node_index))

        v = sorted(list(set(v)))
        self.assertTrue(all(map(equal, zip(list(tree.iter()), v))))


unittest.TextTestRunner(verbosity=10).run(
    unittest.TestLoader().loadTestsFromTestCase(TestAVL)
)
