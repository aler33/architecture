from datetime import datetime
from views import Index, Course, Category, Contact, CreateCourse, CreateCategory, CopyCourse


def add_date(request):
    request['date'] = datetime.now()


fronts = [add_date]


routes = {
    '/': Index(),
    '/course/': Course(),
    '/category/': Category(),
    '/contact/': Contact(),
    '/create_course/': CreateCourse(),
    '/create_category/': CreateCategory(),
    '/copy_course/': CopyCourse(),
    '/index/': Index(),
}
