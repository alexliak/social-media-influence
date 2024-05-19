import csv
import time
import numpy as np
from collections import defaultdict, deque
from sklearn.linear_model import LinearRegression
import random

class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.followers = set()
        self.following = set()
        self.likes = defaultdict(int)
        self.comments = defaultdict(int)
        self.likes_to = defaultdict(int)
        self.comments_to = defaultdict(int)

    def follow(self, other):
        self.following.add(other)
        other.followers.add(self)

    def like(self, other, count=1):
        self.likes[other.member_id] += count
        self.likes_to[other.member_id] += count

    def comment(self, other, count=1):
        self.comments[other.member_id] += count
        self.comments_to[other.member_id] += count

    def engagement_rate(self):
        followers_count = len(self.followers)
        if followers_count == 0:
            return 0.0
        total_likes = sum(self.likes.values())
        total_comments = sum(self.comments.values())
        return (total_likes + total_comments) / followers_count * 100

    def total_engagement(self):
        return sum(self.likes.values()) + sum(self.comments.values())

    def influence_on(self, other):
        total_engagement = self.total_engagement()
        if total_engagement == 0:
            return 0.0
        return (self.likes_to[other.member_id] + self.comments_to[other.member_id]) / total_engagement * 100

    def shortest_path_to(self, other, members):
        if self == other:
            return [self.member_id], []

        visited = set()
        queue = deque([(self, [self.member_id])])
        bfs_matrix = []

        while queue:
            current, path = queue.popleft()
            bfs_matrix.append([n.member_id for n, _ in queue] + [current.member_id])
            if current in visited:
                continue
            visited.add(current)
            for neighbor in current.following:
                if neighbor == other:
                    bfs_matrix.append([neighbor.member_id])
                    return path + [neighbor.member_id], bfs_matrix
                queue.append((neighbor, path + [neighbor.member_id]))
        return [], bfs_matrix

    def highest_engagement_path_to(self, other, members):
        dfs_matrix = []

        def dfs(current, target, path, visited, engagement):
            dfs_matrix.append(current.member_id)
            if current == target:
                return path, engagement
            max_path, max_engagement = [], 0
            for neighbor in current.following:
                if neighbor not in visited:
                    new_engagement = engagement + current.total_engagement()
                    new_path, new_engagement = dfs(neighbor, target, path + [neighbor.member_id], visited | {neighbor}, new_engagement)
                    if new_engagement > max_engagement:
                        max_path, max_engagement = new_path, new_engagement
            return max_path, max_engagement

        path, engagement = dfs(self, other, [self.member_id], {self}, 0)
        return path, engagement, dfs_matrix


class Network:
    def __init__(self):
        self.members = {}

    def add_member(self, member_id, name):
        self.members[member_id] = Member(member_id, name)

    def follow(self, follower_id, followee_id):
        self.members[follower_id].follow(self.members[followee_id])

    def like(self, liker_id, likee_id, count=1):
        self.members[liker_id].like(self.members[likee_id], count)

    def comment(self, commenter_id, commentee_id, count=1):
        self.members[commenter_id].comment(self.members[commentee_id], count)


def display_all_pairs_data(members, relationship_matrix, engagement_matrix):
    summary_data = {
        'engagement_rates': {},
        'influences': defaultdict(dict),
        'shortest_paths': defaultdict(dict),
        'engagement_paths': defaultdict(dict)
    }
    
    for member in members.values():
        total_likes = sum(member.likes.values())
        total_comments = sum(member.comments.values())
        followers_count = len(member.followers)
        if followers_count > 0:
            engagement_rate = (total_likes + total_comments) / followers_count * 100
        else:
            engagement_rate = 0
        summary_data['engagement_rates'][member.member_id] = engagement_rate

        for other in members.values():
            if member != other:
                likes_to_other = member.likes_to[other.member_id]
                comments_to_other = member.comments_to[other.member_id]
                total_engagement = member.total_engagement()
                if total_engagement > 0:
                    influence = (likes_to_other + comments_to_other) / total_engagement * 100
                else:
                    influence = 0
                summary_data['influences'][member.member_id][other.member_id] = influence

                start_time = time.time()
                shortest_path, bfs_matrix = member.shortest_path_to(other, members)
                end_time = time.time()
                shortest_path_time = end_time - start_time

                start_time = time.time()
                highest_engagement_path, engagement, dfs_matrix = member.highest_engagement_path_to(other, members)
                end_time = time.time()
                highest_engagement_path_time = end_time - start_time

                if shortest_path:
                    summary_data['shortest_paths'][member.member_id][other.member_id] = (shortest_path, shortest_path_time, bfs_matrix)
                else:
                    summary_data['shortest_paths'][member.member_id][other.member_id] = ([], 0, [])

                if highest_engagement_path:
                    summary_data['engagement_paths'][member.member_id][other.member_id] = (highest_engagement_path, engagement, dfs_matrix)
                else:
                    summary_data['engagement_paths'][member.member_id][other.member_id] = ([], 0, [])

    return summary_data


