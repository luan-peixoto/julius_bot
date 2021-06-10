# coding=utf-8
import tweepy
import time
import datetime
from os import environ
from random import randint

# --------------------------------------------------------------------------  KEYS

def auth(ck, cs, ak, ass):
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(ak, ass)
    api= tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


api_0 = auth(environ['CONSUMER_KEY_0'], environ['CONSUMER_SECRET_0'], environ['ACCESS_KEY_0'], environ['ACCESS_SECRET_0'])

api_1 = auth(environ['CONSUMER_KEY_1'], environ['CONSUMER_SECRET_1'], environ['ACCESS_KEY_1'], environ['ACCESS_SECRET_1'])

api_2 = auth(environ['CONSUMER_KEY_2'], environ['CONSUMER_SECRET_2'], environ['ACCESS_KEY_2'], environ['ACCESS_SECRET_2'])

api_3 = auth(environ['CONSUMER_KEY_3'], environ['CONSUMER_SECRET_3'], environ['ACCESS_KEY_3'], environ['ACCESS_SECRET_3'])

api_4 = auth(environ['CONSUMER_KEY_4'], environ['CONSUMER_SECRET_4'], environ['ACCESS_KEY_4'], environ['ACCESS_SECRET_4'])

api_5 = auth(environ['CONSUMER_KEY_5'], environ['CONSUMER_SECRET_5'], environ['ACCESS_KEY_5'], environ['ACCESS_SECRET_5'])

api_6 = auth(environ['CONSUMER_KEY_6'], environ['CONSUMER_SECRET_6'], environ['ACCESS_KEY_6'], environ['ACCESS_SECRET_6'])

api_7 = auth(environ['CONSUMER_KEY_7'], environ['CONSUMER_SECRET_7'], environ['ACCESS_KEY_7'], environ['ACCESS_SECRET_7'])

api_8 = auth(environ['CONSUMER_KEY_8'], environ['CONSUMER_SECRET_8'], environ['ACCESS_KEY_8'], environ['ACCESS_SECRET_8'])

api_9 = auth(environ['CONSUMER_KEY_9'], environ['CONSUMER_SECRET_9'], environ['ACCESS_KEY_9'], environ['ACCESS_SECRET_9'])


# -------------------------------------------------------------------------- SEARCH
livres = ['aetheryel', 'luanpxoto']
pesquisa = 'julius?'
pesquisa_f = 'julius?!'
tweet_number = 20
filter = ['en', 'ja', 'fr', 'it', 'ru', 'in', 'es', 'ceb', 'de', 'tl', 'da']

# -------------------------------------------------------------------------- REPLIES
the_reply = ['Esse tweet custou %i centavos.',
             'Esse tweet custou 1 dólar e %i centavos.',
             'Esse tweet custou %i dólares e %i centavos.',
             'Se você não comprar nada, o desconto é maior.',
             'Aceita vale-refeição?',
             'Pra que você vai sair pra relaxar se você pode relaxar em casa e de graça?',
             'Eu me lembro dos primeiros 35 dólares que eu achei. Era 17 horas, em frente ao banco, fazia 27 graus, eu achei duas notas de 10, duas de 5, três moedas de 1 dólar, quatro de 25, e 100 moedas de 1 centavo. E uma delas era canadense.',
             'Quer saber o que é mágica? Eu tenho dois empregos, trabalho sete dias por semana e todo dia meu dinheiro desaparece.',
             'Eu ganhei meus primeiros 30 dólares quando tinha 20 anos, e ainda não gastei tudo.',
             'O @%s está te devendo %i centavos.',
             'O @%s está te devendo 1 dólar e %i centavos.',
             'O @%s está te devendo %i dólares e %i centavos.']

# -------------------------------------------------------------------------- CHECK SPAM
burros = []


def time_checker(tweet_id, tweet_created_at, user_screen_name, search_text):
    time_spam = datetime.timedelta(0, 0, 0, 0, 2, 0, 0)
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


# -------------------------------------------------------------------------- POSTS
def reply_tt(api_n):
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
                    if check and (tweet.user.screen_name not in livres):
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
                                    '@' + tweet.user.screen_name + ' ' + the_reply[9] % (
                                        main_tweet.user.screen_name, randint(15, 99)), in_reply_to_status_id=tweet.id)
                            elif 1 < resp < 3:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[10] % (
                                        main_tweet.user.screen_name, randint(15, 99)), in_reply_to_status_id=tweet.id)
                            else:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[11] % (
                                        main_tweet.user.screen_name, randint(2, 8), randint(15, 99)),
                                    in_reply_to_status_id=tweet.id)
                            print('Reply sent. Sleeping for 60~70 seconds.')
                            time.sleep(randint(60, 70))
                        else:
                            resp = randint(0, 25)
                            api_n.create_favorite(tweet.id)
                            if resp < 9:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[0] % (randint(15, 99)),
                                    in_reply_to_status_id=tweet.id)
                            elif 15 > resp > 8:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[1] % (randint(15, 99)),
                                    in_reply_to_status_id=tweet.id)
                            elif 20 > resp > 14:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[2] % (
                                    randint(2, 8), randint(15, 99)),
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 20:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[3],
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 21:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[4],
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 22:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[5],
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 23:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[6],
                                    in_reply_to_status_id=tweet.id)
                            elif resp == 24:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[7],
                                    in_reply_to_status_id=tweet.id)
                            else:
                                api_n.update_status(
                                    '@' + tweet.user.screen_name + ' ' + the_reply[8],
                                    in_reply_to_status_id=tweet.id)
                            print('Reply sent. Sleeping for 60~70 seconds.')
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
                return 0

        except StopIteration:
            break
    return 1


# -------------------------------------------------------------------------- MAIN

keys = [api_1, api_2, api_3, api_4, api_5, api_6, api_7, api_8, api_9]
nums = ['FIRST','SECOND','THIRD','FOURTH','FIFTH','SIXTH', 'SEVENTH', 'EIGHT', 'NINETH']
current = 0
size = 9
print('Running bot...')
while size > 0:
        print('[USING %s KEY]' %nums[current])
        r = reply_tt(keys[current])
        if r == 1:
            if current == size - 1:
                current = 0
            else:
                current += 1
        else:
            if current == size - 1:
                size -= 1
                current = 0
            else:
                while current != size - 1:
                    keys[current] = keys[current + 1]
                    current += 1
                size -= 1
        print('Cursor search ended. Sleeping for 60 seconds...')
        time.sleep(60)
while True:
    print('[ALL KEYS USED]')
    print('Last seen id: ' + str(retrieve_text(FILE_NAME)))
    time.sleep(100)
