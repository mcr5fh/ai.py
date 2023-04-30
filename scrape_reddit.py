import sys
import praw
import openai
import json
from collections import Counter
import click
from praw.models import MoreComments
import os
from dotenv import load_dotenv
import time
import pyperclip

from logger import logger


# Load environment variables from .env file
load_dotenv()
# Retrieve API credentials from environment variables
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_secret = os.getenv("REDDIT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=reddit_client_id, client_secret=reddit_secret, user_agent=reddit_user_agent
)

options = {}

def get_post_info(post):
    details = {
        "id": post.id,
        "title": post.title,
        "author": post.author.name if post.author else None,
        "score": post.score,
        "permalink": f"https://www.reddit.com{post.permalink}",
        "url": post.url,
        "created_utc": post.created_utc,
        "num_comments": post.num_comments,
        "selftext": post.selftext,
        "upvote_ratio": post.upvote_ratio,
        "subreddit": post.subreddit.display_name,
    }

    return details


def scrape_single_post(post_id):
    logger.info(f"Scraping post with ID {post_id}")

    post = reddit.submission(id=post_id)
    comments = parse_comments(post)
    return comments

def search_subreddit(subreddit_name, time_filter, search_string, search_limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    # These are lazily loaded
    search_results = subreddit.search(
        search_string, sort="hot", time_filter=time_filter, limit=search_limit
    )

    feedback = []
    logger.info(f"Found {len(search_results.list())} search results")
    for post in search_results:
        post_feedback = analyze_post(post)
        feedback.extend(post_feedback)

    print(str(feedback))
    # summary = summarize_feedback(feedback)
    # return summary


def analyze_post(post):
    # Analyze the post using OpenAI API (you can change this to use other methods)
    post_title = post.title
    comments = post.comments.replace_more(limit=None)  # list()

    # Process each comment
    feedback = []


def parse_comments(post):
    global options
    post.comments.replace_more(limit=None)
    comments = post.comments.list()
    comment_list = []
    logger.info("Number of comments for : " + post.title + " " + str(len(comments)))
    for comment in comments:
        if isinstance(comment, MoreComments):
            logger.debug("Got a MoreComments")
            continue
        if options['exclude_user'] and comment.author and comment.author.name == options['exclude_user']:
            logger.debug(f"Ignoring comment from {comment.author.name}")
            continue
        #         print(comment.id)  # to make it non-lazy
        #         pprint.pprint(vars(comment))
        comment_list.append(comment.body)
    logger.info(f"Found total comments {str(len(comment_list))}")
    return comment_list

    # Return a list of feedback extracted from the post
    return feedback


def summarize_feedback(feedback):
    # Summarize the feedback to get the top 5 liked and disliked items
    # ...

    return summary


@click.command()
@click.option("--subreddit", help="Subreddit to scrape")
@click.option(
    "--time",
    "time_filter",
    default="week",
    type=click.Choice(["all", "day", "hour", "month", "week", "year"]),
    help="Time filter for the search (default: week)",
)
@click.option("--post_id", help="Post ID to scrape")
@click.option("--search_string", default=None, help="Search string (optional)")
@click.option('--exclude_user', default=None, help='Exclude comments from a specific user (optional)')
def main(subreddit, time_filter, post_id, search_string, exclude_user):
    global options
    options = {
        "subreddit": subreddit,
        "post_id": post_id,
        "time_filter": time_filter,
        "search_string": search_string,        
        'exclude_user': exclude_user,

    }
    logger.info(
        f"Scraping subreddit {options['subreddit']} with time filter {options['time_filter']} and search string {options['search_string']}"
    )
    if not subreddit and not post_id:
        raise click.UsageError("You must provide either --subreddit or --post_id")
    if post_id:
        comments = scrape_single_post(post_id)
    else:
        comments = search_subreddit(subreddit, time_filter, search_string)
    logger.info(f"Done scraping")

    pyperclip.copy(str(comments))


if __name__ == "__main__":
    main()
