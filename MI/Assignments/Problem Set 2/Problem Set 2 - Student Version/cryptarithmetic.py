from typing import List, Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

# TODO (Optional): Import any builtin library or define any helper function you want to use


# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that it can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None:
                continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) + ")"
        return formula

    @staticmethod
    def from_text(text: str) -> "CryptArithmeticProblem":
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match:
            raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i + 1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        # TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is a string (the variable name)
        # problem.domains:      should be a dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constraints:  should contain a list of constraints (either unary or binary constraints).

        lhs0, lhs1, rhs = LHS0, LHS1, RHS

        # All unique characters
        letters = set(lhs0 + lhs1 + rhs)

        # Initialize variables and domains
        problem._initialize_variables(letters)

        # Initial constraints
        problem.constraints = []

        # All words must not start with 0
        leading_chars = problem._get_first_letters([lhs0, lhs1, rhs])
        problem._apply_unary_constraints(leading_chars)

        # Ensure all letters have unique values
        problem._apply_binary_constraints()

        # Initialize carry variables, count=rhs+1
        rhs_sz = len(rhs)
        carries = problem._setup_carry_variables(rhs_sz)

        # Reverse so indices start from least digit
        rev_lhs0, rev_lhs1, rev_rhs = lhs0[::-1], lhs1[::-1], rhs[::-1]

        #         F = 0   + C3
        # 10*C3 + O = 2*T + C2
        # 10*C2 + U = 2*W + C1
        # 10*C1 + R = 2*O

        for i in range(rhs_sz):
            aux_var = f"aux{i}"
            problem.variables.append(aux_var)

            # 1 (carry) * 100 + 9 (digit) * 10 + 9 (digit) = 199
            problem.domains[aux_var] = set(range(200))

            # Add constraints based on available digits
            problem._add_digit_constraints(i, rev_lhs0, rev_lhs1, rev_rhs, carries, aux_var)

        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, "r") as f:
            return CryptArithmeticProblem.from_text(f.read())


    # *******************************************************************************
    def _initialize_variables(self, letters: set):
        # Initialize variables and their domains
        self.variables = list(letters)
        self.domains = {letter: set(range(10)) for letter in letters}

    def _get_first_letters(self, words: List[str]) -> List[str]:
        # Retrieve the first letters of each word
        return [word[0] for word in words]

    def _apply_unary_constraints(self, leading: List[str]):
        # Apply unary constraints
        for letter in leading:
            self.constraints.append(UnaryConstraint(letter, lambda x: x > 0))

    def _apply_binary_constraints(self):
        # Apply binary constraints to ensure all letters have unique values
        for idx, var1 in enumerate(self.variables):
            for var2 in self.variables[idx + 1 :]:
                self.constraints.append(
                    BinaryConstraint((var1, var2), lambda x, y: x != y)
                )

    def _setup_carry_variables(self, rhs_sz: int) -> List[str]:
        # Initialize carry variables and apply related unary constraints
        carries = [f"C{i}" for i in range(rhs_sz + 1)]
        self.variables += carries
        self.domains.update({c: {0, 1} for c in carries})

        # Initial and final carries = 0
        self.constraints.append(UnaryConstraint(carries[0], lambda x: x == 0))
        self.constraints.append(UnaryConstraint(carries[-1], lambda x: x == 0))

        # RHS is longer by one ?
        other_len = max(len(self.LHS[0]), len(self.LHS[1]))
        if rhs_sz == other_len + 1:
            self.constraints.append(UnaryConstraint(carries[-2], lambda x: x == 1))

        return carries

    def _get_tens_digit(self, num: int) -> int:
        # Extract the tens digit from a number
        return (num // 10) % 10

    def _get_ones_digit(self, num: int) -> int:
        # Extract the ones digit from a number
        return num % 10

    def _get_hundreds_digit(self, num: int) -> int:
        # Extract the hundreds digit from a number
        return num // 100

    def _compute_carry(self, num: int) -> int:
        # Compute the carry value for a sum
        return num // 10

    def _add_digit_constraints(
        self,
        index: int,
        lhs0: str,
        lhs1: str,
        rhs: str,
        carries: List[str],
        aux_var: str,
    ):
        # Case 1: no digits from either number, just handling carries
        if index >= len(lhs0) and index >= len(lhs1):
            # Constraint: carry value for next position
            self.constraints.append(
                BinaryConstraint(
                    (carries[index + 1], aux_var),
                    lambda c, y: c == self._compute_carry(self._get_hundreds_digit(y)),
                )
            )

            # Constraint: result digit from carry
            self.constraints.append(
                BinaryConstraint(
                    (rhs[index], aux_var),
                    lambda d, y: d == self._get_hundreds_digit(y) % 10,
                )
            )

        # Case 2: both first and second numbers have digits at this position
        elif index < len(lhs0) and index < len(lhs1):
            # Constraint: first number's digit maps to tens place
            self.constraints.append(
                BinaryConstraint(
                    (lhs0[index], aux_var), lambda x, y: x == self._get_tens_digit(y)
                )
            )

            # Constraint: second number's digit maps to ones place
            self.constraints.append(
                BinaryConstraint(
                    (lhs1[index], aux_var), lambda x, y: x == self._get_ones_digit(y)
                )
            )

            # Constraint: carry value for next position
            self.constraints.append(
                BinaryConstraint(
                    (carries[index + 1], aux_var),
                    lambda c, y: c
                    == self._compute_carry(
                        self._get_hundreds_digit(y)
                        + self._get_tens_digit(y)
                        + self._get_ones_digit(y)
                    ),
                )
            )

            # Constraint: result digit from sum of all digits
            self.constraints.append(
                BinaryConstraint(
                    (rhs[index], aux_var),
                    lambda d, y: d
                    == (
                        self._get_hundreds_digit(y)
                        + self._get_tens_digit(y)
                        + self._get_ones_digit(y)
                    )
                    % 10,
                )
            )

        # Case 3: only first number has a digit at this position
        elif index < len(lhs0):
            # Constraint: first number's digit maps to tens place
            self.constraints.append(
                BinaryConstraint(
                    (lhs0[index], aux_var), lambda x, y: x == self._get_tens_digit(y)
                )
            )

            # Constraint: carry value for next position
            self.constraints.append(
                BinaryConstraint(
                    (carries[index + 1], aux_var),
                    lambda c, y: c
                    == self._compute_carry(
                        self._get_hundreds_digit(y) + self._get_tens_digit(y)
                    ),
                )
            )

            # Constraint: result digit from sum
            self.constraints.append(
                BinaryConstraint(
                    (rhs[index], aux_var),
                    lambda d, y: d
                    == (self._get_hundreds_digit(y) + self._get_tens_digit(y)) % 10,
                )
            )

        # case 4: only second number has a digit at this position
        elif index < len(lhs1):
            # Constraint: second number's digit maps to ones place
            self.constraints.append(
                BinaryConstraint(
                    (lhs1[index], aux_var), lambda x, y: x == self._get_ones_digit(y)
                )
            )

            # Constraint: carry value for next position
            self.constraints.append(
                BinaryConstraint(
                    (carries[index + 1], aux_var),
                    lambda c, y: c
                    == self._compute_carry(
                        self._get_hundreds_digit(y) + self._get_ones_digit(y)
                    ),
                )
            )

            # Constraint: result digit from sum
            self.constraints.append(
                BinaryConstraint(
                    (rhs[index], aux_var),
                    lambda d, y: d
                    == (self._get_hundreds_digit(y) + self._get_ones_digit(y)) % 10,
                )
            )

        # Constraint: current position's carry maps to hundreds place
        self.constraints.append(
            BinaryConstraint(
                (carries[index], aux_var), lambda c, y: c == self._get_hundreds_digit(y)
            )
        )
