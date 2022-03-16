from src.PostRepository import all_posts
from src.UserPost import UserPost
from src.UserReply import UserReply
# TESTING:
# User creates a post on our website
user_1 = UserPost("I_need_homework_help120", "HOW DO I CODE THIS PROJECT?", "Hey guys, I have no idea what I am doing. I really don't. Please help.", "Math")
# Another user sees the post and then creates a reply. In the back-end it takes user 1's post and attaches it as a reply.
all_posts.add_post(user_1)
user_2 = UserReply("response1","hey just buy chegg",user_1)
user_3 = UserReply("response2","Hi I think you forgot a semi-colon", user_1)
user_4 = UserReply("response3","Hi I think you forgot a semi-colon as well", user_1)
user_5 = UserReply("response4","I agree with @response3 and @repsonse2", user_1)

all_posts.attach_reply(user_1, user_2)
all_posts.attach_reply(user_1, user_3)
all_posts.attach_reply(user_1, user_4)
all_posts.attach_reply(user_1, user_5)

print("================= SAMPLE OUTPUT =================")
for post_id in all_posts.get_all_posts().keys():
    current_post = all_posts.get_all_posts()[post_id]
    print("POST ID NUMBER: " + str(current_post.get_post_id()))
    print("TITLE: " + str(current_post.get_title()))
    print("MAIN TEXT: "+ str(current_post.get_main_text()))
    print("Replies: ")
    for reply in current_post.get_replies():
        print("       Main text: " + str(reply.get_main_text() + " FROM USER: " + str(reply.get_username())))

another_post = UserPost("I_am_bad_at_math", "How do I calculate this derivative?", "Hi, how do I take this integral?", "Math")
derivative_response = UserReply("calculus response","you suck", another_post)
different_response = UserReply("the_god_512", "I think it should be 15.21", another_post)

all_posts.add_post(another_post)
all_posts.attach_reply(another_post, derivative_response)
all_posts.attach_reply(another_post, different_response)

for post_id in all_posts.get_all_posts().keys():
    current_post = all_posts.get_all_posts()[post_id]
    print("POST ID NUMBER: " + str(current_post.get_post_id()))
    print("TITLE: " + str(current_post.get_title()))
    print("MAIN TEXT: "+ str(current_post.get_main_text()))
    print("Replies: ")
    for reply in current_post.get_replies():
        print("       Main text: " + str(reply.get_main_text() + " FROM USER: " + str(reply.get_username())))