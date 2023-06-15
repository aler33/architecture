from datetime import datetime
from views import Index, Page, Contact


def add_date(request):
    request['date'] = datetime.now()


fronts = [add_date]


routes = {
    '/': Index(),
    '/page/': Page(),
    '/contact/': Contact(),
    '/index/': Index(),
}
