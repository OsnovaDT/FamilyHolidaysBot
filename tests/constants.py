"""Constants for the tests"""

ALL_TYPES_AND_EXAMPLES = {
    "str": "test string",
    "int1": 101,
    "int2": -23,
    "float": 45.6,
    "bool": True,
    "list": [1, 2, 3],
    "tuple": (1, 2, 3, 4),
    "set": {1, 2, 3, 4, 5},
    "dict": {"test1": 1, "test2": 2.1},
}

NOT_STR_VALUES = ALL_TYPES_AND_EXAMPLES.copy()
NOT_STR_VALUES.pop("str")

WRONG_AGES = ALL_TYPES_AND_EXAMPLES.copy()
WRONG_AGES.pop("int1")
