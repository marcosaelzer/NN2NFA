from dataclasses import dataclass
from typing import List


@dataclass
class Inequality:
    left_side: List[float or None]
    right_side: float
    leq: bool

    def __str__(self):
        ineq_str_representation = ""
        if self.left_side[0] is not None:
            if self.left_side[0] >= 0:
                ineq_str_representation += f"{self.left_side[0]}x_0"
            else:
                ineq_str_representation += f"-{self.left_side[0]*-1}x_0"

        for idx, operand in enumerate(self.left_side[1:]):
            if operand is None:
                continue
            elif operand >= 0:
                if ineq_str_representation == "":
                    ineq_str_representation += f"{operand}x_{idx + 1}"
                else:
                    ineq_str_representation += f" + {operand}x_{idx+1}"
            else:
                ineq_str_representation += f" - {operand*-1}x_{idx+1}"

        ineq_str_representation += (" <= " if self.leq else " >= ") + str(self.right_side)

        return ineq_str_representation


@dataclass
class OutReachProperty:
    input_specification: List[Inequality]
    output_specification: List[Inequality]

    def __str__(self):
        input_specification_parts = []
        for inequality in self.input_specification:
            input_specification_parts.append(str(inequality))
        output_specification_parts = []
        for inequality in self.output_specification:
            output_specification_parts.append(str(inequality).replace('x', 'y'))

        return f"Input Specification: {' && '.join(input_specification_parts)} \n" \
               f"Output Specification: {' && '.join(output_specification_parts)}"
