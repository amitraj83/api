import praw
from praw.models import InlineGif, InlineImage, InlineVideo

reddit = praw.Reddit(
    client_id="utcpaWWt5u9GFg",
    client_secret="OT3bMDBS0O_nnZ_4NCzcOhczgTUOIg",
    password="D15@Glaway",
    user_agent="SuggestRank by u/suggestrank",
    username="suggestrank",
)

print(reddit.user.me())

# reddit.subreddit("u_suggestrank").submit("bmw x1 vs x3 - which one is better family car?", selftext="Its very difficult to decide which one is better. Anyone came across the similar situation?")

# Posting with image
# reddit.subreddit("u_suggestrank").submit_image("Which Ferrari is this one?", image_path="image_20210417_212517.jpg")

for submission in  reddit.subreddit("carporn").hot(limit=5):

    # submission.reply("Nice car")
    # if submission.title == "Nissan Silvia S15.":
    #     print(submission.comments)
        # submission.reply("This is a nice car. Love it.")
        #submission.comments._comments[0]
        # print("replied")
    print(submission.title)


# reddit.subreddit("suggestrank").submit("Lamborghini Murcielago vs Ford Laser - Which one is better", selftext="Any one know why Lamborghini Murcielago is better than Ford Laser?")
print("Done")