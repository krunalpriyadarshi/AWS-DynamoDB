import boto3
import csv
import io

dynamodb = boto3.resource('dynamodb')
table_name = 'YourDynamoDBTable'  # Change to your table name
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Get object from S3
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(content))

    table = dynamodb.Table(table_name)
    
    for row in csv_reader:
        item = {
            'RecordID': row['RecordID'],
            'Name': row['Name'],
            'Timestamp': row['Timestamp'],
            'Value': int(row['Value'])
        }
        # Put item into DynamoDB
        table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': f'Successfully processed {key} and added to {table_name}.'
    }
