from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.backup_service import BackupService
from app.api import schema
from app.api.schema import BackupRequest, NFSBackupRequest
from app.infrastructure.nfs_client import NFSClient

from app.services import crud
from app.core.database import SessionLocal

router = APIRouter()

# Dependency to provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_backup_service(db: Session = Depends(get_db)) -> BackupService:
    return BackupService(
        aws_access_key_id="your-access-key",
        aws_secret_access_key="your-secret-key",
        region_name="us-east-1",
        bucket_name="bucket-name",
        db=db
    )

@router.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.post("/configurations/", response_model=schema.Configuration)
def create_configuration(configuration: schema.ConfigurationCreate, db: Session = Depends(get_db)):
    return crud.create_configuration(db=db, configuration=configuration)

@router.post("/backup_jobs/", response_model=schema.BackupJob)
def create_backup_job(backup_job: schema.BackupJobCreate, db: Session = Depends(get_db)):
    return crud.create_backup_job(db=db, backup_job=backup_job)

@router.post("/backup/")
async def create_backup(request: schema.BackupRequest, backup_service: BackupService = Depends(get_backup_service)):
    try:
        job = backup_service.create_backup_job(request.source, request.target)
        backup_service.start_backup_job(job.id, upload_to_s3=request.upload_to_s3, s3_key=request.s3_key)
        return {"job_id": job.id, "status": "Backup started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {e}")
    
@router.post("/backup/nfs/")
async def backup_to_nfs(request: schema.NFSBackupRequest, backup_service: BackupService = Depends(get_backup_service)):
    try:
        job = backup_service.create_backup_job(request.source, request.local_path)
        backup_service.start_backup_job(job.id, use_nfs=True, nfs_path=request.nfs_path)
        return {"job_id": job.id, "status": "Backup to NFS started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup to NFS failed: {e}")

@router.get("/backup/{job_id}/status/")
def get_backup_status(job_id: int, backup_service: BackupService = Depends(get_backup_service)):
    job = backup_service.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job.id, "status": job.status, "error_message": job.error_message}

@router.post("/backup_metadata/", response_model=schema.BackupMetadata)
def create_backup_metadata(backup_metadata: schema.BackupMetadataCreate, db: Session = Depends(get_db)):
    return crud.create_backup_metadata(db=db, backup_metadata=backup_metadata)
