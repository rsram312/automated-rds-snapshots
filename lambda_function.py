""" Lambda function to backup database.
"""
import boto3
import os
from datetime import date
from botocore.exceptions import ClientError

rds = boto3.client('rds')
sns = boto3.client('sns')

"""
    Environment variables are being read.
"""
db_instance_identifier = os.environ['dbInstanceIdentifier']
owner_contact = os.environ['ownerContact']
topic_arn = os.environ['topicArn']

def lambda_handler(event, context):

    current_date = date.today()
    current_date_update='db-backup-' + str(current_date)
    try:
        response = rds.create_db_snapshot(
            DBSnapshotIdentifier=current_date_update,
            DBInstanceIdentifier=db_instance_identifier,
            Tags=[
                {
                    'Key': 'OwnerContact',
                    'Value': owner_contact
                },
            ]
        )
        sns_publish("RDS Daily backup successfully completed", "Success")
        print(response)
    except ClientError as ex:
        print("Failed")
        sns_publish("RDS Daily backup failed. Check Cloudwatch logs", "Failed")
        raise ex


def sns_publish(message, subject):
     """Publish SNS message.

    Arguments:
        message {string} -- Message that needs to be published to subscribers.
        subject -- Title of the SNS notification.

    Returns:
        none
    """
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='Database Daily backup: ' + subject
    )
