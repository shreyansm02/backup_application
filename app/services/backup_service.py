from app.core.models import BackupJob
from app.infrastructure.s3_storage import S3Storage
from app.infrastructure.nfs_client import NFSClient, MockNFSClient
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm 
from sqlalchemy.orm import Session
from . import crud
from app.api.schema import BackupJobCreate

class BackupService:
    def __init__(self, db: Session, aws_access_key_id: str, aws_secret_access_key: str, region_name: str, bucket_name: str):
        self.db = db
        self.s3_storage = S3Storage(aws_access_key_id, aws_secret_access_key, region_name, bucket_name)
        self.nfs_client = NFSClient()
        # self.nfs_client = MockNFSClient()  # Use MockNFSClient for testing

    def create_backup_job(self, source: str, target: str) -> BackupJob:
        owner_id = crud.get_owner_id(self.db)
        print(f"Owner ID: {owner_id}")
        backup_job = BackupJobCreate(
            source_path=source,
            target_path=target,
            status='pending',
            owner_id=owner_id
            )
        return crud.create_backup_job(self.db, backup_job)

    def start_backup_job(self, job_id: int, upload_to_s3: bool = False, s3_key: str = None, use_nfs: bool = False, nfs_path: str = None):
        job = crud.get_backup_job_by_id(self.db, job_id)
        if not job:
            raise ValueError("Job not found")

        def backup():
            try:
                job.status = 'in_progress'
                # Backup to NFS if specified
                if use_nfs and nfs_path:
                    local_mount_path = job.target_path
                    self.nfs_client.mount(nfs_path, local_mount_path)
                    self.backup_directory(job.source_path, local_mount_path)
                    # self.nfs_client.copy_file(job.source_path, local_mount_path)
                    self.nfs_client.unmount(local_mount_path)
                else:
                    # Simulate local file copy (if needed)
                    if not upload_to_s3:
                        destination = os.path.join(job.target_path, os.path.basename(job.source_path))
                        shutil.copy2(job.source_path, destination)

                # Optionally upload to S3
                if upload_to_s3 and s3_key:
                    self.s3_storage.upload_file(job.source_path, s3_key)

                job.status = 'completed'
            except Exception as e:
                job.status = 'failed'
                job.error_message = str(e)

            self.db.commit()

        backup()

    def backup_directory(self, source: str, target: str):
        """Backup a directory to an NFS share."""
        # Collect all files to be copied
        files_to_copy = []
        for root, dirs, files in os.walk(source):
            for name in files:
                file_path = os.path.join(root, name)
                relative_path = os.path.relpath(file_path, source)
                target_path = os.path.join(target, relative_path)
                files_to_copy.append((file_path, target_path))

        # Use ThreadPoolExecutor to copy files concurrently with progress tracking
        with ThreadPoolExecutor() as executor, tqdm(total=len(files_to_copy), desc="Copying files", unit="file") as progress_bar:
            futures = {executor.submit(self.nfs_client.copy_file, src, tgt): (src, tgt) for src, tgt in files_to_copy}
            
            for future in as_completed(futures):
                try:
                    future.result()
                    progress_bar.update(1)
                except Exception as e:
                    print(f"Error during backup: {e}")

    def get_job_status(self, job_id: int) -> BackupJob:
        return crud.get_backup_job_by_id(self.db, job_id)
