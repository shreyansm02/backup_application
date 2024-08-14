# backup_application

![Untitled Diagram drawio](https://github.com/user-attachments/assets/c60e0452-fb31-4fc5-b734-a2c6d103af43)

A FastAPI application designed to manage and execute backup jobs. The application supports creating users, configuring backup settings, and handling the backup process while storing related metadata. This document provides an overview of the database schema, relationships, and the sequence of operations needed to perform a backup.

Database Schema Relationships:
User Table

    Primary Key: id
    Relationships:
        A user can have multiple backup jobs, establishing a one-to-many relationship.
        This relationship is facilitated by the owner_id foreign key in the BackupJob table.

BackupJob Table

    Primary Key: id
    Foreign Key: owner_id references users.id
    Relationships:
        Each backup job is associated with a single user (owner).
        Backup jobs can have associated metadata stored in the BackupMetadata table.

Configuration Table

    Primary Key: id
    Purpose: Stores configuration data for the application. This table is not directly linked to any other table.

BackupMetadata Table

    Primary Key: id
    Foreign Key: backup_job_id references backup_jobs.id
    Relationships:
        Each record in this table corresponds to metadata for a single backup job.

FastAPI Endpoints and Sequence of Operations:
1. Create a User
    Endpoint: POST /users/
    Description: This step creates a new user who can own backup jobs.
    curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"username": "user1", "email": "user1@example.com"}'
   
2. Create a Configuration (Optional)
    Endpoint: POST /configurations/
    Description: Use this endpoint to store configuration settings. This step is not directly tied to the backup job process but is useful for application settings.
    curl -X POST "http://localhost:8000/configurations/" -H "Content-Type: application/json" -d '{"key": "nfs_mount_path", "value": "/mnt/nfs"}'

3. Create a Backup Job
   Endpoint: POST /backup_jobs/
   Description: Initializes a new backup job associated with the created user.
   curl -X POST "http://localhost:8000/backup_jobs/" -H "Content-Type: application/json" -d '{"source_path": "/data/source", "target_path": "/data/target", "owner_id": 1}'

4. Start a Backup Job

    Endpoint: POST /backup/ or POST /backup/nfs/
    Description: Use POST /backup/ to start a regular backup job, optionally uploading to S3. Use POST /backup/nfs/ to start a backup job using NFS.
    curl -X POST "http://localhost:8000/backup/" -H "Content-Type: application/json" -d '{"source": "/data/source", "target": "/data/target", "upload_to_s3": true, "s3_key": "backup_key"}'

5.  Get Backup Status

    Endpoint: GET /backup/{job_id}/status/
    Description: Retrieves the status of a backup job, showing the current state and any error messages related to the job.
    curl -X GET "http://localhost:8000/backup/1/status/"

6. Create Backup Metadata (Optional)

    Endpoint: POST /backup_metadata/
    Description: Adds additional metadata for a backup job, such as size and duration. This operation is typically done after the backup is complete.
    curl -X POST "http://localhost:8000/backup_metadata/" -H "Content-Type: application/json" -d '{"backup_job_id": 1, "size": 1024, "duration": 30, "details": "Backup completed successfully."}'

   
