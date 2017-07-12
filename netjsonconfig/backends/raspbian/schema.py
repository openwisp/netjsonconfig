from ...schema import schema as default_schema
from ...utils import merge_config

schema = merge_config(default_schema, {})
