
from .construct_base import ConstructBase
from .str_construct_exceptions import StrConstructBuildError, StrConstructParseError, StrStopFieldError

class StrStruct(ConstructBase):
    def __init__(self, *args, **kwargs):
        for item in args:
            if not isinstance(item, ConstructBase):
                raise TypeError(
                    "All items need to be of type ConstructBase (e.g. StrFloat, StrInt, etc.). Found "
                    f"a {type(item)}."
                )
        try:
            self._separator = kwargs["separator"]
        except KeyError:
            self._separator = ""
        self.name = kwargs["name"] if "name" in kwargs.keys() else None
        self._fields = args

    def _div(self, other):
        # As this class has a different footprint for the __init__ method, we need to
        # override this method
        if not isinstance(other, str):
            raise TypeError("Division is support only for strings")
        return StrStruct(name=other, separator=self._separator, *self._fields)

    def _build(self, values, **ctx):
        if not isinstance(values, dict):
            raise TypeError("The value for building an StrConstruct should be a dict")

        outputs = []
        for field in self._fields:
            if field.name in ctx.keys():
                raise ValueError(f"Got two definitions for {field.name}")
            if field.name is None:
                # Well there is no name. So we can't find a given value. In this case, the
                # build method of the corresponding object is expected to be able to build
                # without a give value. Let's give it a try.
                try:
                    output = field.build(**ctx)
                except StrStopFieldError:
                    # Nothing problematic. The StopIf construct has signaled to stop building
                    break
                except Exception as e:
                    raise StrConstructBuildError("Could not build the nameless field")

            else:
                try:
                    value = values[field.name]
                except KeyError:
                    # If the key-value pair is not provided, try to build it with no value
                    try:
                        output = field.build(**ctx)
                    except StrStopFieldError:
                        break
                else:
                    try:
                        output = field.build(value, **ctx)
                    except StrStopFieldError:
                        break
                ctx[field.name] = value
            outputs.append(output)

        return self._separator.join(outputs)

    def _parse(self, string, **ctx):
        outputs = {}
        for index, field in enumerate(self._fields):
            try:
                output = field.parse(string, **ctx)
            except StrStopFieldError:
                break
            if field.name is not None and field.name[0] != "_":
                outputs[field.name] = output
                if field.name in ctx.keys():
                    raise ValueError(f"Got two definitions for {field.name}")
                ctx[field.name] = output
            string = field.parse_left()
            self._parse_left = string

            # No need to check the separator for the last item
            if index != (len(self._fields) - 1) and self._separator != "":
                if not string.startswith(self._separator):
                    raise StrConstructParseError(f"Separator ('{self._separator}') not found")
                string = string[len(self._separator):]

        return outputs
