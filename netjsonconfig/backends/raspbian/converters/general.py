from ....utils import get_copy
from .base import RaspbianConverter


class General(RaspbianConverter):
    netjson_key = 'general'

    def to_intermediate(self):
        result = []
        general = get_copy(self.netjson, self.netjson_key)
        result.append(general)
        return (('general', result),)
