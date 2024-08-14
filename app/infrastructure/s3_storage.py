import os
import boto3
from concurrent.futures import ThreadPoolExecutor

class S3Storage:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str, bucket_name: str):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.bucket_name = bucket_name

    def upload_file(self, file_path: str, s3_key: str, chunk_size_mb: int = 50):
        """Upload a file to S3 using multipart upload."""
        file_size = os.path.getsize(file_path)
        part_size = chunk_size_mb * 1024 * 1024

        if file_size < part_size:
            self.s3.upload_file(file_path, self.bucket_name, s3_key)
            print(f"Uploaded {file_path} to s3://{self.bucket_name}/{s3_key} in a single upload.")
            return

        multipart_upload = self.s3.create_multipart_upload(Bucket=self.bucket_name, Key=s3_key)
        upload_id = multipart_upload['UploadId']
        parts = []

        try:
            with open(file_path, 'rb') as file:
                part_number = 1
                offset = 0
                with ThreadPoolExecutor(max_workers=4) as executor:
                    futures = []
                    while offset < file_size:
                        end = min(offset + part_size, file_size)
                        data = file.read(end - offset)
                        future = executor.submit(self.upload_part, file_path, s3_key, upload_id, part_number, data)
                        futures.append((future, part_number))
                        offset = end
                        part_number += 1

                    for future, part_number in futures:
                        response = future.result()
                        parts.append({
                            'ETag': response['ETag'],
                            'PartNumber': part_number
                        })

            self.s3.complete_multipart_upload(
                Bucket=self.bucket_name,
                Key=s3_key,
                MultipartUpload={'Parts': parts},
                UploadId=upload_id
            )
            print(f"Successfully uploaded {file_path} to s3://{self.bucket_name}/{s3_key} using multipart upload.")
        except Exception as e:
            self.s3.abort_multipart_upload(Bucket=self.bucket_name, Key=s3_key, UploadId=upload_id)
            print(f"Failed to upload {file_path} due to {e}")

    def upload_part(self, file_path, s3_key, upload_id, part_number, data):
        response = self.s3.upload_part(
            Bucket=self.bucket_name,
            Key=s3_key,
            PartNumber=part_number,
            UploadId=upload_id,
            Body=data
        )
        return response
    
 