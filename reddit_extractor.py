import praw
import argparse
import os
import time
import random
import json

# Set up argument parser
parser = argparse.ArgumentParser(description='Reddit Data Extractor Script')
parser.add_argument('--subreddit', required=True, help='Name of the subreddit')
parser.add_argument('--posts_limit', type=int, default=10, help='Number of posts to fetch (default: 10)')
parser.add_argument('--comments_limit', type=int, default=None, help='Number of comments per post (default: all)')
parser.add_argument('--output_filename', default=None, help='Output filename (default: data/<subreddit>.<format>)')
parser.add_argument('--client_id', required=True, help='Reddit API client ID')
parser.add_argument('--client_secret', required=True, help='Reddit API client secret')
parser.add_argument('--user_agent', default='data_extractor/0.1', help='Reddit API user agent')
parser.add_argument('--output_format', default='json', help='Format of the output file. Options: text, json (default: json)')

# Parse arguments
args = parser.parse_args()

# Initialize PRAW
reddit = praw.Reddit(client_id=args.client_id, client_secret=args.client_secret, user_agent=args.user_agent)

# Subreddit name and output filename
subreddit_name = args.subreddit
output_filename = args.output_filename if args.output_filename else f'data/{subreddit_name}'

# Initialize subreddit instance
subreddit = reddit.subreddit(subreddit_name)

# Extract and save data
dir_path = os.path.dirname(output_filename)
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

def format_comment_text(comment, depth=0):
    padding = '    ' * depth
    comment_text = f"{padding}Comment by {comment.author}:\n{padding}    {comment.body}\n"
    # All direct replies to this comment will have the same indentation as the comment itself
    for reply in comment.replies:
        comment_text += format_comment_text(reply, depth + 1)  # Indent replies once from the parent comment
    return comment_text

def format_comment_json(comment):
    return {
        'id': comment.id,
        'author': str(comment.author),
        'body': comment.body,
        'replies': [format_comment_json(reply) for reply in comment.replies] if hasattr(comment, 'replies') else []
    }

def process_comments(comment, format_type):
    if format_type == 'text':
       return format_comment_text(comment, 1)  # Start with depth 1 for top-level comments
    elif format_type == 'json':
        return format_comment_json(comment)

def get_post_details(post, output_format, comments_limit):
    post.comments.replace_more(limit=None)  # Expands all comments
    if output_format == 'text':
        details = f"Post Title: {post.title}\nAuthor: {post.author}\n\nPost Text:\n{post.selftext}\n\nComments:\n"
        for comment in post.comments.list():
            details += process_comments(comment, 'text')
    elif output_format == 'json':
        details = {
            'title': post.title,
            'author': str(post.author),
            'selftext': post.selftext,
            'comments': [process_comments(comment, 'json') for comment in post.comments.list()]
        }
    else:
        raise ValueError("Unsupported output format. Use 'text' or 'json'.")
    return details

def save_collection_of_posts(posts, output_format, filename, comments_limit=None):
    file_extension = 'txt' if output_format == 'text' else 'json'
    with open(f'{filename}.{file_extension}', 'w', encoding='utf-8') as f:
        if output_format == 'json':
            all_posts_details = [get_post_details(post, 'json', comments_limit) for post in posts]
            json.dump(all_posts_details, f, ensure_ascii=False, indent=4)
        else:
            for post in posts:
                details = get_post_details(post, 'text', comments_limit)
                f.write(details + "\n\n" + "-"*80 + "\n\n")
                time.sleep(random.uniform(0, 1))

save_collection_of_posts(subreddit.hot(limit=args.posts_limit), args.output_format, output_filename)


print(f"Data extracted and saved to {output_filename}")
