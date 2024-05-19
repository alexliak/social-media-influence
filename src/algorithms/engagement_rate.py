# algorithms/engagement_rate.py

def calculate_engagement_rate(member):
    rate = member.engagement_rate()
    print(f"Calculated engagement rate for {member.name}: {rate:.2f}%")
    return rate
