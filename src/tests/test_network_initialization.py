import unittest
from data.network import Network

class TestNetworkInitialization(unittest.TestCase):

    def test_add_member(self):
        network = Network()
        network.add_member(1, "Alice")
        self.assertIn(1, network.members)
        self.assertEqual(network.members[1].name, "Alice")

    def test_follow_member(self):
        network = Network()
        network.add_member(1, "Alice")
        network.add_member(2, "Bob")
        network.follow(1, 2)
        self.assertIn(network.members[2], network.members[1].following)
        self.assertIn(network.members[1], network.members[2].followers)

    def test_like_member(self):
        network = Network()
        network.add_member(1, "Alice")
        network.add_member(2, "Bob")
        network.like(1, 2, 5)
        self.assertEqual(network.members[1].likes[2], 5)

    def test_comment_member(self):
        network = Network()
        network.add_member(1, "Alice")
        network.add_member(2, "Bob")
        network.comment(1, 2, 3)
        self.assertEqual(network.members[1].comments[2], 3)

if __name__ == '__main__':
    unittest.main()
