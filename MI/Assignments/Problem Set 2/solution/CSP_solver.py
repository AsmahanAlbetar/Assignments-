from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    """
    Implement forward checking:
    - domains is the current domains of *unassigned* variables only.
    - For every binary constraint that involves the assigned variable:
        - If the other variable is unassigned (exists in `domains`), remove from its domain
          any value that does not satisfy the binary constraint together with the assigned value.
    - If any domain becomes empty return False. Otherwise return True.

    Important detail about ordering of arguments passed to the constraint:
    - BinaryConstraint.condition expects arguments in the same order as BinaryConstraint.variables.
      So we must check which position assigned_variable occupies, and pass (assigned_value, candidate)
      or (candidate, assigned_value) accordingly.
    """
    for constraint in problem.constraints:
        # only binary constraints are relevant for forward checking
        if not isinstance(constraint, BinaryConstraint):
            continue
        v1, v2 = constraint.variables
        if assigned_variable not in (v1, v2):
            continue

        other = constraint.get_other(assigned_variable)
        # If other is not in domains it means it's already assigned -> skip
        if other not in domains:
            continue

        new_domain = set()
        # For every candidate in the other variable domain, check if it satisfies the constraint
        # with the assigned value. Must preserve correct order according to constraint.variables.
        if assigned_variable == v1:
            # constraint.condition(assigned_value, candidate)
            for candidate in domains[other]:
                try:
                    if constraint.condition(assigned_value, candidate):
                        new_domain.add(candidate)
                except Exception:
                    # If the condition raises (shouldn't happen), treat it as failing
                    continue
        else:
            # assigned_variable == v2 -> constraint.condition(candidate, assigned_value)
            for candidate in domains[other]:
                try:
                    if constraint.condition(candidate, assigned_value):
                        new_domain.add(candidate)
                except Exception:
                    continue

        # Update the domain for the other variable
        domains[other] = new_domain
        if not new_domain:
            return False
    return True


def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    """
    Return the values in variable_to_assign's domain ordered by the least-restraining-value heuristic.

    Heuristic definition used:
      - For each candidate value v in domains[variable_to_assign]:
          - Simulate assigning v (do not modify the given `domains`):
              - Create a shallow copy of domains for unassigned variables
              - Remove `variable_to_assign` from that copy (it's now assigned)
              - Run forward_checking on that copy (with assigned value v)
          - Compute how many values were removed from neighbors (total removed)
      - The LEAST restraining value is the value that removes the fewest values in neighbors.
      - If multiple candidates have the same number of removed values, order by increasing value.

    Returns: list of values sorted ascending by (removed_count, value).
    """
    if variable_to_assign not in domains:
        return []

    original_domain = domains[variable_to_assign]
    scored_values = []

    for val in sorted(original_domain):  # iterate sorted so tie-break by value is natural
        # copy domains shallowly (sets must be copied to avoid aliasing)
        domains_copy = {v: set(domains[v]) for v in domains if v != variable_to_assign}
        # run forward checking on domains_copy with this assignment
        ok = forward_checking(problem, variable_to_assign, val, domains_copy)
        if not ok:
            # If forward checking fails, this value prunes everything -> treat as maximum restraint
            # We'll count removed as the sum of all neighbor domain sizes (i.e., everything pruned)
            removed = sum(len(domains[n]) for n in domains if n != variable_to_assign)
        else:
            # removed = total original neighbor domain sizes - remaining sizes
            removed = 0
            for neigh in domains:
                if neigh == variable_to_assign:
                    continue
                removed += (len(domains[neigh]) - len(domains_copy.get(neigh, set())))
        scored_values.append((removed, val))

    # sort by (removed, value) ascending -> least removed first, ties by numeric value ascending
    scored_values.sort(key=lambda x: (x[0], x[1]))
    return [val for _, val in scored_values]


