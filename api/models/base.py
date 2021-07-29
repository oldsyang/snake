from typing import List, Union

from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.engine.result import RowProxy
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from settings import config
from utils.tools import ObjectDict, now_time

IGNORE_ATTRS = ['redis', 'stats']
MC_KEY_ITEM_BY_ID = '%s:%s'


class PropertyHolder(type):
    """
    We want to make our class with som useful properties
    and filter the private properties.
    """

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        new_cls.property_fields = []

        for attr in list(attrs) + sum([list(vars(base))
                                       for base in bases], []):
            if attr.startswith('_') or attr in IGNORE_ATTRS:
                continue
            if isinstance(getattr(new_cls, attr), property):
                new_cls.property_fields.append(attr)
        return new_cls


@as_declarative()
class Base():
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return "_".join([config.DB_TABLE_PREFIX, cls.__name__.lower()])


class ModelMeta(Base.__class__, PropertyHolder):
    ...


class BaseModel(Base, metaclass=ModelMeta):
    __abstract__ = True
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=now_time, index=True)

    @classmethod
    def to_dict(cls,
                results: Union[RowProxy, List[RowProxy]]) -> Union[List[dict], dict]:
        if not isinstance(results, list):
            return ObjectDict({col: val for col, val in zip(results.keys(), results)})
        list_dct = []
        for row in results:
            list_dct.append(ObjectDict({col: val for col, val in zip(row.keys(), row)}))
        return list_dct
