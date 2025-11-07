import os
import json
import boto3

import datetime
from dto.fake_account import FakeAccount
from dto.group import GroupDTO
from scrapper import Scrapper


def upload_to_s3(data, bucket_name, key):
    s3_client = boto3.client('s3')
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(data))


def main():
    fake_account = json.loads(os.getenv('FAKE_ACCOUNT', '{}'))
    keywords = json.loads(os.getenv('KEYWORDS', '[]'))
    s3_bucket = os.getenv('S3_BUCKET', 'scrapper-leadtrek')
    result_key = os.getenv('RESULT_KEY', f"posts/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")

    groups = [GroupDTO(**group) for group in fake_account.pop("groups")]
    account = FakeAccount(**fake_account, groups=groups)

    scrapper = Scrapper()
    recent_posts = scrapper.get_new_posts(account)

    # Upload results to S3
    upload_to_s3(recent_posts, s3_bucket, result_key)


if __name__ == "__main__":
    main()
