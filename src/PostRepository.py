# Inspiration for writing this class was taken from 
# module 8 - flask group assignment.
# I felt it was convienent to have a data structure
# that stores all posts made. It makes it easy to
# display and keep track of all posts.
class PostRepository:
    # repository_list is just the list that maintains all UserPost objects created.
    def __init__(self):
        self.repository_list = []
    def add_post(self, user_post):
        self.repository_list.append(user_post)
    def get_all_posts(self):
        return self.repository_list
# Work with all_data variable to keep track of 1 database.
all_data = PostRepository()