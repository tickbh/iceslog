from typing import Any, List

from fastapi import APIRouter, Body, Depends, Form, HTTPException
from sqlmodel import col, delete, func, or_, select

from iceslog import models
from iceslog.api.deps import (
    CurrentUser,
    PageNumType,
    PageSizeType,
    SessionDep,
    check_has_perm,
    get_current_active_superuser,
)
from iceslog.core.config import settings
from iceslog.core.security import get_password_hash, verify_password
from iceslog.models import (
    RetMsg,
)
from iceslog.models.base import OptionType
from iceslog.models.dictmap import DictMap, DictMapItem, MsgDictItemsPublic, MsgEditDictMap, OneDictItem, OneEditDictMap

from iceslog.models.logs.store import LogsStore, LogsStoreBase, LogsStoreCreate, LogsStorePublices, LogsStoreUpdateUrl
from iceslog.models.perms import GroupPerms, GroupPermsBase, GroupPermsPublic, OnePerm, Perms, PermsPublic
from iceslog.models.syslog import LogsPublic, SysLog
from iceslog.utils import base_utils, cache_utils
from iceslog.utils.cache_table import CacheTable
from iceslog.utils.utils import page_view_condition
from yarl import URL

router = APIRouter(
    dependencies=[Depends(check_has_perm)])

@router.get("/page", response_model=LogsStorePublices)
def get_logs_store(session: SessionDep, keywords: str = None, status: int = None, project: str = None, pageNum: PageNumType = 0, pageSize: PageSizeType = 100):
    condition = []
    if keywords:
        condition.append(or_(LogsStore.name.like(f"%{keywords}%"), LogsStore.store.like(f"%{keywords}%")))
    if status != None:
        condition.append(LogsStore.status == status)
    if project != None:
        condition.append(LogsStore.project == project)
        
    logs, count = page_view_condition(session, condition, LogsStore, pageNum, pageSize, [col(LogsStore.sort).desc()])
    for log in logs:
        parsed_url = URL(log.connect_url)
        if not parsed_url:
            continue
        if parsed_url.user:
            parsed_url = parsed_url.with_user("***")
        if parsed_url.password:
            parsed_url = parsed_url.with_password("***")
        log.connect_url = parsed_url.human_repr()
        
    return LogsStorePublices(list=logs, total=count)

@router.post(
    "/create", response_model=LogsStoreBase
)
def create_user(*, session: SessionDep, store_in: LogsStoreCreate) -> Any:
    url = URL(store_in.connect_url)
    if not url or not url.scheme:
        raise HTTPException(400, "无效的url")

    store = LogsStore.model_validate(store_in)
    session.add(store)
    session.commit()
    session.refresh(store)
    return store


@router.get(
    "/form", 
    response_model=LogsStoreBase
)
def read_store_form(*, session: SessionDep, id: int) -> Any:
    
    store = session.get(LogsStore, id)
    if not store:
        return RetMsg("00001", "账号不存在")
    
    return store

@router.patch(
    "/url/{id}", 
    response_model=LogsStoreBase
)
def set_store_connect_url(*, session: SessionDep, id: int, body: LogsStoreUpdateUrl) -> Any:
    store = session.get(LogsStore, id)
    if not store:
        return RetMsg("00001", "账号不存在")
    url = URL(body.connect_url)
    if not url or not url.scheme:
        raise HTTPException(400, "无效的url")
    store.connect_url = body.connect_url
    session.merge(store)
    session.commit()
    return store


@router.put(
    "/{id}",
    response_model=LogsStoreBase,
)
def update_store(
    *,
    session: SessionDep,
    id: int,
    user_in: LogsStoreBase,
) -> Any:
    """
    Update a user.
    """

    store = session.get(LogsStore, id)
    if not store:
        raise HTTPException(
            status_code=404,
            detail="当前存储方式不存在",
        )
    store.sqlmodel_update(user_in)
    session.merge(store)
    session.commit()
    return store


@router.delete("/{stores}")
def delete_user(
    session: SessionDep, stores: str
) -> RetMsg:
    """
    Delete a user.
    """
    ids = base_utils.split_to_int_list(stores, ",")
    for id in ids:
        store = session.get(LogsStore, id)
        if not store:
            raise HTTPException(status_code=404, detail="未找到存储配置")
        session.delete(store)
        session.commit()
    return RetMsg(msg="User deleted successfully")
