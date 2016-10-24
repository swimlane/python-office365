import inspect
from typing import Any


class Model(object):

    def __getattr__(self, name):
        return self.get(name)

    @classmethod
    def parameters(cls):
        parameters = inspect.signature(cls.__init__).parameters.copy()
        parameters.pop('self')
        return parameters

    @classmethod
    def from_dict(cls, data: dict):
        kwargs = {}
        for arg in cls.parameters().values():
            kwargs[arg.name] = Model.get_data(data.pop(arg.name), arg.annotation)
        model = cls(**kwargs)
        model.__dict__.update(data)
        return model

    @staticmethod
    def get_data(value, value_type)->Any:
        if isinstance(value_type, list):
            return [Model.get_data(v, value_type[0]) for v in value]
        if issubclass(value_type, Model):
            return value_type.from_dict(value)
        return value
