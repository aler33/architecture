from alex_framework.templator import render
from patterns.create import Engine, Logger
from patterns.strucktur import AppRoute, Debug
from patterns.behavioral import ListView, CreateView, SMSNotifier, EmailNotifier, BaseSerializer

site = Engine()
logger = Logger('main')
sms_notifier = SMSNotifier()
email_notifier = EmailNotifier()

routes = {}


@AppRoute(routes=routes, url=['/index/', '/'])
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


@AppRoute(routes=routes, url='/course/')
class Course:
    @Debug(name='Course')
    def __call__(self, request):
        logger.log('Course list')
        try:
            category = site.find_category_by_id(
                int(request['Request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '204 No Content', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create_course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('beginner', name, category)
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['Request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))
                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '204 No Content', 'No categories have been added yet'


@AppRoute(routes=routes, url='/category/')
class Category:
    @Debug(name='Category')
    def __call__(self, request):
        logger.log('Category list')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


@AppRoute(routes=routes, url='/create_category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('category_list.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


@AppRoute(routes=routes, url='/copy_course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['Request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name,
                                    id=new_course.category.id)
        except KeyError:
            return '204 No Content', 'No courses have been added yet'


@AppRoute(routes=routes, url='/students/')
class StudentsListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute(routes=routes, url='/create_student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data):
        name_raw = data['name']
        name = site.decode_value(name_raw)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add_student/')
class AddStudentCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data):
        course_name_raw = data['course_name']
        course_name = site.decode_value(course_name_raw)
        course = site.get_course(course_name)
        student_name_raw = data['student_name']
        student_name = site.decode_value(student_name_raw)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request, *args, **kwargs):
        return '200 OK', BaseSerializer(site.courses).save()
