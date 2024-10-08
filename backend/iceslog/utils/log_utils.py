from fastapi import Request
from redis.asyncio import Redis
from iceslog.utils import base_utils, http_utils, pool_utils, log_save_utils
from iceslog.utils.scheduler_utils import scheduler


def do_record_syslog(request: Request, module: str, content: str):
    from iceslog.models.syslog import SysLog
    from iceslog.core.db import get_db
    session = next(get_db())
    log = SysLog(module=module, content=content,
                 request_uri=str(request.url), ip=http_utils.get_client_ip(request), province="", city="",
                 execution_time=0, browser=http_utils.get_browser(request))
    session.add(log)
    session.commit()

last_check_minute = base_utils.get_now_minute()
def get_apilog_key(step: int) -> str:
    return  f"apilog_freq:{step}"

async def try_cache_last(redis: Redis):
    global last_check_minute
    now = base_utils.get_now_minute()
    if last_check_minute >= now:
        return
    
    for idx in range(last_check_minute, now):
        key = get_apilog_key(idx)
        val = await redis.getdel(key)
        if val:
            from iceslog.models.logs.record import LogFreq
            from iceslog.core.db import get_db
            log_freq = LogFreq.model_validate({
                "module": "log",
                "log_time": idx,
                "times": val,
            })
            session = next(get_db())
            session.add(log_freq)
            session.commit()
    last_check_minute = now
        
async def do_record_apilogs(project, logs):
    from iceslog.models.logs.record import RecordLog
    redis = await pool_utils.get_redis_cache()
    logs: list[RecordLog] = logs
    new_logs = []
    now = base_utils.now()
    for log in logs:
        if not log.create:
            log.create = now
        new_logs.append(log.model_dump())
    log_save_utils.append_logs(project, new_logs)
    key = get_apilog_key(base_utils.get_now_minute())
    await redis.incr(key, len(new_logs))
    await redis.expire(key, 180)

async def do_record_apilog(project, log):
    from iceslog.models.logs.record import RecordLog
    log: RecordLog = log
    await do_record_apilogs(project, [log])
   
# 每分钟执行的定时任务
@scheduler.scheduled_job('interval', minutes=1)
async def write_log_job():
    redis = await pool_utils.get_redis_cache()
    await try_cache_last(redis)