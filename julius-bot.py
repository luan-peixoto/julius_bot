# coding=utf-8
import tweepy
import time
import datetime
from os import environ
from random import randint

# --------------------------------------------------------------------------  KEYS yes

auth_0 = tweepy.OAuthHandler(environ['CONSUMER_KEY_0'], environ['CONSUMER_SECRET_0'])
auth_0.set_access_token(environ['ACCESS_KEY_0'], environ['ACCESS_SECRET_0'])
api_0 = tweepy.API(auth_0, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

auth_1 = tweepy.OAuthHandler(environ['CONSUMER_KEY_1'], environ['CONSUMER_SECRET_1'])
auth_1.set_access_token(environ['ACCESS_KEY_1'], environ['ACCESS_SECRET_1'])
api_1 = tweepy.API(auth_1, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

auth_2 = tweepy.OAuthHandler(environ['CONSUMER_KEY_2'], environ['CONSUMER_SECRET_2'])
auth_2.set_access_token(environ['ACCESS_KEY_2'], environ['ACCESS_SECRET_2'])
api_2 = tweepy.API(auth_2, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# -------------------------------------------------------------------------- CHECK SPAM
burros = []


def time_checker(tweet_id, tweet_created_at, user_screen_name, search_text):
    time_spam = datetime.timedelta(0, 0, 0, 0, 3, 0, 0)
    current_tweet = datetime.datetime.strptime(tweet_created_at, '%Y-%m-%d %H:%M:%S')
    for twt in tweepy.Cursor(api_0.user_timeline, id=user_screen_name, tweet_mode='extended', include_rts=False).items(
            10):
        try:
            if twt.id != tweet_id:
                if search_text in twt.full_text.lower():
                    tweet_time = datetime.datetime.strptime(str(twt.created_at), '%Y-%m-%d %H:%M:%S')
                    if current_tweet > tweet_time:
                        if (current_tweet - tweet_time) <= time_spam:
                            return True
                    else:
                        if (tweet_time - current_tweet) <= time_spam:
                            return True
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break
    return False


# -------------------------------------------------------------------------- CHECK TEXT FILE FUNCTION
FILE_NAME = 'last_interaction_id.txt'
STATUS_NAME = 'status.txt'


def retrieve_text(file_name):
    file = open(file_name, 'r')
    text = str(file.read().strip())
    file.close()
    return text


def store_text(text, file_name):
    file = open(file_name, 'w')
    file.write(str(text))
    file.close()
    return


# -------------------------------------------------------------------------- SEARCH
pesquisa = 'julius?'
pesquisa_f = 'julius?!'
tweet_number = 20
filter = ['en', 'ja', 'fr', 'it', 'ru', 'in', 'es', 'ceb', 'de', 'tl']

# -------------------------------------------------------------------------- REPLIES
the_reply = ['Esse tweet custou ',
             '1 dólar e ',
             ' centavos.',
             ' dólares e ',
             'Se você não comprar nada, o desconto é maior.', 'Aceita vale-refeição?',
             'Pra que você vai sair pra relaxar se você pode relaxar em casa e de graça?',
             'Eu me lembro dos primeiros 35 dólares que eu achei. Era 17 horas, em frente ao banco, fazia 27 graus, eu achei duas notas de 10, duas de 5, três moedas de 1 dólar, quatro de 25, e 100 moedas de 1 centavo. E uma delas era canadense.',
             'Quer saber o que é mágica? Eu tenho dois empregos, trabalho sete dias por semana e todo dia meu dinheiro desaparece.',
             'Eu ganhei meus primeiros 30 dólares quando tinha 20 anos, e ainda não gastei tudo.', 'O @',
             ' está te devendo ']


# -------------------------------------------------------------------------- POSTS
def reply_tt(api_n,current):
    last_seen_id = int(retrieve_text(FILE_NAME))
    print('Searching for tweets...')
    tweets = []
    for tt in tweepy.Cursor(api_0.search, pesquisa + ' -filter:retweets', since_id=last_seen_id,
                            tweet_mode='extended',
                            result_type='recent').items(tweet_number):
        tweets.append(tt)
    for tweet in reversed(tweets):
        try:
            last_seen_id = int(retrieve_text(FILE_NAME))
            print('Found Tweet ID: ' + str(tweet.id))
            if pesquisa in tweet.full_text.lower():
                if tweet.lang not in filter:
                    check = time_checker(tweet.id, str(tweet.created_at), tweet.user.screen_name, pesquisa)
                    if check:
                        print('User already requested in less than 3 minutes, ignoring...')
                        burros.append(tweet.user.screen_name)
                    else:
                        friends = api_0.show_friendship(source_screen_name='bot_do_julius',
                                                        target_screen_name=tweet.user.screen_name)
                        if (tweet.in_reply_to_status_id is not None) and (pesquisa_f in tweet.full_text.lower()) and (
                                friends[0].followed_by == True):
                            print("It's a request number 2.")
                            main_tweet = api_0.get_status(tweet.in_reply_to_status_id)
                            resp = randint(0, 3)
                            api_n.create_favorite(tweet.id)
                            if resp < 2:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[10] + main_tweet.user.screen_name +
                                    the_reply[11] + str(randint(15, 99)) + the_reply[2], in_reply_to_status_id=tweet.id)
                            elif 1 < resp < 3:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[10] + main_tweet.user.screen_name +
                                    the_reply[11] + the_reply[1] + str(randint(15, 99)) + the_reply[2],
                                    in_reply_to_status_id=tweet.id)
                            else:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[10] + main_tweet.user.screen_name +
                                    the_reply[11] + str(randint(2, 8)) + the_reply[3] + str(randint(15, 99)) +
                                    the_reply[2], in_reply_to_status_id=tweet.id)
                            time.sleep(randint(62, 72))

                        else:
                            resp = randint(0, 20)
                            api_n.create_favorite(tweet.id)
                            if resp < 7:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[0] + str(
                                        randint(15, 99)) + the_reply[2],
                                    in_reply_to_status_id=tweet.id)
                            elif 11 > resp > 6:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[0] + the_reply[1] + str(
                                        randint(15, 99)) + the_reply[2], in_reply_to_status_id=tweet.id)
                            elif 15 > resp > 10:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[0] + str(randint(2, 8)) +
                                    the_reply[3] + str(randint(15, 99)) + the_reply[2],
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 15:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[4],
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 16:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[5],
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 17:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[6],
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 18:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[7],
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 19:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[8],
                                    in_reply_to_status_id=tweet.id)
                            else:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[9],
                                    in_reply_to_status_id=tweet.id)
                            if current == 'ONE':
                                store_text('TWO', STATUS_NAME)
                            else:
                                store_text('ONE', STATUS_NAME)
                            time.sleep(randint(60, 70))
                else:
                    print('Not a br tweet, skipping...')
            else:
                print('Keyword not found, skipping...')
            if int(tweet.id) > int(last_seen_id):
                store_text(tweet.id, FILE_NAME)
                print('Last seen ID updated - ' + str(tweet.id))
        except tweepy.TweepError as e:
            print(e.reason)
            if '261' in e.reason:
                if current == 'ONE':
                    store_text('OFF', 'api_1.txt')
                    time.sleep(300)
                    break
                else:
                    store_text('OFF', 'api_2.txt')
                    time.sleep(300)
                    break

        except StopIteration:
            break


# -------------------------------------------------------------------------- MAIN
while True:
    print('Running bot...')
    status = retrieve_text(STATUS_NAME)
    api_one = retrieve_text('api_1.txt')
    api_two = retrieve_text('api_2.txt')
    if api_one == api_two == 'ON':
        if status == 'ONE':
            print('[USING FIRST KEY]')
            reply_tt(api_1,'ONE')
        else:
            print('[USING SECOND KEY]')
            reply_tt(api_2,'TWO')
    else:
        if api_one == 'OFF' and api_two == 'ON':
            print('[USING SECOND KEY]')
            reply_tt(api_2, 'TWO')
        elif api_one == 'ON' and api_two == 'OFF':
            print('[USING FIRST KEY]')
            reply_tt(api_1, 'ONE')
        else:
            while True:
                print('[ALL KEYS USED]')
                for i in burros:
                    print(i, end=' ')
                print('Last seen id: ' + str(retrieve_text(FILE_NAME)))
                time.sleep(100)
    print('Sleeping for 60 seconds...')
    time.sleep(60)