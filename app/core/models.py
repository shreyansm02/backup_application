from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    backup_jobs = relationship("BackupJob", back_populates="owner")

class BackupJob(Base):
    __tablename__ = 'backup_jobs'

    id = Column(Integer, primary_key=True, index=True)
    source_path = Column(String, nullable=False)
    target_path = Column(String, nullable=False)
    status = Column(String, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    error_message = Column(String) 
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="backup_jobs")

class Configuration(Base):
    __tablename__ = 'configurations'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(Text, nullable=False)

class BackupMetadata(Base):
    __tablename__ = 'backup_metadata'

    id = Column(Integer, primary_key=True, index=True)
    backup_job_id = Column(Integer, ForeignKey('backup_jobs.id'))
    size = Column(Integer)
    duration = Column(Integer)
    details = Column(Text)
