import unittest
import numpy as np
from main import Member, display_all_pairs_data, display_overall_statistics, create_relationship_matrix, create_engagement_matrix
import time

class TestSocialNetwork(unittest.TestCase):

    def measure_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
            return result
        return wrapper

    @measure_time
    def test_single_member(self):
        alice = Member(1, "Alice")
        members = {1: alice}
        relationship_matrix = create_relationship_matrix(members)
        engagement_matrix = create_engagement_matrix(members)
        display_all_pairs_data(members, relationship_matrix, engagement_matrix)
        display_overall_statistics(members)
        
        all_engagement_rates = [member.engagement_rate() for member in members.values()]
        mean_engagement_rate = np.mean(all_engagement_rates)
        std_dev_engagement_rate = np.std(all_engagement_rates)
        
        self.assertEqual(mean_engagement_rate, 0.00)
        self.assertEqual(std_dev_engagement_rate, 0.00)

    @measure_time
    def test_no_interactions(self):
        alice = Member(1, "Alice")
        bob = Member(2, "Bob")
        charlie = Member(3, "Charlie")
        members = {1: alice, 2: bob, 3: charlie}
        relationship_matrix = create_relationship_matrix(members)
        engagement_matrix = create_engagement_matrix(members)
        display_all_pairs_data(members, relationship_matrix, engagement_matrix)
        display_overall_statistics(members)
        
        all_engagement_rates = [member.engagement_rate() for member in members.values()]
        mean_engagement_rate = np.mean(all_engagement_rates)
        std_dev_engagement_rate = np.std(all_engagement_rates)
        
        self.assertEqual(mean_engagement_rate, 0.00)
        self.assertEqual(std_dev_engagement_rate, 0.00)

    @measure_time
    def test_cyclic_follow(self):
        alice = Member(1, "Alice")
        bob = Member(2, "Bob")
        charlie = Member(3, "Charlie")

        alice.follow(bob)
        bob.follow(charlie)
        charlie.follow(alice)

        alice.like(bob, 2)
        alice.comment(bob, 1)
        bob.like(charlie, 2)
        bob.comment(charlie, 1)
        charlie.like(alice, 2)
        charlie.comment(alice, 1)
        bob.follow(alice)
        charlie.follow(bob)

        members = {1: alice, 2: bob, 3: charlie}
        relationship_matrix = create_relationship_matrix(members)
        engagement_matrix = create_engagement_matrix(members)
        display_all_pairs_data(members, relationship_matrix, engagement_matrix)
        display_overall_statistics(members)

        all_engagement_rates = [member.engagement_rate() for member in members.values()]
        mean_engagement_rate = np.mean(all_engagement_rates)
        std_dev_engagement_rate = np.std(all_engagement_rates)
        
        self.assertAlmostEqual(mean_engagement_rate, 200.00, places=2)
        self.assertAlmostEqual(std_dev_engagement_rate, 70.71, places=2)

    @measure_time
    def test_no_path(self):
        alice = Member(1, "Alice")
        bob = Member(2, "Bob")
        charlie = Member(3, "Charlie")

        members = {1: alice, 2: bob, 3: charlie}
        relationship_matrix = create_relationship_matrix(members)
        engagement_matrix = create_engagement_matrix(members)
        display_all_pairs_data(members, relationship_matrix, engagement_matrix)
        display_overall_statistics(members)

        all_engagement_rates = [member.engagement_rate() for member in members.values()]
        mean_engagement_rate = np.mean(all_engagement_rates)
        std_dev_engagement_rate = np.std(all_engagement_rates)
        
        self.assertEqual(mean_engagement_rate, 0.00)
        self.assertEqual(std_dev_engagement_rate, 0.00)

    @measure_time
    def test_high_interaction_varied(self):
        alice = Member(1, "Alice")
        bob = Member(2, "Bob")
        charlie = Member(3, "Charlie")
        dave = Member(4, "Dave")

        alice.follow(bob)
        alice.follow(charlie)
        bob.follow(charlie)
        charlie.follow(dave)
        dave.follow(alice)

        alice.like(bob, 2)
        alice.comment(bob, 1)
        bob.like(charlie, 4)
        bob.comment(charlie, 2)
        charlie.like(dave, 3)
        charlie.comment(dave, 2)
        dave.like(alice, 1)
        dave.comment(alice, 1)

        alice.follow(dave)
        bob.follow(alice)
        bob.follow(dave)
        charlie.follow(alice)
        charlie.like(alice, 2)
        charlie.comment(alice, 1)
        dave.like(bob, 1)
        dave.comment(bob, 1)

        members = {1: alice, 2: bob, 3: charlie, 4: dave}
        relationship_matrix = create_relationship_matrix(members)
        engagement_matrix = create_engagement_matrix(members)
        display_all_pairs_data(members, relationship_matrix, engagement_matrix)
        display_overall_statistics(members)

        all_engagement_rates = [member.engagement_rate() for member in members.values()]
        mean_engagement_rate = np.mean(all_engagement_rates)
        std_dev_engagement_rate = np.std(all_engagement_rates)
        
        self.assertAlmostEqual(mean_engagement_rate, 308.33, places=2)
        self.assertAlmostEqual(std_dev_engagement_rate, 204.63, places=2)

if __name__ == '__main__':
    unittest.main()