def display_overall_statistics(members):
    total_comments = sum(sum(member.comments.values()) for member in members.values())
    total_likes = sum(sum(member.likes.values()) for member in members.values())
    total_following = sum(len(member.followers) for member in members.values())
    total_members = len(members)
    all_engagement_rates = [member.engagement_rate() for member in members.values()]
    mean_engagement_rate = np.mean(all_engagement_rates) if all_engagement_rates else 0
    std_dev_engagement_rate = np.std(all_engagement_rates) if all_engagement_rates else 0

    # Calculate coefficient and R-squared value
    engagement_rates = np.array(all_engagement_rates).reshape(-1, 1)
    followers_counts = np.array([len(member.followers) for member in members.values()]).reshape(-1, 1)
    
    if total_members > 1:
        model = LinearRegression().fit(followers_counts, engagement_rates)
        coefficient = model.coef_[0][0]
        r_squared = model.score(followers_counts, engagement_rates)
    else:
        coefficient = None
        r_squared = None

    overall_stats = {
        "Total comments": total_comments,
        "Total likes": total_likes,
        "Total following": total_following,
        "Total members": total_members,
        "Mean engagement rate": round(mean_engagement_rate, 2),
        "Standard deviation of engagement rates": round(std_dev_engagement_rate, 2),
        "Engagement rate vs Followers regression coefficient": round(coefficient, 2) if coefficient is not None else None,
        "R-squared value": round(r_squared, 2) if r_squared is not None else None
    }

    return overall_stats


def create_relationship_matrix(members):
    size = len(members)
    matrix = np.zeros((size, size), dtype=int)
    for member in members.values():
        for followed in member.following:
            matrix[member.member_id - 1][followed.member_id - 1] = 1
    return matrix

def create_engagement_matrix(members):
    size = len(members)
    matrix = np.zeros((size, size), dtype=int)
    for member in members.values():
        for other_id, likes in member.likes.items():
            matrix[member.member_id - 1][other_id - 1] += likes
        for other_id, comments in member.comments.items():
            matrix[member.member_id - 1][other_id - 1] += comments
    return matrix

def format_percentage(value):
    if value < 10:
        return f"{value:.1f}%"
    elif value < 100:
        return f"{value:.2f}%"
    else:
        return f"{value:.2f}%"


def save_to_csv(overall_stats, summary_data, members):
    with open('network_summary.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Overall Statistics
        writer.writerow(["Overall Statistics"])
        for key, value in overall_stats.items():
            writer.writerow([key, value])
        
        writer.writerow([])  # Empty row for separation
        
        # Engagement Rates
        writer.writerow(["Engagement Rates"])
        for member_id, rate in summary_data['engagement_rates'].items():
            writer.writerow([f"Member {member_id}", f"{rate:.2f}%"])
        
        writer.writerow([])  # Empty row for separation
        
        # Influences
        writer.writerow(["Influences"])
        for member_id, influences in summary_data['influences'].items():
            for other_id, influence in influences.items():
                writer.writerow([f"Influence of Member {member_id} on Member {other_id}", f"{influence:.2f}%"])
        
        writer.writerow([])  # Empty row for separation
        
        # Shortest Paths
        writer.writerow(["Shortest Paths"])
        for member_id, paths in summary_data['shortest_paths'].items():
            for other_id, (path, shortest_path_time, bfs_matrix) in paths.items():
                writer.writerow([f"Shortest path from Member {member_id} to Member {other_id}", path])
                writer.writerow([f"BFS Matrix", bfs_matrix])
        
        writer.writerow([])  # Empty row for separation
        
        # Highest Engagement Paths
        writer.writerow(["Highest Engagement Paths"])
        for member_id, paths in summary_data['engagement_paths'].items():
            for other_id, (path, engagement, dfs_matrix) in paths.items():
                writer.writerow([f"Highest engagement path from Member {member_id} to Member {other_id}", path, f"{engagement:.2f}%"])
                writer.writerow([f"DFS Matrix", dfs_matrix])

def main():
    start_time = time.time()
    
    network = Network()
    
    # Adding members
    for i in range(1, 10):
        network.add_member(i, f"Member{i}")
    
    members = network.members

    # Establishing follow relationships randomly
    member_ids = list(members.keys())
    for member_id in member_ids:
        num_following = random.randint(1, min(5, len(member_ids) - 1))  # Increase the number of possible followings
        following = random.sample([m for m in member_ids if m != member_id], num_following)
        for followee_id in following:
            network.follow(member_id, followee_id)

    # Adding likes and comments randomly with more engagement
    for member_id in member_ids:
        for other_member_id in member_ids:
            if member_id != other_member_id:
                likes = random.randint(0, 5)  # Increase range for likes
                comments = random.randint(0, 3)  # Increase range for comments
                network.like(member_id, other_member_id, likes)
                network.comment(member_id, other_member_id, comments)
    
    relationship_matrix = create_relationship_matrix(members)
    engagement_matrix = create_engagement_matrix(members)

    summary_data = display_all_pairs_data(members, relationship_matrix, engagement_matrix)
    overall_stats = display_overall_statistics(members)

    save_to_csv(overall_stats, summary_data, members)
    
    end_time = time.time()
    total_execution_time = end_time - start_time
    minutes, seconds = divmod(total_execution_time, 60)
    print(f"\nTotal execution time: {int(minutes)} minutes {seconds:.4f} seconds")

if __name__ == '__main__':
    main()































































































