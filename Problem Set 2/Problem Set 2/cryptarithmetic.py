from typing import Tuple
import re
from itertools import product
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
        problem.variables=[]
        problem.constraints=[]
        problem.domains={}
        chars=set(LHS0+LHS1+RHS)
        problem.variables.extend(chars)
        # For the letters, the domain can only contain integers in the range [0,9].
        problem.domains = {char:{0,1,2,3,4,5,6,7,8,9}for char in chars}
        # Add auxiliary variables for carries
        max_length=max(len(LHS1),len(LHS0)) if (len(RHS)>=max(len(LHS1),len(LHS0))) else max(len(LHS1),len(LHS0))-1
        carry_vars = [f"C{i}" for i in range(max_length+1)]  
        problem.variables.extend(carry_vars)
        # Carry is always 0 or 1
        for carry in carry_vars:
            problem.domains[carry] = {0, 1}  
            
        problem.constraints = []
        # 1. Add unary constraints for leading digits (can't be 0)
        for word in [LHS0, LHS1, RHS]:
            leading_letter = word[0]
            problem.constraints.append(
                UnaryConstraint(leading_letter, lambda x: x != 0)
            )

        # 2. Add binary constraints for unique digits
        for i, letter1 in enumerate(chars):
            for letter2 in list(chars)[i + 1:]:
                problem.constraints.append(
                    BinaryConstraint((letter1, letter2), lambda x, y: x != y)
                )

        # 3. Add a global constraint for the mathematical equation (column-wise addition constraints)

        # if the length of RHS > length of LHS0&length of LHS1:
        # Then most significant in RHS = most significant carry
        if (len(RHS)>max(len(LHS0),len(LHS1))):
            problem.constraints.append(BinaryConstraint((RHS[0],carry_vars[max_length]),lambda a,b:a==b))

        # Constraint to ensure column addition is valid
        def mega_constraint(mega1, mega2):
                letter1, letter2,carry_in = mega1 
                result,carry_out = mega2  
                return letter1 + letter2 +carry_in == result + 10*carry_out
        # Looping from least most
        i=-1
        # Within the loop multiply i by -1 to make comparsions understandable 
        # We will make the lHS of summation equation as mega_variable1 
        # RHS of summation equation as mega_variable2
        while(i*-1 <=min(len(LHS0),len(LHS1))):
            letter1 = LHS0[i]
            letter2 = LHS1[i]
            result = RHS[i]
            carry_in = carry_vars[i*-1 - 1] if i !=-1 else '0'
            carry_out = carry_vars[i*-1] 
            
            # Adding the least most column -> no carry_in
            if (i==-1):
                mega_variable1=(letter1,letter2)
                mega_variable2=(result,carry_out)
                problem.variables.append(mega_variable1)
                problem.variables.append(mega_variable2)
                # Add domain for mega_variable1
                problem.domains[mega_variable1] = list(
                    (x, y) for x, y in product(
                        problem.domains[letter1],
                        problem.domains[letter2],
                    )
                )
                # Add domain for mega_variable2
                problem.domains[mega_variable2] = list(
                    (x, y) for x, y in product(
                        problem.domains[result],
                        problem.domains[carry_out],
                    )
                )
                # Constraints between mega_variable1 and mega_variable2 
                # and constraints between each mega_variable and its components 
                problem.constraints.append(BinaryConstraint((mega_variable1,mega_variable2),lambda a,b: a[0]+a[1]==b[0]+10*b[1]))
                problem.constraints.append(BinaryConstraint((mega_variable1,letter1),lambda a,b:a[0]==b))
                problem.constraints.append(BinaryConstraint((mega_variable1,letter2),lambda a,b:a[1]==b))
                problem.constraints.append(BinaryConstraint((mega_variable2,result),lambda a,b:a[0]==b))
                problem.constraints.append(BinaryConstraint((mega_variable2,carry_out),lambda a,b:a[1]==b))
            else:
            # Otherwise there's carry_in
                mega_variable1=(letter1,letter2,carry_in)
                mega_variable2=(result,carry_out)
                problem.variables.append(mega_variable1)
                problem.variables.append(mega_variable2)
                # Add domain for mega_variable1
                problem.domains[mega_variable1] = {
                    (x, y,z) for x, y,z in product(
                        problem.domains[letter1],
                        problem.domains[letter2],
                        problem.domains[carry_in]
                    )
                }
                # Add domain for mega_variable2
                problem.domains[mega_variable2] = {
                    (x, y) for x, y in product(
                        problem.domains[result],
                        problem.domains[carry_out],
                    )
                }
                # Constraints between mega_variable1 and mega_variable2 
                # and constraints between each mega_variable and its components 
                problem.constraints.append(BinaryConstraint((mega_variable1,mega_variable2),mega_constraint))
                problem.constraints.append(BinaryConstraint((mega_variable1,letter1),lambda a,b:a[0]==b))
                problem.constraints.append(BinaryConstraint((mega_variable1,letter2),lambda a,b:a[1]==b))
                problem.constraints.append(BinaryConstraint((mega_variable1,carry_in),lambda a,b:a[2]==b))
                problem.constraints.append(BinaryConstraint((mega_variable2,result),lambda a,b:a[0]==b))
                problem.constraints.append(BinaryConstraint((mega_variable2,carry_out),lambda a,b:a[1]==b))
            i=i-1

        # Looping on remaining letters if one word has length > other word
        if (len(LHS1)>len(LHS0)):
            while(i*-1 <= len(LHS1)):
                letter2 = LHS1[i]
                result = RHS[i]
                carry_in = carry_vars[i*-1 - 1] 
                carry_out = carry_vars[i*-1] 
                mega_variable1=(letter2,carry_in)
                mega_variable2=(result,carry_out)
                problem.variables.append(mega_variable1)
                problem.variables.append(mega_variable2)
                # Add domain for mega_variable1
                problem.domains[mega_variable1] = {
                    (x, y) for x, y in product(
                        problem.domains[letter2],
                        problem.domains[carry_in]
                    )
                }
                # Add domain for mega_variable2
                problem.domains[mega_variable2] = {
                    (x, y) for x, y in product(
                        problem.domains[result],
                        problem.domains[carry_out],
                    )
                }
                # Constraints between mega_variable1 and mega_variable2 
                # and constraints between each mega_variable and its components 
                problem.constraints.append(BinaryConstraint((mega_variable1,mega_variable2),lambda a,b:a[0]+a[1]==b[0]+10*b[1]))
                problem.constraints.append(BinaryConstraint((mega_variable1,letter2),lambda a,b:a[0]==b))
                problem.constraints.append(BinaryConstraint((mega_variable1,carry_in),lambda a,b:a[1]==b))
                problem.constraints.append(BinaryConstraint((mega_variable2,result),lambda a,b:a[0]==b))
                problem.constraints.append(BinaryConstraint((mega_variable2,carry_out),lambda a,b:a[1]==b))
                i=i-1
        else:
            while(i*-1 <= len(LHS0)):
                letter1 = LHS0[i]
                result = RHS[i]
                carry_in = carry_vars[i*-1 - 1] 
                carry_out = carry_vars[i*-1] 
                mega_variable1=(letter1,carry_in)
                mega_variable2=(result,carry_out)
                problem.variables.append(mega_variable1)
                problem.variables.append(mega_variable2)
                # Add domain for mega_variable1
                problem.domains[mega_variable1] = {
                    (x, y) for x, y in product(
                        problem.domains[letter1],
                        problem.domains[carry_in]
                    )
                }
                # Add domain for mega_variable2
                problem.domains[mega_variable2] = {
                    (x, y) for x, y in product(
                        problem.domains[result],
                        problem.domains[carry_out],
                    )
                }
                # Constraints between mega_variable1 and mega_variable2 
                # and constraints between each mega_variable and its components 
                problem.constraints.append(BinaryConstraint((mega_variable1,mega_variable2),lambda a,b:a[0]+a[1]==b[0]+10*b[1]))
                problem.constraints.append(BinaryConstraint((mega_variable1,letter1),lambda a,b:a[0]==b))
                problem.constraints.append(BinaryConstraint((mega_variable1,carry_in),lambda a,b:a[1]==b))
                problem.constraints.append(BinaryConstraint((mega_variable2,result),lambda a,b:a[0]==b))
                problem.constraints.append(BinaryConstraint((mega_variable2,carry_out),lambda a,b:a[1]==b))
                i=i-1

        
        return problem
    

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())