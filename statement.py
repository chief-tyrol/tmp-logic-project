import functions
import FullBiTree as Tree
from itertools import combinations as combo
_FUNCTIONS_PARSED = "functions parsed"
_VARIABLES_PARSED = "variables parsed"
_SYNTAX_VERIFIED = "syntax verified"

class statement:
    
    def __init__(self, assertion):
        if not type(assertion) == str:
            raise Exception("Statement must be a string")
            
        self.FUNC = 1
        self.VAR = 0
        self.NONE = -1
        self.items = dict()
        self._variables = dict()
        # a set of completed actions
        self._completed = set()
        
        # raw data to parse
        self._raw = assertion.lower()
        
        # raw data, kept for posterity
        self._original = assertion
        
        print "verifying syntax...",
        # verify the basic syntax
        self._verify_syntax()
        print "Done"
        
        print "parsing function...",
        # parse the function and
        self._parse()
        print "Done"
        
        print "classifying variables...",
        # parse the function
        self._classify()
        print "Done"
        
        print "building logical tree...",
        #build the tree
        self._build_tree()
        print "Done"
        
        print "running simulations...",
        # run simulations
        self._simulate()
        print "Done"
        
        print "printing results..."
        self.print_results()
        print "Done"
        
        
    def is_var(self, var):
        return self.items[var] == self.VAR
        
        
    def print_results(self):
        for line in self.results:
            print line
            
            
    def _simulate(self):
        size = len(self._raw)
        def shorten(value):
            """
            Converts a boolean into either "T" or "F"
            """
            if value:
                return "T"
            return "F"

        self.results = []
        nodes = [value for value in self.items.keys() if self.items[value] == self.VAR]
        
        vals = {}
        
        header = ""
        nodes.sort()
        for node in nodes:
            vals[node] = False
            header += "{} | ".format(node)

        header +=  self._raw
        

        for i in xrange(len(nodes) + 1):
            for comb in combo(nodes, i):
                for node in vals.keys():
                    if node in comb:
                        vals[node] = True
                    else:
                        vals[node] = False

                val = self._eval(vals)
                line = ""
                for node in nodes:
                    line += "{} | ".format(shorten(vals[node]))
                line += " " * (size / 2 )
                line += shorten(val)
                line += " " * (size / 2)
                self.results.append(line)

        self.results.sort()
        self.results.reverse()

        self.results.insert(0, "-" * len(header))
        self.results.insert(0, header)
        
        #print nodes
        pass
        
        
        
    def _eval(self, node_states):
        def evalt(tree):
            if tree.is_leaf():
                return node_states[tree.get_name()]
            else:
                func = functions.get_func(tree.get_name())
                return func(evalt(tree.get_left_child()), evalt(tree.get_right_child()))
        return evalt(self.tree)
        
    def is_func(self, func):
        return func in functions.FUNCTIONS
        
        
    def _build_tree(self):
        
        def num_vars(func):
            count = 0
            for value in func:
                if self.is_var(value):
                    count += 1
            return count
            
        def split(func):
            
            def clean(func):
                if func[0] == "(" and func[-1] == ")":
                    return func[1:-1]
                return func
                
            a, b, f = [], [], None
            lvl = 0
            prev_lvl = float("inf")
            split_point = float("inf")
            for idx in xrange(len(func)):
                value = func[idx]
                if value == "(":
                    lvl += 1
                elif value == ")":
                    lvl -= 1
                if self.is_func(value):
                    if lvl < prev_lvl:
                        split_point = idx
                        prev_lvl = lvl
            a = clean(func[0:split_point])
            b = clean(func[split_point +1:])
            f = func[split_point]
            
            return a, b, f
            
            
        def get_var(func):
            for idx in xrange(len(func)):
                value = func[idx]
                if self.is_var(value):
                    return value
                    
            
        def build_tree(lvl, func, var):
            #print "build tree called with ({}, {}, {})".format(lvl, func, var)
            if num_vars(func) <= 1:
                #print (lvl, get_var(func))
                return Tree.FullBiTree(get_var(func))
            else:
                a, b, f = split(func)
                

                #a_name = self._next_name()
                #self._variables[a_name] = a

                #b_name = self._next_name()
                #self._variables[b_name] = b
                
                
                #var.append((lvl, a, b, f))
                
                return Tree.FullBiTree(f, build_tree(lvl + 1, a, var), build_tree(lvl + 1, b, var))
        asdf = Tree.FullBiTree("top")
        asdf = build_tree(0, self.parsed_function, asdf)
        #print "printing tree: {}".format(asdf)
        self.tree = asdf
                
                
    def _next_name(self):
        
        def is_taken(name):
            if str(name) in self._variables.keys():
                return True
            return False
            
        name = 0
        while is_taken(name):
            name += 1
        return str(name)
    
    
    
    def _parse(self):

        # an array of the entries in the list
        self.parsed_function = []
                
        start_string = 0
        in_string = False
        
        for i in xrange(len(self._raw)):
            char = self._raw[i]
            
            if not in_string and char.isalpha():
                start_string = i
                in_string = True
                
            if in_string and not char.isalpha():
                self.parsed_function.append(self._raw[start_string: i])
                in_string = False
                
            if not in_string and not char == " ":
                self.parsed_function.append(char)
                
            if in_string and i == len(self._raw) - 1:
                self.parsed_function.append(self._raw[start_string: i + 1])
        
        #print self.parsed_function
        pass
                
                
    def _classify(self):
        
        def _is_func(var):
            return var in functions.FUNCTIONS
            
        def _is_none(var):
            return var in "( )"
            
        def next_var(idx):
            lvl = 0
            start = idx
            if self.is_var(self.parsed_function[idx + 1]):
                return [self.parsed_function[idx + 1]]
            for i in xrange(idx + 1, len(self.parsed_function)):
                var = self.parsed_function[i]
                if var == "(":
                    lvl += 1
                elif var == ")":
                    lvl -= 1
                if lvl == 0:
                    return self.parsed_function[idx + 1:i +1]
                    
                    
        self.classed = []
        
        for unclass in self.parsed_function:
            if _is_none(unclass):
                self.items[unclass] = self.NONE
            elif _is_func(unclass):
                self.items[unclass] = self.FUNC
            else:
                self.items[unclass] = self.VAR
                
        for idx in xrange(len(self.parsed_function)):
            item = self.parsed_function[idx]
            if item == "not":
                temp = next_var(idx)
                #print "old function: ",self.parsed_function
                #print "new var:",temp
                asdf = self.parsed_function[0:idx] + ["("] + temp + ["nand"] + temp + [")"] + self.parsed_function[idx + len(temp) + 1:]
                #print "new function: ", asdf
                self.parsed_function = asdf
                self._classify()
        #for i in xrange(len(self.classed)):
        #    print "{}\t: {}".format(self.classed[i],self.parsed_function[i])
        pass

            
        
        
    
    def _verify_syntax(self):
        """
        Verify the basic syntax.
        i.e. for each '(', there is a ')'
        """
        # verify the number of parenthases
        extra_parens = 0
        for char in self._raw:
            if char == "(":
                extra_parens += 1
            elif char == ")":
                extra_parens -= 1
            # verify that the character is allowed
            if not char.isalpha() and char not in "( )":
                raise Exception("Invalid character: {}. Only letters, '(', and ')' are allowed".format(char))
        if extra_parens > 0:
            raise Exception("Invalid number of parentheses: found {} extra parentheses".format(extra_parens))
            
        
        self._completed.add(_SYNTAX_VERIFIED)
        
