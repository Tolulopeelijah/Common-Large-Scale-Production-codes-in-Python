## Attribute descriptor ##
class TypedField:
    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        return obj.__dict__[self.name]
    
    def __set__(self, obj, value):
        if type(value) != self.expected_type:
            raise TypeError(f"value has a type of {type(value)} instead of {self.expected_type}")
        obj.__dict__[self.name] = value


    
