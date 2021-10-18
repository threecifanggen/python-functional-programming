==================
API Reference
==================


基本函数
======================

函数组合
--------------------

.. autofunction:: fppy.base.compose
.. autofunction:: fppy.base.I
.. autofunction:: fppy.base.and_then


函数修饰器
--------------------

.. autofunction:: fppy.base.F_


常量与惰性
====================

定义常量
------------

.. automodule:: fppy.const

惰性
-------------

.. autofunction:: fppy.lazy_evaluate.lazy_property
.. autoclass:: fppy.lazy_evaluate.LazyValue


组合子
======================

.. autofunction:: fppy.combinator.Y
.. autofunction:: fppy.combinator.Z


列表类
===========================


通过元组的实现
------------------------

.. autofunction:: fppy.cons_list_base.cons
.. autofunction:: fppy.cons_list_base.head
.. autofunction:: fppy.cons_list_base.tail


常用函数
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: fppy.cons_list_base.map_cons
.. autofunction:: fppy.cons_list_base.map_cons_curry
.. autofunction:: fppy.cons_list_base.filter_cons
.. autofunction:: fppy.cons_list_base.filter_cons_curry
.. autofunction:: fppy.cons_list_base.fold_left_cons
.. autofunction:: fppy.cons_list_base.fold_left_cons_curry
.. autofunction:: fppy.cons_list_base.equal_cons