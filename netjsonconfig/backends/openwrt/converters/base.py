from ...base.converter import BaseConverter


class OpenWrtConverter(BaseConverter):
    _uci_types = []

    def should_skip_block(self, block):
        _type = block.get('.type')
        return not block or _type not in self._uci_types

    def _get_uci_name(self, name):
        return name.replace('.', '_').replace('-', '_')
