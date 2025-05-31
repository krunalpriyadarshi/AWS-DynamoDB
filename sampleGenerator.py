import csv
import random
import string

def generate_sample_csv(file_name, num_rows):
    with open(file_name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(['RecordID', 'Name', 'Timestamp', 'Value'])

        for i in range(num_rows):
            record_id = f"ID{i}"
            name = ''.join(random.choices(string.ascii_letters, k=5))
            timestamp = f"2023-09-{random.randint(1,30)}"
            value = random.randint(1, 100)
            writer.writerow([record_id, name, timestamp, value])

# Generate a small CSV with 100 rows
generate_sample_csv('sample_data.csv', 100)
