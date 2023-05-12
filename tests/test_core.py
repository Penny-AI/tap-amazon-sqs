"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import json

from singer_sdk.testing import get_tap_test_class
from singer_sdk.testing import get_standard_tap_tests

from moto import mock_iam, mock_sqs
from moto.core import set_initial_no_auth_action_count
import boto3

from tap_amazon_sqs.tap import Tapamazonsqs


def create_config(queue_url, access_key, secret_key, queue_region, delete_message):
    return {
        "delete_messages": delete_message,
        "queue_url": queue_url,
        "region": queue_region,
        "access_key": access_key,
        "secret_key": secret_key,
        "max_wait_time": 5,
        "visibility_timeout": 120,
    }


@mock_iam
def create_user_with_all_permissions():
    client = boto3.client("iam", region_name="eu-west-1")
    client.create_user(UserName="test_user1")

    policy_document = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Action": ["sqs:*"], "Resource": "*"}],
    }

    client.put_user_policy(
        UserName="test_user1",
        PolicyName="policy1",
        PolicyDocument=json.dumps(policy_document),
    )

    return client.create_access_key(UserName="test_user1")["AccessKey"]


@set_initial_no_auth_action_count(3)
@mock_sqs
@mock_iam
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""

    # Create User
    user = create_user_with_all_permissions()
    # Create Queue
    queue_name = "amazon-sqs-mock-queue"
    queue_region = "eu-west-1"
    client = boto3.client(
        "sqs", aws_access_key_id=user["AccessKeyId"], aws_secret_access_key=user["SecretAccessKey"], region_name=queue_region
    )
    queue_url = client.create_queue(QueueName=queue_name)["QueueUrl"]
    # Create config
    config = create_config(queue_url, user["AccessKeyId"], user["SecretAccessKey"], queue_region, False)

    tests = get_standard_tap_tests(Tapamazonsqs, config=config)
    for test in tests:
        test()
