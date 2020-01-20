# Amazon RDS Snapshots

RDS Automated snapshots can be set to a max retention of 35 days, which means AWS deletes your snapshot when it is 35 days old. While you can create a manual snapshot from the AWS console, unfortunately there is no straight forward method to automate the creation of manual snapshots from AWS console. Below is one of the designs to automate creation of manual snapshots:

## Pre-Requisites

Create an IAM Role with the following permissions to the Lambda Service

* Take new RDS snapshots using CreateDBSnapshot and ModifyDBSnapshot API calls.
* Add/Create Lambda basic execution role policy to give CloudWatch events access to trigger Lambda.
* SNS Publish access to your SNS topic.


## How it works

The CloudWatch event is scheduled to run on a daily basis and Lambda function is added as target to be triggered. The Lambda function is python based and uses Boto library to make calls to AWS Resources. The Lambda function uses the `create_db_snapshot` API call to create RDS snapshots. On completion of the job, the Lambda would then send the SNS notifications based on whether it was a success or failure.
