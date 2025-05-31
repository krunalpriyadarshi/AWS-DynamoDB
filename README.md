
# AWS DynamoDB with Lambda: CSV Processing Pipeline

This project demonstrates a **serverless data processing pipeline** using AWS services. It processes large CSV files uploaded to an **S3 bucket**, parses their content, and stores the data into **DynamoDB**.  
It also covers **CloudWatch monitoring** and **batch writing** for efficient handling of big data.

## 📁 Project Structure
```
aws-dynamodb-lambda-csv/
├── lambda_function.py      # Lambda handler code (S3 → DynamoDB)
├── sample_data.csv         # Test CSV file for S3 upload
└── README.md               # Project documentation
```

## 🚀 Step 1: Setup AWS Services
1. **Create S3 Bucket**: For uploading CSV files (e.g., `big-csv-uploads-project`).
2. **Create DynamoDB Table**:  
   - Partition Key: `RecordID` (String)
3. **Create Lambda Function**:
   - Runtime: Python 3.x
   - Attach IAM Role with S3 and DynamoDB permissions
4. **Configure S3 Event Trigger**:  
   - Event: `ObjectCreated` (All)

## 📝 Step 2: Write Sample CSV File
Create a simple `sample_data.csv`:
```csv
RecordID,Name,Timestamp,Value
1,John,2023-09-01T12:00:00Z,100
2,Jane,2023-09-01T12:05:00Z,200
3,Bob,2023-09-01T12:10:00Z,300
```
Upload this file to the S3 bucket to test the Lambda trigger.

## 🏗 Step 3: Lambda Handler
Implemented Lambda function that:
- Gets CSV from S3 using `boto3`
- Parses CSV content
- Inserts each row into DynamoDB

## 🔍 Step 4: CloudWatch Monitoring
- Logs Lambda execution details (START, END, REPORT)
- Prints logs for processed files and records
- Tracks metrics: invocations, errors, duration, throttling
- Optionally, configure CloudWatch alarms for error monitoring

## ⚡ Step 5: Batch Processing
Enhanced the Lambda to:
- Use `batch_write_item` for efficient writes (up to 25 items/batch)
- Handle large CSV files (2+ GB) by writing in batches
- Retry unprocessed items due to throttling
- Improve performance and cost efficiency

