Reddit Search Notifications
Author: Sam Clotfelter

This script uses reddits search feature to notify when there are new posts containing the given string in the given subreddit(s).

Runs in linux only.

# Usage

## Create the config file

1. Make a file called `config` in the same directory.

2. The file should be 3 lines long with the following content.

	\[subreddits separated by commas\]
	\[search term\]
	\[most\_recent\]

	See `config.example`

## Run

Run

`python reddit-search-notifications.py`

The script will run continuously on a timer. When it finds search results newer than most_recent value, it notifies the user.

Set most_recent to the current time with

`python reddit-search-notifications.py -r`

