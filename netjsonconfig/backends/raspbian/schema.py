from ..schema import schema as default_schema
from ..schema import DEFAULT_FILE_MODE
from ..utils import merge_config

schema = merge_config(default_schema, {})
