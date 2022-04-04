from enum import IntEnum


class DropOffAction(IntEnum):
    DROP_OFF_01 = 9  # not last row, rhs
    DROP_OFF_34 = 10  # not last row, lhs
    DROP_OFF_2 = 11  # last row, rhs
    DROP_OFF_5 = 12  # last row, lhs
