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

## Running the Scraper

You can run the scraper using the following command:

```bash
python scrape_reddit.py --subreddit "your_subreddit" --time "your_time_filter" --search_string "your_search_string" --exclude_user "username_to_exclude"
```

Replace the following placeholders with your desired values:

- `your_subreddit`: The subreddit you want to scrape.
- `your_time_filter`: The time filter for the search (all, day, hour, month, week, or year).
- `your_search_string`: The search string for filtering posts (optional).
- `username_to_exclude`: Exclude comments from a specific user (optional).

You can also scrape a single post and its comments using the `--post_id` option:

```bash
python scrape_reddit.py --post_id "your_post_id"
```

Replace `your_post_id` with the ID of the post you want to scrape.

## Deactivating the Virtual Environment

When you're done using the scraper, deactivate the virtual environment with the following command:

```bash
deactivate
```
