from os import access
import firebase_admin
import time
import datetime
import tweepy
import constant
from media import Media
from firebase_admin import credentials,firestore

def user_on_snapshot(document_snapshot, changes, read_time):
    doc = document_snapshot
    # print(u'{} => {}'.format(doc.id, doc.to_dict()))
    print(doc[0].id)

def main():
    media = Media()
    cred = credentials.Certificate("firebase-admin.json")
    app = firebase_admin.initialize_app(cred)
    client = firestore.client(app)
    schedules = client.collection('schedules')
    docs = schedules.list_documents()
    for i in docs:
        schedule = i.get()
        date = datetime.datetime.strptime(schedule.get('time'), "%d-%m-%Y %H:%M:%S")
        current_time = time.time()
        timestamp = datetime.datetime.timestamp(date)
        if timestamp <= current_time:
            # schedule is done
            user_id = schedule.get('user_id')
            user_ref = client.document(f'users/{user_id}')
            user_snapshot = user_ref.get()
            # uname = user.get('asd')
            twitter_account_snapshot = client.document(f'users/{user_id}/accounts/twitter').get()
            twitter_account = twitter_account_snapshot.to_dict()
            access_token = twitter_account['access_token']
            access_secret = twitter_account['access_secret']
            if access_secret != None and access_token != None:
                # print(f"Access secret = {access_secret}, access_token = {access_token}")
                description = schedule.get('description')
                image_urls = schedule.get('image')
                auth = tweepy.OAuthHandler(constant.CONSUMER_KEY,constant.CONSUMER_SECRET)
                auth.set_access_token(access_token,access_secret)
                api = tweepy.API(auth)
                # print(f"url = {image_url[0]}")
                # 
                media_ids = []
                for idx,url in enumerate(image_urls):
                    media.download_image(url,idx)
                    upload = api.media_upload(f'download{idx}.png')
                    media_ids.append(upload.media_id)
                api.update_status(description,media_ids=media_ids)
                schedule_type = schedule.get('type')
                if schedule_type =='Once':
                    i.delete()
                elif schedule_type == 'Daily':
                    pass
                


    


if __name__=="__main__":
    main()