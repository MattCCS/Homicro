
from datetime import datetime, timedelta

from models import RegistryEntry


REGISTRY: dict[str, RegistryEntry] = {}


class ActionNotAllowedException(Exception):
    pass


def register(source_ip: str, name: str, port: int, expire: int) -> RegistryEntry:
    _clear_expired_entries()

    if (entry := REGISTRY.get(name)) is None or not entry.expire:
        return _register_upsert(name=name, ip=source_ip, port=port, expire=expire)

    if entry.ip == source_ip:
        return _register_upsert(name=name, ip=source_ip, port=port, expire=entry.expire)

    raise ActionNotAllowedException("Action not allowed yet.")


def discover():
    _clear_expired_entries()
    return {
        k: {
            **v.dict(exclude={"ip", "expire_at"}),
            "ip": str(v.ip),
            "expire_at": v.expire_at.strftime("%c") if v.expire_at else None,
        }
        for (k, v) in REGISTRY.items()
    }


def _register_upsert(name: str, ip: str, port: int, expire: int):
    expire_at = None if not expire else (datetime.now() + timedelta(seconds=expire))
    entry = RegistryEntry(
        ip=ip,
        port=port,
        expire=expire,
        expire_at=expire_at,
    )
    REGISTRY[name] = entry
    return entry


def _clear_expired_entries():
    now = datetime.now()
    expired_entries = {name for name in REGISTRY if (expire_at := REGISTRY[name].expire_at) is not None and expire_at < now}
    for name in expired_entries:
        REGISTRY.pop(name, None)
