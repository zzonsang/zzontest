def sum(a, b):
    return a+b

def safe_sum(a, b):    
    if type(a) != type(b):
        print "Not supported."
        return
    else:
        result = sum(a, b)
    return result