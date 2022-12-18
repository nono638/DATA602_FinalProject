def CountingDictAdd(dictParam : dict, toAdd, verbose = False):
    """Takes a dict param and a toAdd param.
    Keeps a count of how many times the toAdd Param is being added to the dictParam"""
    if type(dictParam) != dict:
        if verbose:
            print("A non-dictionary object was passed to CountingDictAdd... returning None")
        return None
    if toAdd in dictParam:
        dictParam[toAdd] += 1
    else:
        dictParam[toAdd] = 1
    return dictParam