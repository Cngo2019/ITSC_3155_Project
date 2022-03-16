from uuid import uuid4
class UserPost:
    # user_name (string) - the poster's username
    # title (string) - the title of the post
    # post_body (string) - the body of the text itself
    # replies - the replies associated with the post itself (an array of UserReply).
    # subject - the subject of the homework post (computer science, math, english, etc.)
    def __init__(self, username, title, main_text, subject):
        self.subject = subject
        self.username = username
        self.title = title
        self.main_text = main_text
        self.replies = []
        self.id_number = str(uuid4())

    def attach_reply(self, user_reply):
        self.replies.append(user_reply)

    def get_replies(self):
        return self.replies

    def get_main_text(self):
        return self.main_text

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_user_name(self):
        return self.username
        
    def get_post_id(self):
        return self.id_number