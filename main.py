import time
import praw
import config
import re

def bot_login():
    # Login with praw
    print ("Logging in...")
    r = praw.Reddit(username = config.username,
                    password= config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "Combo Translator Bot")
    print ("Logged in!")

    return r

def getRelevantComments(r,startTime):
    # Get comments in </r/dragonballfigtherz>
    relevantComments = []

    #print "Obtaining last 20 comments..."
    # Go over the last 20 comments
    for comment in r.subreddit('privbottest').comments(limit=20):
        try:
            if comment.created_utc > startTime and comment.author.name != config.username:
                relevantComments.append(comment)
        except Exception as e:
            pass  # comment probably deleted

    return relevantComments,time.time()

def replyToComment(comment,msg):
    commentFormat = '\n\n ______________________________________ \n\n' \
                    '^(I AM A BOT, use {combo} to call me.)  \n ' \
                    '[Source Code](https://github.com/Ronserruya/DL_HowToObtain_Reddit_Bot)'
    try:
        comment.reply(msg + commentFormat)
    except Exception as e:
        pass  # comment probably deleted

def reportError(r,comment,cardname,message):
    errorMsg = '{} Error report:  \n\n' \
               'Comment: {}  \n\n' \
               'Cardname: {}  \n\n' \
               'Error: {}'.format(config.username,comment.permalink,cardname,message)
    r.redditor(config.developer).message('{} Error report'.format(config.username),errorMsg)

def textToCombo(text):
    dictonary = {
        ' ': '',
        ',': ',',
        '1': '↙',
        '2': '↓',
        '3': '↘',
        '4': '←',
        '5': '',
        '6': '→',
        '7': '↖',
        '8': '↑',
        '9': '↗',
        'h': 'B',
        'l': 'X',
        's': 'A',
        'm': 'Y',
        'j': '↑',
        'D': 'dash',
        'A': 'assist',
        'r': 'RB',
        'R': 'RT',
        'v': 'vanish',
        '.': ''
    }
    combo = ''
    text = text.replace('dash','D').replace('vanish','v').replace('assist','A').replace('lm','r').replace('ml','r').replace('sh','R')\
        .replace('hs','R').replace('mh','v').replace('hm','v').replace('a','A')
    for char in text:
        combo += dictonary.get(char,'?')

    combo = combo.replace('↓↘→','↺').replace('↓↙←','↻')
    return combo

def run_bot(r,startTime):
    relevantComments,startTime = getRelevantComments(r,startTime)
    if len(relevantComments) == 0:
        #print 'No relevant comments'
        return startTime

    for comment in relevantComments:
        output = ''
        #Get any string between {}
        try:
            combos = re.findall('(?<=\{)(.*?)(?=\})',comment.body)
        except Exception as e:
            continue

        for combo in combos:
            if len(combo) > 0:
                output += textToCombo(combo) + '  \n'

        replyToComment(comment,output)



    return startTime




def main():
    startTime = time.time() #Current UNIX time

    r = bot_login()
    while True:
        # startTime gets the last time I went over the comments
        startTime = run_bot(r,startTime)
        #print "Waiting for 30 seconds"
        time.sleep(30)



if __name__ == '__main__':
    main()
