# StartMeUp_Instances_byOne
#
# This lambda script is triggered by a CloudWatch Event, startGroupByInstance.
# Every evening a separate lambda script is launched on a schedule to stop
# all non-essential instances.
# 
# This script will turn on all instances with a LaunchGroup tag that matches 
# a single instance which has been changed to the running state.
#
# To start all instances in a LaunchGroup, 
# start one of the instances in the LaunchGroup and wait about 5 minutes.
# 
# Costs to run: approx. $0.02/month
# https://s3.amazonaws.com/lambda-tools/pricing-calculator.html
# 150 executions per month * 128 MB Memory * 60000 ms Execution Time
# 
# Problems: talk to chrisj
# ======================================

# test system
# this is what the event object looks like (see below)
# it is configured in the test event object with a specific instance-id
# change that to test a different instance-id with a different LaunchGroup

# {  "version": "0",
#   "id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#   "detail-type": "EC2 Instance State-change Notification",
#   "source": "aws.ec2",
#   "account": "999999999999999",
#   "time": "2015-11-11T21:30:34Z",
#   "region": "us-east-1",
#   "resources": [
#     "arn:aws:ec2:us-east-1:123456789012:instance/i-abcd1111"
#   ],
#   "detail": {
#     "instance-id": "i-0aad9474",  # <---------- chg this
#     "state": "running"
#   }
# }
# ======================================

import boto3
import logging
import json

ec2 = boto3.resource('ec2')

def get_instance_LaunchGroup(iid):
    # When given an instance ID as str e.g. 'i-1234567', 
    # return the instance LaunchGroup.
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(iid)
    thisTag = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'LaunchGroup':
            thisTag = tags["Value"]
    return thisTag

# this is the entry point for the cloudwatch trigger
def lambda_handler(event, context):

    # get the instance id that triggered the event
    thisInstanceID = event['detail']['instance-id']
    print("instance-id: " + thisInstanceID)

    # get the LaunchGroup tag value of the thisInstanceID
    thisLaunchGroup = get_instance_LaunchGroup(thisInstanceID)
    print("LaunchGroup: " + thisLaunchGroup)
    if thisLaunchGroup == '':
        print("No LaunchGroup associated with this InstanceID - ending lambda function")
        return

    # set the filters
    filters = [{
            'Name': 'tag:LaunchGroup',
            'Values': [thisLaunchGroup] 
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]

    # get the instances based on the filter, thisLaunchGroup and stopped
    instances = ec2.instances.filter(Filters=filters)

    # get the stopped instance IDs
    stoppedInstances = [instance.id for instance in instances]

    # make sure there are some instances not already started
    if len(stoppedInstances) > 0:
        startingUp = ec2.instances.filter(InstanceIds=stoppedInstances).start()

    print ("Finished launching all instances for tag: " + thisLaunchGroup)
shareimprove this answer