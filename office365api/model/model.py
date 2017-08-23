import funcsigs


class Model(object):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __iter__(self):
        """
        Convert objects back to dictionary.
        :return: Dictionary representation.
        """
        for k, v in self.__dict__.items():
            if v is not None:
                yield k,  Model.get_value(v)

    @staticmethod
    def get_value(value):
        """
        Convert objects back to dictionary.
        :param value:
        :return:
        """
        if isinstance(value, list):
            return [Model.get_value(v) for v in value]
        if issubclass(type(value), Model):
            return dict(value)
        return value

    @classmethod
    def parameters(cls):
        parameters = funcsigs.signature(cls.__init__).parameters.copy()
        parameters.pop('self')
        return parameters

    @classmethod
    def from_dict(cls, data):
        kwargs = {}
        for arg in cls.parameters():
            kwargs[arg] = Model.get_data(data.pop(arg)) if arg in data else None
        model = cls(**kwargs)
        model.__dict__.update(data)
        return model

    @staticmethod
    def get_data(value):
        if isinstance(value, list):
            return [Model.get_data(v) for v in value]
        if isinstance(value, Model):
            return value.from_dict(value)
        return value

    @property
    def data(self):
        return {self.__class__.__name__: dict(self)}