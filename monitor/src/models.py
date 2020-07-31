from typing import (
    ClassVar,
)
from datetime import (
    datetime,
    timedelta,
)
from pydantic import (
    Field,
)

from src.model_mapper import ModelMapper

MAX_URL_LENGTH = 2 ** 16


class WebsiteHealth(ModelMapper):
    table_name: ClassVar = 'monitor_website_health'

    # TODO: the reason for the extra `description` is because `constr` could not be
    #       easily introspected for the column declaration
    url: str = Field(max_length=MAX_URL_LENGTH, description='str')
    status_code: int = Field(description='int')
    response_time: timedelta = Field(description='timedelta')
    pattern_found: bool = Field(default=False, description='bool')
    timestamp: datetime = Field(default_factory=datetime.utcnow, description='timestamp')
