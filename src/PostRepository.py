# Inspiration for writing this class was taken from 
# module 8 - flask group assignment.
# I felt it was convienent to have a data structure
# that stores all posts made. It makes it easy to
# display and keep track of all posts.
class PostRepository:
    def __init__(self):
        self.repository_list = dict()
    def add_post(self, user_post):
        self.repository_list[user_post.get_post_id()] = user_post
    def get_all_posts(self):
        return self.repository_list
    def attach_reply(self, main_post, incoming_response):
        main_post.attach_reply(incoming_response)
all_posts = PostRepository()