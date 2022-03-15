from UserReply import UserReply
class UserPost:
    # user_name (string) - the poster's username
    # title (string) - the title of the post
    # post_body (string) - the body of the text itself
    # replies - the replies associated with the post itself (an array of UserReply).
    # subject - the subject of the homework post (computer science, math, english, etc.)

    def __init__(self, user_name, title, main_text, subject):
        self.subject = subject
        self.user_name = user_name
        self.title = title
        self.main_text = main_text
        self.replies = []
    def attach_reply(self, user_reply):
        self.replies.append(user_reply)
# TESTING:
# User creates a post on our website
user_1 = UserPost("I_need_homework_help120", "HOW DO I CODE THIS PROJECT?", "Hey guys, I have no idea what I am doing. I really don't. Please help.", "Math")
# Another user sees the post and then creates a reply. In the back-end it takes user 1's post and attaches it as a reply.
user_2 = UserReply("Stop_cheating_guy_123", "Bro just buy a chegg subscription", user_1)
user_1.attach_reply(user_2)
# Same concept applied to the 2nd responder
user_3 = UserReply("Toxic_Poster", "You suck.", user_1)
user_1.attach_reply(user_3)

print(user_1.main_text)
for reply in user_1.replies:
    print(reply.main_text)
