# app/services/crud.py
from sqlalchemy.orm import Session
from app.core.models import User, BackupJob, Configuration, BackupMetadata
from app.api.schema import UserCreate, BackupJobCreate, ConfigurationCreate, BackupMetadataCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_backup_job(db: Session, backup_job: BackupJobCreate):
    # db_backup_job = BackupJob(**backup_job.dict(), owner_id=owner_id)
    db_backup_job = BackupJob(
        source_path=backup_job.source_path,
        target_path=backup_job.target_path,
        status=backup_job.status,
        owner_id=backup_job.owner_id
    )
    db.add(db_backup_job)
    db.commit()
    db.refresh(db_backup_job)
    print("Backup job created:", db_backup_job)
    return db_backup_job

def create_configuration(db: Session, configuration: ConfigurationCreate):
    db_configuration = Configuration(**configuration.dict())
    db.add(db_configuration)
    db.commit()
    db.refresh(db_configuration)
    return db_configuration

def get_configuration(db: Session, key: str):
    return db.query(Configuration).filter(Configuration.key == key).first()

def get_configurations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Configuration).offset(skip).limit(limit).all()

def create_backup_metadata(db: Session, backup_metadata: BackupMetadataCreate):
    db_backup_metadata = BackupMetadata(**backup_metadata.dict())
    db.add(db_backup_metadata)
    db.commit()
    db.refresh(db_backup_metadata)
    return db_backup_metadata

def get_backup_job_by_id(db: Session, job_id: int):
    """Retrieve a backup job by its ID."""
    return db.query(BackupJob).filter(BackupJob.id == job_id).first()

def get_owner_id(db: Session):
    """Retrieve the owner_id of the BackupJob."""
    backup_job = db.query(BackupJob).order_by(BackupJob.id.desc()).first()
    return backup_job.owner_id if backup_job else 0

