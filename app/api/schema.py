from pydantic import BaseModel
from typing import Optional

class BackupRequest(BaseModel):
    source: str
    target: str
    upload_to_s3: bool
    s3_key: str


class NFSBackupRequest(BaseModel):
    nfs_path: str
    local_path: str
    source: str

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class BackupJobBase(BaseModel):
    source_path: str
    target_path: str
    status: str
    owner_id: int

class  BackupJobCreate(BackupJobBase):
    pass

class BackupJob(BackupJobBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class ConfigurationBase(BaseModel):
    key: str
    value: str

class ConfigurationCreate(ConfigurationBase):
    pass

class Configuration(ConfigurationBase):
    id: int

    class Config:
        orm_mode = True

class BackupMetadataBase(BaseModel):
    backup_job_id: int
    size: int
    duration: int
    details: Optional[str] = None

class BackupMetadataCreate(BackupMetadataBase):
    pass

class BackupMetadata(BackupMetadataBase):
    id: int

    class Config:
        orm_mode = True

