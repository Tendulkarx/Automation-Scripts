

def remove_duplicates(the_list):
    [i for n, i in enumerate(the_list) if i not in the_list[n + 1:]]
    return the_list
