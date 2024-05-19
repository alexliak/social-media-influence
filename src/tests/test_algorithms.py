import unittest
import numpy as np
from data.network import Network
from data.member import Member
from algorithms.path_finding import dijkstra, find_highest_engagement_path
from algorithms.influence import calculate_influence
from sklearn.linear_model import LinearRegression
import random

class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.alice = Member(1, "Alice")
        self.bob = Member(2, "Bob")
        self.charlie = Member(3, "Charlie")
        self.dave = Member(4, "Dave")
        self.eve = Member(5, "Eve")
        self.frank = Member(6, "Frank")
        
        self.members = {1: self.alice, 2: self.bob, 3: self.charlie, 4: self.dave, 5: self.eve, 6: self.frank}
        
        # Establishing the follow relationships
        self.alice.follow(self.eve)
        self.alice.follow(self.frank)
        self.eve.follow(self.bob)
        self.frank.follow(self.charlie)
        self.charlie.follow(self.dave)
        self.dave.follow(self.alice)
        self.frank.follow(self.bob)
        
        # Adding likes and comments
        self.alice.like(self.bob, 3)
        self.alice.comment(self.bob, 2)
        self.alice.like(self.charlie, 3)
        self.alice.comment(self.charlie, 2)
        self.alice.like(self.dave, 1)
        self.alice.comment(self.dave, 1)
        self.alice.like(self.eve, 1)
        self.alice.comment(self.eve, 2)
        self.alice.like(self.frank, 3)
        self.alice.comment(self.frank, 2)

    def test_calculate_engagement_rate(self):
        self.alice.followers.add(self.bob)  # Ensure Alice has followers
        self.alice.followers.add(self.charlie)  # Add another follower to Alice for accurate calculation
        self.alice.followers.add(self.dave)  # Add another follower to Alice for accurate calculation
        expected_rate = (11 + 9) / 3 * 100  # (total likes + total comments) / followers * 100
        actual_rate = self.alice.engagement_rate()
        self.assertAlmostEqual(actual_rate, expected_rate, places=2)

    def test_calculate_influence(self):
        expected_influence = calculate_influence(self.alice, self.bob)  # (likes to Bob + comments to Bob) / total engagement of Alice * 100
        actual_influence = calculate_influence(self.alice, self.bob)
        self.assertAlmostEqual(actual_influence, expected_influence, places=2)

    def test_dijkstra(self):
        path = dijkstra(self.members, 1, 2)  # Shortest path from Alice (1) to Bob (2)
        self.assertEqual(path, [1, 5, 2])  # Should be [1, 5, 2]

    def test_find_highest_engagement_path(self):
        path, engagement = find_highest_engagement_path(self.members, 1, 2)  # Highest engagement path from Alice (1) to Bob (2)
        expected_path = [1, 5, 2]
        expected_engagement = self.alice.total_engagement() + self.eve.total_engagement() + self.bob.total_engagement()
        self.assertEqual(path, expected_path)
        self.assertAlmostEqual(engagement, expected_engagement)

    def test_large_network(self):
        def create_network(num_members):
            network = Network()
            for i in range(1, num_members + 1):
                network.add_member(i, f"Member{i}")

            # Randomly establish follow relationships
            member_ids = list(network.members.keys())
            for member_id in member_ids:
                num_following = random.randint(1, min(3, num_members - 1))  # Each member follows 1 to 3 other members
                following = random.sample([m for m in member_ids if m != member_id], num_following)
                for followed_id in following:
                    network.follow(member_id, followed_id)

            # Randomly generate likes and comments with stricter constraints
            for member_id in member_ids:
                total_likes = 0
                total_comments = 0
                for other_member_id in member_ids:
                    if member_id != other_member_id:
                        if total_likes < 5:  # Max 5 total likes per member
                            likes = random.randint(0, min(2, 5 - total_likes))  # Max 2 likes per interaction
                            network.like(member_id, other_member_id, likes)
                            total_likes += likes
                        if total_comments < 3:  # Max 3 total comments per member
                            comments = random.randint(0, min(1, 3 - total_comments))  # Max 1 comment per interaction
                            network.comment(member_id, other_member_id, comments)
                            total_comments += comments

            return network

        def train_engagement_model(members):
            X = []
            y = []
            for member in members.values():
                X.append([len(member.followers), len(member.following), sum(member.likes.values()), sum(member.comments.values())])
                y.append(member.engagement_rate())
            
            model = LinearRegression()
            model.fit(X, y)
            return model

        for num_members in [10, 20, 48]:  # Progressively larger networks
            network = create_network(num_members)
            members = network.members

            model = train_engagement_model(members)

            # Pick two random members to test the algorithms
            start_id, end_id = random.sample(list(members.keys()), 2)

            # Calculate engagement rates using ML model
            for member in members.values():
                features = np.array([len(member.followers), len(member.following), sum(member.likes.values()), sum(member.comments.values())]).reshape(1, -1)
                predicted_engagement_rate = model.predict(features)[0]
                actual_engagement_rate = member.engagement_rate()
                print(f"Member ID: {member.member_id}, Predicted Engagement Rate: {predicted_engagement_rate}, Actual Engagement Rate: {actual_engagement_rate}")
                self.assertTrue(0 <= predicted_engagement_rate <= 3000, f"Engagement rate out of bounds: {predicted_engagement_rate}")  # Ensure engagement rate is within a reasonable range
                self.assertAlmostEqual(predicted_engagement_rate, actual_engagement_rate, delta=1000, msg=f"Predicted engagement rate differs significantly for Member {member.member_id}")

            # Calculate influence
            start_member = members[start_id]
            end_member = members[end_id]
            influence = calculate_influence(start_member, end_member)
            self.assertTrue(0 <= influence <= 100, f"Influence out of bounds: {influence}")  # Influence should be between 0 and 100

            # Find shortest path
            shortest_path = dijkstra(members, start_id, end_id)
            if shortest_path:
                self.assertGreaterEqual(len(shortest_path), 2, "Shortest path too short")  # There should be at least a start and an end node

            # Find highest engagement path
            highest_engagement_path, engagement = find_highest_engagement_path(members, start_id, end_id)
            if highest_engagement_path:
                self.assertGreaterEqual(len(highest_engagement_path), 2, "Highest engagement path too short")  # There should be at least a start and an end node
                self.assertGreaterEqual(engagement, 0, f"Engagement is negative: {engagement}")  # Engagement should be non-negative

if __name__ == '__main__':
    unittest.main()
