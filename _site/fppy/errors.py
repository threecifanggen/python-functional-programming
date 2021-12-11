"""错误类
"""
class NoOtherCaseError(Exception):
    """无其他可能性错误
    """

class ConstError(TypeError):
    """常量错误
    """

class NotVoidFunctionError(TypeError):
    """不是无参数函数错误
    """

class NothingHasNoSuchMethod(Exception):
    """Nothing不包含此方法错误
    """
