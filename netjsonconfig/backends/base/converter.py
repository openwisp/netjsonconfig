class BaseConverter(object):
    """
    Base Converter class
    Converters are used to convert a configuration dictionary
    which represent a NetJSON object to a data structure that
    can be easily rendered as the final router configuration
    and vice versa.
    """
    netjson_key = None

    def __init__(self, backend):
        self.backend = backend
        self.netjson = backend.config
        self.intermediate_data = backend.intermediate_data

    @classmethod
    def should_run(cls, config):
        """
        Returns True if Converter should be instantiated and run
        Used to skip processing if the configuration part related to
        the converter is not present in the configuration dictionary.
        """
        netjson_key = cls.netjson_key or cls.__name__.lower()
        return netjson_key in config

    def to_intermediate(self):  # pragma: no cover
        raise NotImplementedError()
