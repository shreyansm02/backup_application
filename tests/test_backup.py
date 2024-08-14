import requests

def test_backup_service():
    # Create a backup job
    response = requests.post("http://127.0.0.1:8000/backup/nfs/", json={
        "source": "/tmp/test_source",
        "local_path": "/tmp/test_target",
        "nfs_path": "nfs_mount_path"
    })
    if response.status_code != 200:
        print("Failed to create backup job")
        return

    job_id = response.json()["id"]
    print(f"Created Backup Job {job_id}")

    # Start the backup job
    response = requests.post("http://127.0.0.1:8000/backup_jobs/", json={
        "job_id": job_id,
        "use_nfs": True,
        "nfs_path": "/tmp/test_target"
    })
    if response.status_code != 200:
        print(f"Failed to start backup job: {response.json()['detail']}")
        return
    print(f"Started Backup Job {job_id}")

    # Check the status of the backup job
    response = requests.get(f"http://127.0.0.1:8000/backup/{job_id}/status")
    if response.status_code != 200:
        print(f"Failed to get job status: {response.json()['detail']}")
        return

    job_status = response.json()
    print(f"Backup Job {job_id} Status: {job_status['status']}")
    if job_status.get('error_message'):
        print(f"Error: {job_status['error_message']}")

if __name__ == "__main__":
    test_backup_service()