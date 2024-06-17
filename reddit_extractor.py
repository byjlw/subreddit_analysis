import praw
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Reddit Data Extractor Script')
parser.add_argument('--subreddit', required=True, help='Name of the subreddit')
parser.add_argument('--posts_limit', type=int, default=10, help='Number of posts to fetch (default: 10)')
parser.add_argument('--comments_limit', type=int, default=None, help='Number of comments per post (default: all)')
parser.add_argument('--output_filename', default=None, help='Output filename (default: data/<subreddit>.txt)')
parser.add_argument('--client_id', required=True, help='Reddit API client ID')
parser.add_argument('--client_secret', required=True, help='Reddit API client secret')
parser.add_argument('--user_agent', default='data_extractor/0.1', help='Reddit API user agent')

# Parse arguments
args = parser.parse_args()

# Initialize PRAW
reddit = praw.Reddit(client_id=args.client_id, client_secret=args.client_secret, user_agent=args.user_agent)

# Subreddit name and output filename
subreddit_name = args.subreddit
output_filename = args.output_filename if args.output_filename else f'data/{subreddit_name}.txt'

# Initialize subreddit instance
subreddit = reddit.subreddit(subreddit_name)

# Extract and save data
with open(output_filename, 'w', encoding='utf-8') as file:
    for post in subreddit.hot(limit=args.posts_limit):
        file.write(f"Title: {post.title} | Posted by: {post.author}\n")
        if post.is_self and post.selftext:
            file.write(f"Post: {post.selftext}\n")
        elif hasattr(post, 'url'):
            file.write(f"Content URL: {post.url}\n")
        else:
            file.write("Post content is not available.\n")

        post.comments.replace_more(limit=0)
        comment_count = 0
        for comment in post.comments.list():
            if args.comments_limit is None or comment_count < args.comments_limit:
                file.write(f"Comment by {comment.author}: {comment.body}\n")
                comment_count += 1
            else:
                break
        file.write("\n=======================================\n\n")

print(f"Data extracted and saved to {output_filename}")
