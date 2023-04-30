# ai.py

This is a Python-package for a variety of things, so far there is a reddit scraper and some code to mess around with hugging face models.

## Prerequisites

- Python 3
- pip

## Setting Up the Environment

```bash
# 1. Clone the repository:
git clone https://github.com/mcr5fh/ai.py.git
cd ai.py

# 2. Create a virtual environment and activate it:
python3 -m venv ai.py.venv
source ai.py.venv/bin/activate

# 3. Install the required dependencies:
pip install -r requirements.txt
```

# Reddit Scraper

**NOTE: You have to have a reddit dev account set up. You can follow that here: https://github.com/reddit-archive/reddit/wiki/OAuth2

Then put that in a `.env` file like so: 

```bash
# Reddit API credentials
REDDIT_CLIENT_ID="aaaaaa"
REDDIT_SECRET="bbbbbb"
REDDIT_USER_AGENT="reddit script by u/whoever"
```

## About
This is a wrapper around the PRAW Reddit sdk here: https://praw.readthedocs.io/en/stable/getting_started/quick_start.html

### CLI
```bash
Usage: scrape_reddit.py [OPTIONS]

Options:
  --subreddit TEXT                Subreddit to scrape
  --time [all|day|hour|month|week|year]
                                  Time-from-now filter for the search (default: week)
  --post_id TEXT                  Post ID to scrape
  --copy_to_clipboard             copy the comments to your clipboard
  --search_string TEXT            Search string (optional)
  --exclude_user TEXT             Exclude comments from a specific user
                                  (optional)
  --max_posts INTEGER             Max numbers of posts to search within
                                  subreddit
  --help                          Show this message and exit.
```

### Scrape a Single Post

To scrape a single post and its comments, you will need the post ID. You can find the post ID in the URL of the post. It is usually a 6-character alphanumeric string. For example, in the URL `https://www.reddit.com/r/whoop/comments/102df41/rwhoop_team_created/`, the post ID is `102df41`.

Use the `--post_id` option to specify the post ID:

```bash
python scrape_reddit.py --post_id "102df41"
```

(Optional) To exclude comments from a specific user, use the `--exclude_user` option:

```bash
python scrape_reddit.py --post_id "102df41" --exclude_user "username_to_exclude"
```


### Search a Subreddit

To search Reddit for posts in a specific subreddit, use the `--subreddit` option, and you must pass a `--search_string` as well:

```bash
python scrape_reddit.py --subreddit "whoop" --search_string "Strength Builder"
```

(Optional) To specify a time frame "from now" for the search, use the `--time` option. Available time frames are "all", "day", "hour", "month", "week", or "year". For example, passing in "month" searches all posts within the past month. 

```bash
python scrape_reddit.py --subreddit "whoop" --search_string "Strength Builder" --time "month"
```

You can also scrape a single post and its comments using the `--post_id` option:

```bash
python scrape_reddit.py --post_id "your_post_id"
```

Replace `your_post_id` with the ID of the post you want to scrape.

## Copying Results to Clipboard

To copy the results to the clipboard, use the `--copy_to_clipboard` flag:

```bash
python scrape_reddit.py --subreddit "your_subreddit" --copy_to_clipboard
```

### Real Example
```bash
(ai.py.venv) ➜  ai.py git:(main) ✗ python3 scrape_reddit.py --post_id 130mgyl --exclude_user whoop_official  --copy_to_clipboard
2023-04-30T19:28:15Z - INFO - Scraping subreddit None with time filter week and search string None
2023-04-30T19:28:15Z - INFO - Scraping post with ID 130mgyl
2023-04-30T19:28:18Z - INFO - Number of comments for : WHOOP x Reddit Ask Us Anything: Strength Trainer 💪 313
2023-04-30T19:28:18Z - INFO - Found total comments 241
2023-04-30T19:28:18Z - INFO - Done scraping. Found 241 comments

["It would also be pretty cool if they added it as its own separate category for progress tracking even though it has nothing to do with the wearable itself. I weigh myself daily as I'm always either cutting or bulking and like to see where I'm at with specific calorie intake."...

2023-04-30T19:35:20Z - INFO - Copied 241 comments to your clipboard. You can CNTRL+V them now
```
## Deactivating the Virtual Environment

When you're done using the scraper, deactivate the virtual environment with the following command:

```bash
deactivate
```
