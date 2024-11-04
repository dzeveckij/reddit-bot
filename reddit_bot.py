import praw
import requests
import time
from mistralai import Mistral
import config

# Initialize Reddit API
print("Initializing Reddit API...")
reddit = praw.Reddit(
    client_id=config.reddit_client_id,
    client_secret=config.reddit_client_secret,
    user_agent=config.reddit_user_agent,
    username=config.reddit_username,
    password=config.reddit_password
)
print("Reddit API initialized.")

client = Mistral(api_key=config.api_key)


def generate_comment(title, description):
    # Generate a comment based on the input title and description using Mistral API
    chat_response = client.chat.complete(
        model= config.model,
        messages = [
            {
                "role": "user",
                "content": (
                "Generate a short comment, that appears to have been commented by a casual reddit user. "
                "Don't use any emojis. Here is the post you are commenting on: " 
                + title + " " + description
            )   , 
            },
        ]
    )
       

    print(chat_response.choices[0].message.content)

    return chat_response.choices[0].message.content


def main():
    subreddits = ['all']  # List of subreddits to scrape
    processed_posts = set()  # Keep track of processed posts

    while True:
        print("Starting new iteration...")
        for subreddit_name in subreddits:
            print(f"Scraping subreddit: {subreddit_name}")
            subreddit = reddit.subreddit(subreddit_name)
            for submission in subreddit.new(limit=10):  # Scrape latest 10 posts
                if submission.id not in processed_posts and not submission.stickied:  # Skip stickied and already processed posts
                    print(f"Processing post: {submission.title}")
                    comment_text = generate_comment(submission.title, submission.selftext)
                    # submission.reply(comment_text)
                    processed_posts.add(submission.id)  
                    time.sleep(20)
        print("Waiting for 5 minutes")
        time.sleep(300)  # Wait for 5 minutes before checking again

if __name__ == "__main__":
    main()