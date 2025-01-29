import boto3
import os

# Initialize AWS Clients
ec2 = boto3.client('ec2')
sns = boto3.client('sns')

# Set SNS Topic ARN (Replace with your SNS Topic ARN)
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:EBS-Snapshot-Alerts"

def lambda_handler(event, context):
    # Get all EBS snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])
    
    # Get all active EC2 instance IDs
    instances_response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    active_instance_ids = set()

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    # Iterate through snapshots and delete if not in use
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            send_sns_notification(snapshot_id, "not attached to any volume", "Deleting snapshot")
            ec2.delete_snapshot(SnapshotId=snapshot_id)
        else:
            try:
                volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                if not volume_response['Volumes'][0]['Attachments']:
                    send_sns_notification(snapshot_id, "taken from an unattached volume", "Deleting snapshot")
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
            except ec2.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    send_sns_notification(snapshot_id, "volume was deleted", "Deleting snapshot")
                    ec2.delete_snapshot(SnapshotId=snapshot_id)

def send_sns_notification(snapshot_id, reason, action):
    message = f"Snapshot ID: {snapshot_id} is being deleted.\nReason: {reason}\nAction: {action}"
    sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="EBS Snapshot Cleanup Notification")
