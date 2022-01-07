import tweepy
import constant
import time

class Twitter :
    def __init__(self):
        print("Init twitter api")

    @staticmethod
    def init_tweepy(access_key,access_secret):
        api = tweepy.OAuthHandler(constant.CONSUMER_KEY, constant.CONSUMER_SECRET)
        api.set_access_token(access_key,access_secret)
        return tweepy.API(api)

    def delete_dm(self, id):
        print("Delete dm with id "+ str(id))
        try:
            api = self.init_tweepy()
            api.destroy_direct_message(id)
            time.sleep(30)
        except Exception as ex:
            print(ex)
            time.sleep(30)
            pass


    def read_dm(self):
        print("Get dms..")
        dms = list()
        try:
            api = self.init_tweepy()
            dm = api.list_direct_messages()
            for x in range(len(dm)):
                sender_id = dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                d = dict(message = message, sender_id = sender_id, id= dm[x].id)
                dms.append(d)
                dms.reverse()
            print(str(len(dms))+ " collected")
            time.sleep(60)
            return dms

        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def post_tweet(self):
        print("Uploading..")
        api = self.init_tweepy()
        api.update_with_media(filename="ready.png")

    def get_user_screen_name(self, id):
        print("Getting username")
        api = self.init_tweepy()
        user = api.get_user(id)
        return user.screen_name