# data/network.py

from data.member import Member

class Network:
    def __init__(self):
        self.members = {}

    def add_member(self, member_id, member_name):
        self.members[member_id] = Member(member_id, member_name)

    def follow(self, follower_id, followee_id):
        self.members[follower_id].follow(self.members[followee_id])

    def like(self, liker_id, likee_id, count):
        self.members[liker_id].like(self.members[likee_id], count)

    def comment(self, commenter_id, commente_id, count):
        self.members[commenter_id].comment(self.members[commente_id], count)

    def get_member(self, member_id):
        return self.members.get(member_id)

