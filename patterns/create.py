from quopri import decodestring
from copy import deepcopy
from .behavioral import Subject, FileWriter
from datetime import datetime
from .archsystem_unit_of_work import DomainObject
from sqlite3 import connect


class User:

    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User, DomainObject):

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class CoursePrototype:

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class BeginnerCourse(Course):
    pass


class ProfiCourse(Course):
    pass


class CourseFactory:
    types = {
        'beginner': BeginnerCourse,
        'profi': ProfiCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Engine:
    def __init__(self):
        self.teachers = []
        mapper = MapperRegistry.get_current_mapper('student')
        self.students = mapper.all()
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'No category with id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name):
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'{datetime.now()} log => {text}'
        # print('log => ', text)
        self.writer.write(text)


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record id = {id} not exist')

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBDeleteException(e.args)


connection = connect('arch.sqlite3')


class MapperRegistry:
    mappers = {
        'student': StudentMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        print(f'MapperRegistry.mappers[name] {MapperRegistry.mappers[name]}')
        return MapperRegistry.mappers[name](connection)


class RecordNotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(f'Record not founf {msg}')


class DBUpdateException(Exception):
    def __init__(self, msg):
        super().__init__(f'DB update error {msg}')


class DBCommitException(Exception):
    def __init__(self, msg):
        super().__init__(f'DB commit error {msg}')


class DBDeleteException(Exception):
    def __init__(self, msg):
        super().__init__(f'DB delete error {msg}')
