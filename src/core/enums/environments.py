from enum import Enum


class EnvironmentEnum(str, Enum):
    INT = 'INT'
    UAT = 'UAT'
    PROD = 'PROD'
    BASE = 'BASE'

