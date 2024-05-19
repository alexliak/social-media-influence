# algorithms/influence.py

def calculate_influence(member_a, member_b):
    total_engagement_a = member_a.total_engagement()
    if total_engagement_a == 0:
        return 0.0
    influence = (member_a.likes.get(member_b.member_id, 0) + member_a.comments.get(member_b.member_id, 0)) / total_engagement_a * 100
    return round(influence, 2)
