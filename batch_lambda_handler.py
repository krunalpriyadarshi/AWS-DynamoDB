import boto3
import csv
import io

dynamodb = boto3.client('dynamodb')  # Note: Using client for batch_write_item
s3_client = boto3.client('s3')

table_name = 'YourDynamoDBTable'

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(content))
    
    items = []
    for row in csv_reader:
        item = {
            'PutRequest': {
                'Item': {
                    'RecordID': {'S': row['RecordID']},
                    'Name': {'S': row['Name']},
                    'Timestamp': {'S': row['Timestamp']},
                    'Value': {'N': str(row['Value'])}
                }
            }
        }
        items.append(item)
        
        # If we reach batch size limit, write the batch
        if len(items) == 25:
            write_batch(items)
            items = []
    
    # Write any remaining items
    if items:
        write_batch(items)
        
    return {
        'statusCode': 200,
        'body': f'Successfully processed {key} and added to {table_name} in batches.'
    }

def write_batch(items):
    request_items = {table_name: items}
    response = dynamodb.batch_write_item(RequestItems=request_items)
    unprocessed = response.get('UnprocessedItems', {})
    
    # Retry unprocessed items (if any)
    while unprocessed:
        print(f"Retrying {len(unprocessed[table_name])} unprocessed items...")
        response = dynamodb.batch_write_item(RequestItems=unprocessed)
        unprocessed = response.get('UnprocessedItems', {})
