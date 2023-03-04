import random
import praw
import time
from openMethods import *


# todo: Add more subreddits/keywords OR reconfigure to response to top comment
# todo: Remove debug stuff
# todo: Work on prompt - it is not engaging enough and sometimes responds as if the commenter is talking to it

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


def getAlreadyPosted(id):
    path = 'db/db.sqlite3'
    scriptdir = os.path.dirname(__file__)
    db_path = os.path.join(scriptdir, path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    con = sqlite3.connect(db_path + "reddit.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS REDDIT_POSTS(DATE, USER, ID)")
    con.commit()
    cur.execute("SELECT * FROM REDDIT_POSTS WHERE USER IS ? AND ID IS ?", (CLIENT_USERNAME[0], id))
    rows = cur.fetchall()
    if (len(rows) == 0):
        cur.execute(" INSERT INTO REDDIT_POSTS VALUES(?, ?, ?)", (date.today(), CLIENT_USERNAME[0], id))
        con.commit()
    else:
        print('ALREADY COMMENTED ON THIS POST')
    con.close()
    return len(rows)


def main(debug):
    max_comments_per_thread = 1
    SUBREDDIT_KEYWORDS = getSubKeywords(0)
    subreddit = reddit.subreddit(SUBREDDIT_KEYWORDS[0])
    search_query = SUBREDDIT_KEYWORDS[1]
    checkShadowBan(CLIENT_USERNAME[0])
    if debug == 1: print('Searching for post...')
    for submission in subreddit.hot(limit=10):
        if not submission.archived and not getAlreadyPosted(submission.id):
            comments_in_thread = 0
            for comment in submission.comments:
                if comments_in_thread < max_comments_per_thread and \
                        any(keyword in comment.body.lower() for keyword in search_query) and \
                        not any(stop_word in comment.body.lower() for stop_word in STOP_WORDS[0]) and \
                        len(comment.body.lower()) > 30:
                    reply_text = getResponse(comment.body, submission.id)
                    print('PROMPT:        :%s' % comment.body)
                    print('POSTING COMMENT:%s' % reply_text)
                    print('YOU HAVE 10 SECONDS TO STOP THIS POST IF YOU WANT.')
                    time.sleep(10)
                    comment.reply(reply_text)
                    print("COMMENT MADE\n")
                    comments_in_thread += 1
                    sleep_time = random.randint(60 * 10, 60 * 15)
                    print('sleeping for %i' % sleep_time)
                    time.sleep(sleep_time)

print('test')
reddit = praw.Reddit(
    client_id=CLIENT_ID[0],
    client_secret=CLIENT_SECRET[0],
    username=CLIENT_USERNAME[0],
    password=CLIENT_PASSWORD[0],
    user_agent=CLIENT_USER_AGENT[0]
)

main(0)
