import os
import json
import hashlib
import psycopg2
import subprocess

#Simple hashing function for the device_id and ip fields
def get_hash(input_string):
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode('utf-8'))
    return hash_object.hexdigest()

##This function is written to handle the app version which is coming to us as a float value, however the SQL schema is expecting a an integer value for the app_version column.
#The function will convert the version string to a float and then return the float value.
def version_to_float(version_str):
    parts = version_str.split('.')
    if len(parts) >= 2:  
        if int(parts[2]) > 0:
            print(float(f"{parts[0]}.{parts[1]}{parts[2]}"))
            return float(f"{parts[0]}.{parts[1]}{parts[2]}")
        
        print(float(f"{parts[0]}.{parts[1]}"))
        return float(f"{parts[0]}.{parts[1]}")

    return float(parts[0]) 

def main():
    try:
        # Receiving the message from the local SQS queue
        command = "awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.stdout:
            output = json.loads(result.stdout)
            # Processing the message if it exists
            if 'Messages' in output and output['Messages']:
                message_body = json.loads(output['Messages'][0]['Body'])
                
                message_body['device_id'] = get_hash(message_body['device_id'])
                message_body['ip'] = get_hash(message_body['ip'])
                # Database operations
                try:
                    with psycopg2.connect(
                        host="localhost",  
                        database="postgres",  
                        user="postgres",  
                        password="postgres"
                    ) as conn:
                        with conn.cursor() as cur:
                            insert_sql = """
                            INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
                            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
                            """
                            cur.execute(insert_sql, (
                                message_body['user_id'],
                                message_body['device_type'],
                                message_body['ip'],
                                message_body['device_id'],
                                message_body['locale'],
                                version_to_float(message_body['app_version'])
                            ))
                            conn.commit()

                    print("Data inserted successfully!")
                except (Exception, psycopg2.DatabaseError) as error:
                    print("Failed to execute database operations: ", error)
            else:
                print("No messages to process.")
        else:
            print("No output from subprocess.")
    except Exception as e:
        print("Failed to execute subprocess: ", e)

if __name__ == "__main__":
    main()
