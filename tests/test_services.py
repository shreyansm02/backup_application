from app.services.backup_service import BackupService

def test_backup_to_s3_multipart():
    # Setup mock credentials and bucket
    aws_access_key_id = 'your-access-key'
    aws_secret_access_key = 'your-secret-key'
    region_name = 'us-east-1'
    bucket_name = 'bucket-name'
    
    backup_service = BackupService(aws_access_key_id, aws_secret_access_key, region_name, bucket_name)

    # Create a mock job
    source = '/home/shreyans/run.sh'
    target = '/home/shreyans/Pictures'
    s3_key = 'backups/run2.sh'

    job_id = backup_service.create_backup_job(source, target)

    # Test uploading to S3 with multipart
    backup_service.start_backup_job(job_id, upload_to_s3=True, s3_key=s3_key)

    # Assert job status
    job = backup_service.get_job_status(job_id)
    assert job.status == 'completed'