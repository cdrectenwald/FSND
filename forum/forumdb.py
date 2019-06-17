# "Database code" for the DB Forum.

import datetime
import psycopg2

POSTS = [("This is the first post.", datetime.datetime.now())]
#db-name=psycopg2.connect("dbname=news")

def get_posts():
  """Return all posts from the 'database', most recent first."""

  return reversed(POSTS)

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  POSTS.append((content, datetime.datetime.now()))


#questions our reporting tool should answer
# 1.What are the most popular three articles of all time
#2. Who are the most popular article authors of all time?
# 3. ON which days did more than 1% of requests lead to errors?