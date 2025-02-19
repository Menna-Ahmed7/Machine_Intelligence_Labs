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
    #TODO: Write this function
    for constraint in problem.constraints:
        # Working only on constraints involving the assigned variable
        if isinstance(constraint, BinaryConstraint) and assigned_variable in constraint.variables:
            other_variable = constraint.get_other(assigned_variable)
            
            # Skip If the other variable has no domain 
            if other_variable in domains:
                new_domain=set()
                # Update the other variable's domain to only include the values that 
                # satisfy the binary constraint with the assigned variable.
                for value in domains[other_variable]:
                    if(constraint.is_satisfied({assigned_variable:assigned_value,other_variable:value})):
                        new_domain.add(value)
                
                # If the domain of the other variable becomes empty, return False
                if not new_domain:
                    return False
                
                domains[other_variable] = new_domain
    
    # If no domain becomes empty, return True
    return True

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function
    list_values=[]
    for value in domains[variable_to_assign]:
        does_restrict_any=False
        count=0
        for constraint in problem.constraints:
            # Working only on constraints involving the assigned variable
            if isinstance(constraint, BinaryConstraint) and variable_to_assign in constraint.variables:
                other_variable = constraint.get_other(variable_to_assign)
                # Skip If the other variable has no domain 
                if other_variable in domains:
                    # Try the domain of the other variable
                    for other_value in domains[other_variable]:
                        if(constraint.is_satisfied({variable_to_assign:value,other_variable:other_value})):
                            count+=1
                    # No value in other variable's domain can be assigned to it to keep satsifying the constraint 
                    if count==0:
                        does_restrict_any=True
                        break
        if not does_restrict_any:
            list_values.append((value,count))
    # Sort values by count (descending), then by value (ascending)
    return [value for value, _ in sorted(list_values, key=lambda x: (-x[1], x[0]))]

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #TODO: Write this function
    if (one_consistency(problem)==False):
        return None
    def recursive_backtrack(assignment:Assignment,domains):
        if (problem.is_complete(assignment)):
            return assignment
        # Exclude already assigned variables
        unassigned_variables = {var: domains[var] for var in problem.variables if var not in assignment}
        # Select the next variable using the MRV
        variable = minimum_remaining_values(problem, unassigned_variables)
        if variable is None:
                return None
        for value in least_restraining_values(problem,variable,domains):
            # Make a deep copy of the domains to avoid modifying global state
            local_domains={}
            # Remove the selected variable from domain to prevent selecting it again later
            for var,values in domains.items():
                if var!=variable:
                    local_domains[var]=values
            # Assign the value to the variable and apply forward checking
            if forward_checking(problem, variable, value, local_domains):
                assignment[variable] = value
                # Recurse with the updated assignment
                result = recursive_backtrack(assignment,local_domains)
                if result is not None:
                    return result

                del assignment[variable]
        return None  # No valid assignment found
    
    # Start with an empty assignment
    initial_assignment: Assignment = {}
    # Perform recursive backtracking and return the solution (or None if no solution is found)
    return recursive_backtrack(initial_assignment,problem.domains)
