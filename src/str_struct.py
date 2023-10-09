
from construct_base import ConstructBase
from str_construct_exceptions import StrConstructBuildError, StrConstructParseError

class StrStruct(ConstructBase):
    def __init__(self, *args, **kwargs):
        for item in args:
            if not isinstance(item, ConstructBase):
                raise TypeError(
                    "All items need to be of type ConstructBase (e.g. StrFloat, StrInt, etc.). Found "
                    f"a {type(item)}."
                )
        self._separator = kwargs["separator"]
        self.name = kwargs["name"] if "name" in kwargs.keys() else None
        self._fields = args

    def _div(self, other):
        # As this class has a different footprint for the __init__ method, we need to
        # override this method
        if not isinstance(other, str):
            raise TypeError("Division is support only for strings")
        return StrStruct(name=other, separator=self._separator, *self._fields)

    def _build(self, values):
        if not isinstance(values, dict):
            raise TypeError("The value for building an StrConstruct should be a dict")

        outputs = []
        for field in self._fields:
            if field.name is None:
                # Well there is no name. So we can't find a given value. In this case, the
                # build method of the corresponding object is expected to be able to build
                # without a give value. Let's give it a try.
                try:
                    output = field.build()
                except Exception as e:
                    raise StrConstructBuildError("Could not build the nameless field")

            else:
                value = values[field.name]
                output = field.build(value)
            outputs.append(output)

        return self._separator.join(outputs)

    def _parse(self, string):
        values = string.split(self._separator)

        if len(values) != len(self._fields):
            # What if the separator is also present in a constant field?
            raise StrConstructParseError("Bad input")

        output = {}
        for field, value in zip(self._fields, values):
            output[field.name] = field.parse(value)

        return output