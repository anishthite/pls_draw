import tweepy
import logging
from config import create_api
import time
from io import BytesIO
from craiyon_api import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is None:
            logger.info('continue')
            continue
        
        prompt = api.get_status(tweet.in_reply_to_status_id).text
        logger.info(str(prompt))
        logger.info('Generating...')
        img = generate(prompt)

        b = BytesIO()
        img.save(b, "PNG")
        b.seek(0)

        ret = api.media_upload(filename="dummy_string", file=b)
        logger.info('uploading status...')
        api.update_status(
            status="generated img:",
            media_ids=[ret.media_id_string],
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True
        )
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
