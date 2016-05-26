#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one remaining variable)
        we look for unary constraints of the csp (constraints whose scope contains
        only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
         
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
#IMPLEMENT

    pruned = []
    isDeadend = False
    
    if not newVar:
        cons = csp.get_all_cons()
        for con in cons:
            scope = con.get_scope()
            if len(scope) == 1:
                result = FCCheck(con, scope[0])
                pruned.extend(result[1])
                if not result[0]:
                    isDeadend = True
                    break
            
    
    cons = csp.get_all_cons()
    for con in cons:
        scope = con.get_scope()
        if con.get_n_unasgn() == 1:
            result = FCCheck(con, con.get_unasgn_vars()[0])
            pruned.extend(result[1])
            if not result[0]:
                isDeadend = True
                break         
    if isDeadend:
        return (False, pruned)
    return (True, pruned)    
                

def FCCheck(C, x):
    '''
    (Constraint, Variable) -> (Bool, list of tuple(Varialbe, Value))
    
    Given a constraint C and a variable x, return True if the current domain
    size of x is not zero; False otherwise. Also return a list of (var, val)
    tuples that pruned.
    '''
    pruned = []
    cur_dom = x.cur_domain()
    for val in cur_dom:
        if not C.has_support(x, val):
            x.prune_value(val)
            pruned.append((x, val))
            
    if not x.cur_domain_size():
        return (False, pruned)    
    return (True, pruned)

    
def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
#IMPLEMENT
    
    queue = []
    pruned = []
    cons = csp.get_all_cons()

    if not newVar:
        queue = cons.copy()
    else:
        queue = csp.get_cons_with_var(newVar).copy()

    # For looping queue use an indicator count. It avoids keep append and
    # remove items in the queue list that may slow down the program.
    count = 0
    while count < len(queue):
        
        con = queue[count]       
        scope = con.get_scope()

        for i in range(len(scope)):
            var = scope[i]
            curdom = var.cur_domain()
            found = False
            for val in curdom:
                if con.has_support(var, val):
                    continue
                else:
                    found = True
                    var.prune_value(val)
                    pruned.append((var, val))
                    if not var.cur_domain_size():
                        queue = []
                        return (False, pruned)

            if found:
                cons = csp.get_cons_with_var(var)
                for c in cons:
                    if c not in queue[count:]:
                        queue.append(c)
        count += 1

    return (True, pruned)