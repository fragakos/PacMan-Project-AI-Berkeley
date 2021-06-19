from util import first, count, argmin_random_tie
from operator import neg
import time
from sortedcontainers import SortedSet
import collections
import random

which_file = '2-f24'

var_fd = open("rlfap/var{}.txt".format(which_file), "r")
vars_with_dom = []
total_vars = int(var_fd.readline())
for single_var in range(total_vars):
    temp_var_list = []
    temp_var = var_fd.readline().strip('\n').split()
    for i in temp_var:
        i = int(i)
        temp_var_list.append(i)
    vars_with_dom.append(temp_var_list)
var_fd.close()


var_fd = open("rlfap/var{}.txt".format(which_file), "r")
variables = []
total_vars = int(var_fd.readline())
for single_var in range(total_vars):
    temp_var_list = []
    temp_var = var_fd.readline().strip('\n').rsplit(" ", 1)[0]
    # for i in temp_var:
    #     i = int(i)
    #     temp_var_list.append(i)
    variables.append(int(temp_var))
# for var in variables:
#     var.pop(0)
var_fd.close()

dom_fd = open("rlfap/dom{}.txt".format(which_file), "r")
domains_temp = {}
total_domains = int(dom_fd.readline())
for single_domain in range(total_domains):
    temp_dom_list = []
    temp_dom = dom_fd.readline().strip('\n').split()
    for i in range(len(temp_dom)):
        if i != 0 and i != 1:
            temp_dom[i] = int(temp_dom[i])
            temp_dom_list.append(temp_dom[i])
    domains_temp[single_domain] = temp_dom_list
  
dom_fd.close()
domains = {v[0]: domains_temp[v[1]] for v in vars_with_dom}

ctr_fd = open("rlfap/ctr{}.txt".format(which_file), "r")
ctrs = []
total_ctrs = int(ctr_fd.readline())
for single_ctr in range(total_ctrs):
    temp_ctr = ctr_fd.readline().strip('\n').split()
    for i in range(len(temp_ctr)):
        if i != 2:
            temp_ctr[i] = int(temp_ctr[i])
    ctrs.append(temp_ctr)
ctr_fd.close()


neighbors = {}
for var in variables:
    temp_list = []
    for con in ctrs:
        if con[0] == var:
            temp_list.append(con[1])
        elif con[1] == var:
            temp_list.append(con[0])
    neighbors[var] = temp_list            

def constraints(var1, value1, var2, value2):
        for i in ctrs:
            if i[0] == var1 and i[1] == var2:
                token = i[2].strip()
                k = i[3]
                if token == '>':
                    if abs(value1 - value2) > k:
                        return True  
                    else:
                        return False      
                elif token == '=':
                    if abs(value1 - value2) == k:
                        return True
                    else:
                        return False
            elif i[0] == var2 and i[1] == var1:
                token = i[2].strip()
                k = i[3]
                if token == '>':
                    if abs(value2 - value1) > k:
                        return True  
                    else:
                        return False      
                elif token == '=':
                    if abs(value2 - value1) == k:
                        return True
                    else:
                        return False       
        return True                                      

class CSP():

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        #super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0
        self.checks = 0

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))
   
    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print(assignment)    

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)    

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

##----------------------------------------------------------------------##-------------------------------------------------------------##
# End of class CSP #
       
def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: num_legal_values(csp, var, assignment))


def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])

def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def lcv(var, assignment, csp):
    """Least-constraining-values heuristic."""
    return sorted(csp.choices(var), key=lambda val: csp.nconflicts(var, val, assignment))

def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
                csp.checks+=1
            if not csp.curr_domains[B]:
                return False
    return True

def no_arc_heuristic(csp, queue):
    return queue


def dom_j_up(csp, queue):
    return SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))


def AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # CSP is satisfiable


def revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            csp.checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True
    return revised, checks

def mac(csp, var, value, assignment, removals, constraint_propagation=AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)    

def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result

def min_conflicts(csp, max_steps=100000):
    """Solve a CSP by stochastic Hill Climbing on the number of conflicts."""
    # Generate a complete assignment for all variables (probably with conflicts)
    csp.current = current = {}
    for var in csp.variables:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
        print(i)
    return None


def min_conflicts_value(csp, var, current):
    """Return the value that will give var the least number of conflicts.
    If there is a tie, choose at random."""
    return argmin_random_tie(csp.domains[var], key=lambda val: csp.nconflicts(var, val, current))    
          
csp1 = CSP(variables, domains, neighbors, constraints)
start_time = time.time()
result = backtracking_search(csp1 ,select_unassigned_variable = mrv ,order_domain_values = lcv ,inference = forward_checking)  
#result = backtracking_search(csp1 ,select_unassigned_variable = mrv ,order_domain_values = lcv ,inference = mac) 
#result = min_conflicts(csp1)
print(collections.OrderedDict(sorted(result.items())))  
#print(result)
print("--- %s seconds ---" % (time.time() - start_time))
print(csp1.nassigns)
print(csp1.checks)