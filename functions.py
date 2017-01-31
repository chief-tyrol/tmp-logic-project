FUNCTIONS = {"and", "or", "implies","not","nor","xor","nand"}


def land(p, q):
    return p and q
    
def lor(p, q):
    return p or q
    
def limplies(p, q):
    if not p:
        return True
    return p and q
    
def lnot(p):
    return not p
    
def lnor(p, q):
    if p or q:
        return False
    return True
    
def lxor(p, q):
    if p and not q or q and not p:
        return True
    return False
    
def lnand(p, q):
    if p and q:
        return False
    return True
    

def get_func(name):
    return _mapper[name]
_mapper = {
    "and":land,
    "or":lor,
    "implies":limplies,
    "nor":lnor,
    "xor":lxor,
    "nand":lnand
        }    
