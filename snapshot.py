import boto3
from datetime import datetime

ec2 = boto3.client('ec2', region_name='ap-south-1')

VOLUME_ID = 'your-volume-id'   # replace this

def create_snapshot():
    response = ec2.create_snapshot(
       VOLUME_ID = 'vol-0536085b80fcdd726'
        Description=f"Automated snapshot {datetime.now()}"
    )
    print("Snapshot created:", response['SnapshotId'])


def delete_old_snapshots():
    snapshots = ec2.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [VOLUME_ID]}],
        OwnerIds=['self']
    )['Snapshots']

    # Sort snapshots by StartTime
    snapshots = sorted(snapshots, key=lambda x: x['StartTime'], reverse=True)

    # Keep only latest 5
    old_snapshots = snapshots[5:]

    for snap in old_snapshots:
        print("Deleting:", snap['SnapshotId'])
        ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])


if __name__ == "__main__":
    create_snapshot()
    delete_old_snapshots()