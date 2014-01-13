
import sys
import MySQLdb

PATH_TO_PROJECT = "/Users/Herg/Documents/Projects/recommenditor/recommenditor"
sys.path.append(PATH_TO_PROJECT)

from services.reddit_service import redditor
from services.db_service import db_service

db = db_service()
#r = redditor("hergieherg", "")


# Get the subreddit data
def get_subreddits():
    data = r.get_subreddits(limit=100000)
    for row in data:
        res1 = db.execute("""
            SELECT * FROM reddit.subreddits where subreddit_id=%s
            """,[row[1]])
        if res1["status"] != 1:
            print res1["errmsg"]
            raise
        try:
            subreddit_id = db.get_results()[0][1]
            continue
        except:
            pass
        res = db.execute("""
            INSERT INTO reddit.subreddits VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, row
            )
        if res["status"] != 1:
            break
        db.commit()


def get_authors():
    res = db.execute("""SELECT url FROM subreddits""")
    if res["status"] != 1:
        print res
        raise
    data = db.get_results()
    for tup in data:
        print tup[0]
        authors = r.get_subreddit_submission_authors(subreddit_url=tup[0])
        for author in authors:
            res = db.execute("""
                INSERT INTO reddit.authors VALUES (%s)
                """, author)
            if res["status"] != 1:
                break
            db.commit()


def get_user_submissions():
    # Get all of our usernames to look up
    res = db.execute("""select username from submitters where username>="bdls39b"order by username""")
    if res["status"] != 1:
        print res
        raise
    results = db.get_results()
    usernames = [row[0] for row in results]
    rot = 0
    for username in usernames:
        print username
        # Get the posts submitted by the user from Reddit
        submitted_res = r.get_user_submissions(username=username, limit=1000)
        submission_arr = []
        for s in submitted_res:
            if s[3] in submission_arr:
                continue
            submission_arr.append(s[3])
        for sub in submission_arr:
            res = db.execute("""
                INSERT INTO reddit.submissions VALUES (%s, %s)
                """, (username, sub))
            if res["status"] != 1:
                print "EXITING"
                print res
                return
            db.commit()


def get_user_comments():
    # Get all of our usernames to look up
    res = db.execute("""select username from submitters where username<="bdls39b" and username>="1d10t_error" order by username""")
    if res["status"] != 1:
        print res
        raise
    results = db.get_results()
    usernames = [row[0] for row in results]
    rot = 0
    for username in usernames:
        print username
        # Get the posts submitted by the user from Reddit
        comments_res = r.get_user_comments(username=username, limit=1000)
        comments_arr = []
        for c in comments_res:
            if c[3] in comments_arr:
                continue
            comments_arr.append(c[3])
        res = db.execute("""
            SELECT subreddit_id from reddit.submissions where username=%s
            """, [username])
        already_exists = [subreddit_id[0] for subreddit_id in db.get_results()]
        for com in comments_arr:
            if com in already_exists:
                continue
            print "\tFound a new one!"
            res = db.execute("""
                INSERT INTO reddit.submissions VALUES (%s, %s)
                """, (username, com))
            if res["status"] != 1:
                print "EXITING"
                print res
                return
            db.commit()


def do_rankings():
    # this is because i dont know how to do rank() in mysql. god damnit
    res = db.execute("""select distinct subreddit_id_2 from subreddit_scores""")
    subreddits = [subreddit_arr[0] for subreddit_arr in db.get_results()]
    print str(len(subreddits))
    rot = 0
    for subreddit_id in subreddits:
        to_insert = []
        res = db.execute("""select subreddit_id_2, subreddit_id_1, score
            from subreddit_scores where subreddit_id_2=%s
            order by score desc
            limit 10
            """,[subreddit_id])
        for row in db.get_results():
            to_insert.append([row[0], row[1], row[2]])
        for row in to_insert:
            db.execute("""
                insert into subreddit_recommendations values (%s, %s, %s)
                """, [row[0], row[1], row[2]])
        db.commit()
        rot = rot + 1
        if rot % 100 == 0:
            print str(rot)

do_rankings()




