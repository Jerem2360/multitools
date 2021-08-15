

def getno(dict_: dict, index: int):
    if hasattr(dict_, '__getno__'):
        return dict_.__getno__(index)
    counter = 0
    for item in dict_:
        if counter == index:
            return item, dict_[item]
        counter += 1
    raise IndexError('Dictionary has no index {0}'.format(index))
