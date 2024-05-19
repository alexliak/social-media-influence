class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.followers = set()
        self.following = set()
        self.likes = {}
        self.comments = {}

    def follow(self, other):
        self.following.add(other)
        other.followers.add(self)

    def like(self, other, count):
        if other.member_id in self.likes:
            self.likes[other.member_id] += count
        else:
            self.likes[other.member_id] = count

    def comment(self, other, count):
        if other.member_id in self.comments:
            self.comments[other.member_id] += count
        else:
            self.comments[other.member_id] = count

    def total_engagement(self):
        return sum(self.likes.values()) + sum(self.comments.values())

    def engagement_rate(self):
        if len(self.followers) == 0:
            return 0.0
        return round(((self.total_engagement() / len(self.followers)) * 100), 2)

