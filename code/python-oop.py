class Employee:
    """所有员工的基类"""
    empCount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print("Total Employee %d" % Employee.empCount)

    def displayEmployee(self):
        print("Name : ", self.name, ", Salary: ", self.salary)


class Test:
    def prt(self):
        print(self)
        print(self.__class__)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __del__(self):
        class_name = self.__class__.__name__
        print(class_name, "销毁")


class Parent:
    parentAttr = 100

    def __init__(self):
        print("调用父类构造函数")

    def parentMethod(self):
        print('调用父类方法')

    def setAttr(self, attr):
        Parent.parentAttr = attr

    def getAttr(self):
        print("父类属性 :", Parent.parentAttr)

    def myMethod(self):
        print('调用父类方法')


class Child(Parent):
    def __init__(self):
        print("调用子类构造方法")

    def childMethod(self):
        print('调用子类方法')

    def myMethod(self):
        print('调用子类方法')


# !/usr/bin/python
# -*- coding: UTF-8 -*-

class JustCounter:
    __secretCount = 0  # 私有变量
    publicCount = 0  # 公开变量

    __site = "www.runoob.com"  # 私有变量

    def count(self):
        self.__secretCount += 1
        self.publicCount += 1
        print(self.__secretCount)

class Vector:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return 'Vector (%d, %d)' % (self.a, self.b)

    def __add__(self, other):
        return Vector(self.a + other.a, self.b + other.b)



if __name__ == "__main__":
    # 创建 Employee 类的第一个对象
    emp1 = Employee("Zara", 2000)
    emp2 = Employee("Manni", 5000)
    emp1.displayEmployee()
    emp2.displayEmployee()
    print("Total Employee %d" % Employee.empCount)

    # self代表类的实例，而非类
    t = Test()
    t.prt()

    # 访问属性
    print(hasattr(emp1, 'salary'))  # 如果存在 'salary' 属性返回 True。
    print(getattr(emp1, 'salary'))  # 返回 'salary' 属性的值
    setattr(emp1, 'salary', 7000)  # 设置 'salary' 属性
    print(getattr(emp1, 'salary'))  # 再次返回 'salary' 属性的值
    delattr(emp1, 'salary')  # 删除 'salary' 属性
    print(hasattr(emp1, 'salary'))  # 再次检查 'salary'

    # Python内置类属性
    print("Employee.__doc__:", Employee.__doc__)
    print("Employee.__name__:", Employee.__name__)
    print("Employee.__module__:", Employee.__module__)
    print("Employee.__bases__:", Employee.__bases__)
    print("Employee.__dict__:", Employee.__dict__)

    # 析构函数
    pt1 = Point()
    pt2 = pt1
    pt3 = pt1
    print(id(pt1), id(pt2), id(pt3))
    del pt1
    del pt2
    del pt3

    # 继承
    c = Child()  # 实例化子类
    c.childMethod()  # 调用子类的方法
    c.parentMethod()  # 调用父类的方法
    c.setAttr(200)  # 再次调用父类的方法 - 设置属性值
    c.getAttr()  # 再次调用父类的方法 - 获取属性值

    # 子类
    print(issubclass(Child, Parent))  # Child 是否是 Parent 的子类
    print(isinstance(c, Child))  # c 是否是 Child 类的实例
    print(isinstance(c, Parent))  # c 是否是 Parent 类的实例

    # 方法重写
    c.myMethod()  # 子类重写父类方法后，调用子类方法
    super(Child, c).myMethod()  # 使用 super() 调用父类的方法

    # 运算符重载
    v1 = Vector(2, 10)
    v2 = Vector(5, -2)
    print(v1 + v2)  # Vector (7, 8)

    # 私有变量
    counter = JustCounter()
    counter.count()  # 输出 1
    counter.count()  # 输出 2
    print(counter.publicCount)  # 输出 2
    # print(counter.__secretCount)  # 报错，无法访问私有变量
    print(counter._JustCounter__site)  # 通过 _类名__属性名 来访问私有属性