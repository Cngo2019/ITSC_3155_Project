class UserReply:
    # user_name (string) - sames concept in the UserPost class
    # main_text (string) - same concept as in the UserPost class
    # main_user_post (UserPost) - when creating a reply, there MUST be a main post associated with it. This stores the main post we are on.
    # Right now, a UserReply can not have sub-replies (to keep our logic simple for now but that can change over time)
    def __init__(self, user_name, main_text, main_user_post):
        self.user_name = user_name
        self.main_text = main_text
        self.main_user_post = main_user_post