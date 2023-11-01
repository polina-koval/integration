import logging
import os

from integration.app.config import settings
from integration.utils.request_id import request_id_manager


LOCATION_FORMAT = "%(filename)s:%(lineno)d"
FACILITY_NAME = os.environ.get("FACILITY_NAME", settings.APP_NAME)
FACILITY_ID = os.environ.get("FACILITY_ID", FACILITY_NAME + "-0")
LOG_FORMAT = (
    "["
    "%(levelno)d|"
    "%(asctime)s|"
    "{facility_name}|"
    "{facility_id}|"
    "%(request_id)s|"
    "{location}]"
    "%(message)s".format(
        facility_name=FACILITY_NAME, facility_id=FACILITY_ID, location=LOCATION_FORMAT
    )
)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_manager.get()
        return True


def configure_logging():
    handlers = [logging.StreamHandler()]
    if settings.LOG_FILENAME:
        handlers.append(logging.FileHandler(settings.LOG_FILENAME))

    for h in handlers:
        h.addFilter(RequestIdFilter())

    logging.basicConfig(level=settings.LOG_LEVEL, format=LOG_FORMAT, handlers=handlers)
