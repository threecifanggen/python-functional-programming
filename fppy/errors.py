class NoOtherCaseError(Exception):
    pass

class ConstError(TypeError): pass

class NotVoidFunctionError(TypeError): pass

class NothingHasNoSuchMethod(Exception): pass