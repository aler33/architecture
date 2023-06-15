from jinja2 import Template
from os.path import join


def render(templ_name, folder='templates', **kwargs):
    file_path = join(folder, templ_name)
    with open(file_path, encoding='utf-8') as f:
        templ = Template(f.read())
    return templ.render(**kwargs)
