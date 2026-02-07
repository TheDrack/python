# -*- coding: utf-8 -*-
"""Database models for user authentication using SQLModel"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    SQLModel table for storing user authentication data
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: Optional[str] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    hashed_password: str
    disabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
