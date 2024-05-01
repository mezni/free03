import uuid
from datetime import datetime
from typing import TypeVar, List, Dict
from pydantic import BaseModel
from src.entities import Batch

UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


def generate_uuid() -> UUIDType:
    return uuid.uuid4()


class BatchInpoutDto(Batch):
    batch_code: UUIDType = None
    batch_name: str
    batch_start_time: datetime = None
    batch_end_time: datetime = None
    batch_status: str = None
    exit_status: str = None
    exit_message: str = None

    def model_post_init(self, __context) -> None:
        self.batch_code = generate_uuid()
        self.batch_start_time = datetime.now()


class InputReaderUseCase:
    def __init__(self, input_reader):
        self.input_reader = input_reader

    def execute(self, source_path):
        # batch
        # load
        #
        batch_info = {
            "batch_name": "laod source",
            "batch_start_time": datetime.now(),
            "batch_end_time": None,
            "batch_status": None,
            "exit_status": None,
            "exit_message": None,
        }
        batch_info["batch_end_time"] = datetime.now()
        batch_info["batch_status"] = "finish"
        batch_info["exit_status"] = "0"
        batch_info["exit_message"] = "success"
        batch = BatchInpoutDto(**batch_info)
        print(batch.model_dump())
        return self.input_reader.read_source(source_path)
