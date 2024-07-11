# Subreddit Analysis

## Overview

Subreddit Analysis is a Python project for asking questions about a particular subreddit.

It works by:
- Ingesting the posts and comments of a particular subreddit
- Indexing the data
- Leveraging an LLM to interact with the index

This tool is particularly useful for researchers, marketers, and community managers looking to analyze subreddit content without manually collecting data.

## Features

- Extracts post titles, bodies (or content URLs for non-text posts), and comments, along with the authors' usernames.
- Customizable limits for the number of posts and comments to fetch.
- Runs completely local using the LLM and embed model of your choice
- Indexs the downloaded data + any other data you want included
- Use prompts to ask questions about the data in the index using Ollama

## Prerequisites
*note recommend running in a virtual environment*
```
python3 -m venv .venv
source .venv/bin/activate
```

Before running this script, ensure you have:

- Python 3 installed on your system.
- [Ollama installed on your system](https://ollama.com/download)
- PRAW (Python Reddit API Wrapper) library installed. Install via pip if not already done:
```
pip install praw
```
- [llama index](https://github.com/run-llama/llama_index/tree/main)
```
pip install llama-index-core llama-index-readers-file llama-index-llms-ollama llama-index-embeddings-huggingface
```
- Valid Reddit API credentials (`client_id`, `client_secret`, and `user_agent`). Follow the instructions below to obtain these.

## Obtaining Reddit API Credentials

1. **Create or log in to your Reddit account.**

2. **Navigate to the Reddit apps page** by going to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps).

3. **Create a new application** by clicking on the "Create App" or "Create Another App" button at the bottom.

4. **Fill out the form** with the required details:
 - Name: Give your application a name.
 - App type: Select "script".
 - Description: (Optional) A brief description.
 - About URL: (Optional) URL for your app.
 - Redirect URI: Use `http://localhost` for a script application.

5. **Note your `client_id` and `client_secret`** once the app is created. The `client_id` is found under the app name. The `client_secret` is labeled as such.

6. **Set your User Agent**, which should include the name of your app and a version number, e.g., `my_reddit_app/0.1`.

## Installation

1. **Clone or download the script** to your local machine.

2. **Ensure you have your Reddit API credentials ready.**

## Usage

### Pull data from Reddit
Execute the script from the command line,

```
python reddit_extractor.py --subreddit <subreddit_name> --client_id <your_client_id> --client_secret <your_client_secret> [options]
```
**Required Arguments**

- `--subreddit`: The name of the subreddit from which to extract data.
- `--client_id`: Your Reddit API client ID.
- `--client_secret`: Your Reddit API client secret.

**Optional Arguments**

- `--posts_limit`: The number of posts to fetch (default is 10).
- `--comments_limit`: The number of comments to fetch per post (default fetches all comments).
- `--output_filename`: The name of the output file (default: data/<subreddit>.txt)'`
- `--output_format`: Format of the output file. Options: text, json (default: json)`
- `--submission_id`: Get details on just a single post instead of a collection of posts within the subreddit. For the URL `https://www.reddit.com/r/Python/comments/abcdef/some_post_title/`, the submission ID is `abcdef`

```
python reddit_extractor.py --subreddit books --posts_limit 5 --comments_limit 20 --client_id YOUR_CLIENT_ID --client_secret YOUR_CLIENT_SECRET
```

## Analyze using llama index and Ollama

If you used the defaults above you'll end up with a file with posts and comments in the data directory. The defaults will look in that directory
```
python analyze.py --prompt "what do the members care about?"
```

**Required Arguments**

- `--prompt`: Query or prompt to use to query the index (required)

**Optional Arguments**

- `--data_dir`: Directory containing Reddit data text files (default: data)

- `--embed_model`: Hugging Face embedding model to use (default: BAAI/bge-base-en-v1.5)

- `--llm_model_name`: OLLAMA LLM model name to use (default: llama3:70b)

- `--timeout`: Request timeout against OLLAMA (default: 360.0 seconds)

## Note

- Replace placeholder values with actual data.
- Adhere to Reddit's API rate limits and guidelines to prevent access issues.
- Keep your client secret secure and comply with Reddit's user agreement and privacy policies.
