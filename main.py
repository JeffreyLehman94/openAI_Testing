import random
import praw
from gpt_test import request_gpt
import time
from openMethods import *

def joinSubs():
    with open('subreddits.txt') as file:
        for line in file:
            try:
                reddit.subreddit(line.rstrip()).subscribe()
            except Exception as e:
                print(e)
            time.sleep(5)


def checkShadowBan(username):
    try:
        print(reddit.redditor(username).comment_karma)
    except Exception as e:
        print(str(e) + '\n Probably shadow banned!')

def getSubKeywords(debug):
    SUBREDDITS = list(SUBREDDITS_KEYWORDS.keys())
    SELECTED = SUBREDDITS[random.randint(0, len(SUBREDDITS) - 1)]
    KEYWORDS = SUBREDDITS_KEYWORDS[SELECTED]
    if debug: print(SELECTED + ': ' + str(KEYWORDS))
    return SELECTED, KEYWORDS


def main(debug):
    max_comments_per_thread = 1
    SUBREDDIT_KEYWORDS = getSubKeywords(0)
    subreddit = reddit.subreddit(SUBREDDIT_KEYWORDS[0])
    search_query = SUBREDDIT_KEYWORDS[1]
    if debug == 1:
        print(CLIENT_ID[0] + '\n')
        print(CLIENT_SECRET[0] + '\n')
        print(CLIENT_USERNAME[0] + '\n')
        print(CLIENT_PASSWORD[0] + '\n')
        print(CLIENT_USER_AGENT[0] + '\n')
    if debug == 1: print('Searching for post...')
    for submission in subreddit.hot(limit=10):
        if not submission.archived:
            comments_in_thread = 0
            for comment in submission.comments:
                if comments_in_thread < max_comments_per_thread and \
                        any(keyword in comment.body.lower() for keyword in search_query) and \
                        not any(stop_word in comment.body.lower() for stop_word in STOP_WORDS[0]) and \
                        len(comment.body.lower()) > 30:
                    try:
                        reply_text = request_gpt(comment.body)
                        print('POSTING COMMENT:%s' % reply_text)
                        print('YOU HAVE 10 SECONDS TO STOP THIS POST IF YOU WANT.')
                    except Exception as e:
                        print(str(e) + '\n GPT EXCEPTION')
                        break;
                    time.sleep(10)
                    try:
                        comment.reply(reply_text)
                        print("COMMENT MADE\n")
                    except Exception as e:
                        print(str(e) + '\n POSTING EXCEPTION')
                        break;
                    comments_in_thread += 1
                    time.sleep(random.randint(60 * 5, 60 * 10))


reddit = praw.Reddit(
    client_id=CLIENT_ID[0],
    client_secret=CLIENT_SECRET[0],
    username=CLIENT_USERNAME[0],
    password=CLIENT_PASSWORD[0],
    user_agent=CLIENT_USER_AGENT[0]
)
