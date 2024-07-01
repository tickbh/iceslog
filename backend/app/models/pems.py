from datetime import datetime
from pydantic import ConfigDict, EmailStr
from sqlalchemy import JSON, DateTime, func
from sqlmodel import Field, Relationship, SQLModel, Column


class Perms(SQLModel, table=True):
    id: int = Field(primary_key=True,  description="id值")
    name: str = Field(max_length=50, nullable=False, description="名字")
    route: str = Field(max_length=255, nullable=False,
                       unique=True, description="路由")
    codename: str = Field(max_length=50, nullable=False, description="代码名字")
    sort: int = Field(nullable=False, default=0, description="排序")
    create_time: datetime = Column(DateTime, server_default=func.now(), comment="创建时间")


class GroupPerms(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int = Field(primary_key=True, description="ID")
    name: str = Field(max_length=50, nullable=False, description="名字")
    permissions: JSON = Column(JSON,
        max_length=10240, nullable=False, default="[]", comment="拥有权限数,如[1, 2, 3, 4, 5]")
    create_time: datetime = Column(DateTime, server_default=func.now(), comment="创建时间")
