def cons(head, tail):
    def helper():
        return (head, tail)
    return helper
    
head = lambda cons_list: cons_list()[0]
tail = lambda cons_list: cons_list()[1]

def print_cons_with_brackets(cons_list) -> str:
    if cons_list == ():
        return "()"
    else:
        return f"({head(cons_list)}, {print_cons_with_brackets(tail(cons_list))})"

def print_cons(cons_list) -> str:
    if cons_list == ():
        return "nil"
    else:
        return f"{head(cons_list)}, {print_cons(tail(cons_list))}"

def map_cons(f, cons_list):
    if cons_list == ():
        return ()
    else:
        return cons(f(head(cons_list)), map_cons(f, tail(cons_list)))

def filter_cons(f, cons_list):
    if cons_list == ():
        return ()
    else:
        hd, tl = head(cons_list), tail(cons_list)
        if f(hd):
            return cons(hd, filter_cons(f, tl))
        else:
            return tl

def fold_left_cons(f, cons_list, init):
    if tail(cons_list) == ():
        return f(init, head(cons_list))
    else:
        return fold_left_cons(f, tail(cons_list), f(init, head(cons_list)))
