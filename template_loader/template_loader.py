from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('static', 'templates'),
    autoescape=select_autoescape(['html'])
)

def template(html_file):
    return env.get_template(html_file)