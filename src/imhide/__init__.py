# -*- coding: utf-8 -*-
"""

.. include:: ../../README.md

# Testing

## Run the tests

To run tests, just run:

    pdm run pytest

## Test reports

[See test report](../tests/report.html)



[See coverage](../coverage/index.html)

.. include:: ../../CHANGELOG.md

"""
import logging

from rich.logging import RichHandler
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    loglevel: str


settings = Settings()  # pyright: ignore[reportCallIssue]

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger("imhide_logger")
logger.addHandler(RichHandler(rich_tracebacks=False))
logger.setLevel(settings.loglevel.upper())
