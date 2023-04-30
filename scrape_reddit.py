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


def scrape_single_post(post_id, exclude_user):
    logger.info(f"Scraping post with ID {post_id}")

    post = reddit.submission(id=post_id)
    comments = parse_comments(post, exclude_user)
    return comments

def search_subreddit(subreddit_name, time_filter, search_string, exclude_user, max_posts=5):
    subreddit = reddit.subreddit(subreddit_name)
    # These are lazily loaded
    search_results = subreddit.search(
        search_string, sort="hot", time_filter=time_filter, limit=max_posts
    )

    comments = []
    for post in search_results:
        post_comments = parse_comments(post, exclude_user)
        comments.extend(post_comments)
    logger.info(f"Found {len(comments)} search results")

    print(str(comments))
    return comments
    
def parse_comments(post, exclude_user):
    post.comments.replace_more(limit=None)
    comments = post.comments.list()
    comment_list = []
    logger.info(f"Found {str(len(comments))} comments for post with title: {post.title}")
    for comment in comments:
        if isinstance(comment, MoreComments):
            logger.debug("Got a MoreComments")
            continue
        if exclude_user and comment.author and comment.author.name == exclude_user:
            logger.debug(f"Ignoring comment from {comment.author.name}")
            continue
        #         print(comment.id)  # to make it non-lazy
        #         pprint.pprint(vars(comment))
        comment_list.append(comment.body)
    logger.info(f"Found total comments {str(len(comment_list))}")
    return comment_list

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
@click.option("--copy_to_clipboard", is_flag=True, help="copy the comments to your clipboard")
@click.option("--search_string", default=None, help="Search string (optional)")
@click.option('--exclude_user', default=None, help='Exclude comments from a specific user (optional)')
@click.option("--max_posts", default=5, help="Max numbers of posts to search within subreddit")
def main(subreddit, time_filter, post_id, copy_to_clipboard, search_string, exclude_user, max_posts):
    options = {
        "subreddit": subreddit,
        "post_id": post_id,
        "time_filter": time_filter,
        "search_string": search_string,        
        'exclude_user': exclude_user,
        'copy_to_clipboard': copy_to_clipboard,
        'max_posts': max_posts
    }
    logger.info(
        f"Scraping subreddit with the following options: {options}"
    )
    if not subreddit and not post_id:
        raise click.UsageError("You must provide either --subreddit or --post_id")
    if post_id:
        comments = scrape_single_post(post_id, exclude_user)
    elif subreddit:
        if not search_string:
            raise click.UsageError("You must provide a search string when searching a subreddit via --search_string")
            
        comments = search_subreddit(subreddit, time_filter, search_string, exclude_user, max_posts)
    logger.info(f"Done scraping. Found {len(comments)} comments")

    print(str(comments))
    if copy_to_clipboard:
        pyperclip.copy(str(comments))
        logger.info(f"Copied {len(comments)} comments to your clipboard. You can CNTRL+V them now")

if __name__ == "__main__":
    main()
