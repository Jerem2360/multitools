

def Generic(clas: type):

    def __class_getitem__(cls, item):
        args = item
        if not isinstance(item, tuple):
            args = (item,)

        if hasattr(cls, 'call'):
            return cls.call(*args)
        raise AttributeError("Generic types must define a 'call(items)' class method.")

    clas.__class_getitem__ = classmethod(__class_getitem__)

    return clas


class SubTypeCheck:
    def __init__(self, tp, sub_type):
        self.subtype = sub_type
        self.tp = tp

    def __instancecheck__(self, instance):
        self.tp.check(instance, self.subtype)