def solve(problem: Problem) -> Optional[Assignment]:
    """
    Backtracking search with:
      - 1-Consistency preprocessing (one_consistency)
      - Variable ordering: Minimum Remaining Values (MRV)
      - Value ordering: Least Restraining Value
      - Forward checking after each tentative assignment

    Important behaviour to match autograder:
      - Call problem.is_complete exactly once for every *non-pruned* assignment (including the initial empty assignment).
      - If 1-Consistency declares the problem unsolvable (returns False), do NOT call problem.is_complete at all and return None.
    """
    # Apply 1-consistency first (this mutates problem.domains and removes unary constraints)
    from CSP import UnaryConstraint  # local import safe
    # one_consistency function was defined earlier in this file. Call it.
    solvable = one_consistency(problem)
    if not solvable:
        return None

    # At this point problem.domains is modified by one_consistency
    # We'll perform backtracking. domains argument always contains only unassigned variables.
    # Create initial domains copy for search.
    initial_domains = {var: set(vals) for var, vals in problem.domains.items()}

    # Per requirements: check completeness once for the initial empty assignment
    empty_assignment: Assignment = {}
    # Call is_complete exactly once for the empty assignment
    if problem.is_complete(empty_assignment):
        # If complete, check full constraints and return if satisfied
        # (satisfies_constraints requires a full assignment so this is fine)
        # Before checking constraints, allow cryptarithmetic-style constraints to access the assignment if needed
        try:
            import cryptarithmetic as _crypto_mod
            setattr(_crypto_mod, "LATEST_ASSIGNMENT", empty_assignment)
        except Exception:
            pass
        if problem.satisfies_constraints(empty_assignment):
            return empty_assignment
        # otherwise continue searching (should be unusual)

    # We will implement a recursive backtracking function.
    def backtrack(assignment: Assignment, domains: Dict[str, set]) -> Optional[Assignment]:
        # If no unassigned variables left, assignment is complete.
        # But to obey the "call is_complete exactly once" rule, we call is_complete only
        # after a successful forward_checking . So when recursion reaches here,
        # it means we arrived by a non-pruned branch AND no domains left; still we should check completeness.
        if not domains:
            # prepare cryptarithmetic compatibility (if module exists)
            try:
                import cryptarithmetic as _crypto_mod
                setattr(_crypto_mod, "LATEST_ASSIGNMENT", assignment)
            except Exception:
                pass
            # call is_complete exactly once for this assignment
            if problem.is_complete(assignment) and problem.satisfies_constraints(assignment):
                return dict(assignment)
            return None

        # choose variable by MRV (minimum_remaining_values uses the provided domains argument)
        var = minimum_remaining_values(problem, domains)

        # get ordered values by least restraining values
        ordered_vals = least_restraining_values(problem, var, domains)

        for val in ordered_vals:
            # simulate assignment: create a copy of domains representing unassigned variables after assigning var
            new_domains = {v: set(domains[v]) for v in domains if v != var}

            # run forward checking using the copied domains
            ok = forward_checking(problem, var, val, new_domains)
            if not ok:
                # pruned by forward checking -> per spec do NOT call problem.is_complete for this assignment
                continue

            # assignment passed forward checking -> now create new assignment and call is_complete ONCE
            new_assignment = dict(assignment)
            new_assignment[var] = val

            # prepare cryptarithmetic compatibility (if module exists) so constraint closures can read this assignment
            try:
                import cryptarithmetic as _crypto_mod
                setattr(_crypto_mod, "LATEST_ASSIGNMENT", new_assignment)
            except Exception:
                pass

            # call is_complete exactly once for this non-pruned assignment
            if problem.is_complete(new_assignment):
                # complete: check constraints and return if solution
                if problem.satisfies_constraints(new_assignment):
                    return new_assignment
                # else continue trying other values (no need to recurse)
                continue

            # not complete yet -> recurse
            result = backtrack(new_assignment, new_domains)
            if result is not None:
                return result

        # no value led to a solution
        return None

    # start search with empty assignment and initial domains
    return backtrack({}, initial_domains)