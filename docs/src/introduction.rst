Introduction
############

StrConstruct is declarative parser and builder for string-based data/protocols with a syntax
similar to the `Construct <https://construct.readthedocs.io/en/latest/index.html>`_`
python package. It provides a powerful syntax for defining protocols and it takes care
of parsing and building strings based on the defined protocols. This makes code more
readable, concise and maintainable.

Here is an example.

    >>> from strconstruct import StrInt, StrFloat, StrConst, StrStruct, StrDefault, StrSwitch
    >>> protocol = StrStruct(
    ...     StrConst(">"),
    ...     "register" / StrDefault(StrInt("d"), 17),
    ...     StrConst(","),
    ...     "value1" / StrSwitch(
    ...         lambda this: this["register"],
    ...         {
    ...             1: StrFloat("0.1f"),
    ...             2: StrInt("d"),
    ...             3: StrInt("02X"),
    ...         },
    ...         default=StrInt("03X"),
    ...     ),
    ...     StrConst("\r"),
    ... )
    >>> protocol.build(
    ...     {
    ...         "register": 3,
    ...         "value1": 16,
    ...     }
    ... )
    '>3,10\r'
    >>> protocol.build({"register": 1, "value1": 16})
    '>1,16.0\r'
    >>> protocol.parse(">4,020\r")
    {'register': 4, 'value1': 32}
