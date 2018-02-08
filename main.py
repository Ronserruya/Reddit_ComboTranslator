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
    # Get comments in </r/dragonballfighterz>
    relevantComments = []

    #print "Obtaining last 20 comments..."
    # Go over the last 20 comments
    for comment in r.subreddit('dragonballfighterz').comments(limit=20):
        try:
            if comment.created_utc > startTime and comment.author.name != config.username:
                relevantComments.append(comment)
        except Exception as e:
            pass  # comment probably deleted

    return relevantComments,time.time()

def replyToComment(comment,msg):
    commentFormat = '\n\n ______________________________________ \n\n' \
                    '^(I AM A BOT, use {combo} to call me. Im still new and may be wrong, mistake? Please PM me!)  \n' \
                    '[Don\'t rely on me, learn to read combos! :)]' \
                    '(https://www.reddit.com/r/dragonballfighterz/comments/7lagry/diggys_dojo_basic_mechanics_controls_and_notations/)  \n' \
                    '[Source Code](https://github.com/Ronserruya/Reddit_ComboTranslator)'
    try:
        comment.reply(msg + commentFormat)
    except Exception as e:
        pass  # comment probably deleted

def reportError(r,e):
    errorMsg = '{} Error report:  \n\n' \
               '{}'.format(config.username,e)
    r.redditor(config.developer).message('{} Error report'.format(config.username),errorMsg)

def textToComboXbox(text):
    dictonary = {
        ' ': ' ',
        ',': '>',
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
        'w': 'wait',
        'L': 'land',
        'D': 'dash',
        'A': 'assist',
        'r': 'RB',
        'R': 'RT',
        'v': 'vanish',
        '>': '>'
    }
    combo = ''

    # Replace common phrases with matching characters
    text = text.replace('dash','D').replace('vanish','v').replace('assist','A').replace('sd','D')\
        .replace('jump','j').replace('land','L').replace('wait','w').replace('lm','r').replace('ml','r').replace('sh','R')\
        .replace('hs','R').replace('mh','v').replace('hm','v').replace('a','A').replace('j.','')

    # Go over each character and translate it using the dictionary above
    for char in text:
        combo += dictonary.get(char,char)

    combo = combo.replace('↓↘→','↺').replace('↓↙←','↻')
    return combo

def textToComboPS(text):
    dictonary = {
        ' ': ' ',
        ',': '>',
        '1': '↙',
        '2': '↓',
        '3': '↘',
        '4': '←',
        '5': '',
        '6': '→',
        '7': '↖',
        '8': '↑',
        '9': '↗',
        'h': '○',
        'l': '□',
        's': '×',
        'm': '△',
        'j': '↑',
        'w': 'wait',
        'L': 'land',
        'D': 'dash',
        'A': 'assist',
        'r': 'R1',
        'R': 'R2',
        'v': 'vanish',
        '>': '>'
    }
    combo = ''

    # Replace common phrases with matching characters
    text = text.replace('dash','D').replace('vanish','v').replace('assist','A').replace('sd','D')\
        .replace('jump','j').replace('land','L').replace('wait','w').replace('lm','r').replace('ml','r').replace('sh','R')\
        .replace('hs','R').replace('mh','v').replace('hm','v').replace('a','A').replace('j.','')

    # Go over each character and translate it using the dictionary above
    for char in text:
        combo += dictonary.get(char,char)

    combo = combo.replace('↓↘→','↺').replace('↓↙←','↻')
    return combo

def run_bot(r,startTime):
    relevantComments,startTime = getRelevantComments(r,startTime)
    if len(relevantComments) == 0:
        return startTime

    for comment in relevantComments:
        output = ''
        #Get any string between {}
        combos = re.findall('(?<=\{)(.*?)(?=\})',comment.body)
        if len(combos) == 0:
            continue

        output += 'Xbox:  \n'
        for combo in combos:
            if len(combo) > 0:
                output += textToComboXbox(combo.lower()) + '  \n'

        output += '  \nPS:  \n'
        for combo in combos:
            if len(combo) > 0:
                output += textToComboPS(combo.lower()) + '  \n'

        replyToComment(comment,output)

    return startTime



def main():
    startTime = time.time()  # Current UNIX time
    r = bot_login()
    try:
        while True:
            # startTime gets the last time I went over the comments
            startTime = run_bot(r, startTime)
            time.sleep(30)
    except Exception as e:
        reportError(r,e)




if __name__ == '__main__':
    main()
