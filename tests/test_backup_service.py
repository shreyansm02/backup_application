from app.services.backup_service import BackupService
from app.infrastructure.nfs_client import MockNFSClient

def test_backup_service():
    # Initialize BackupService with mock credentials and bucket name
    backup_service = BackupService(
        aws_access_key_id="mock_access_key",
        aws_secret_access_key="mock_secret_key",
        region_name="us-east-2",
        bucket_name="mock_bucket"
    )

    # Create a backup job
    source_directory = "/tmp/test_source"
    target_directory = "/tmp/test_target"
    job_id = backup_service.create_backup_job(source=source_directory, target=target_directory)
    
    # Start the backup job with NFS (using MockNFSClient)
    backup_service.start_backup_job(job_id=job_id, use_nfs=True, nfs_path=target_directory)

    # Check the status of the backup job
    job_status = backup_service.get_job_status(job_id)
    print(f"Backup Job {job_id} Status: {job_status.status}")
    if job_status.error_message:
        print(f"Error: {job_status.error_message}")

if __name__ == "__main__":
    test_backup_service()

