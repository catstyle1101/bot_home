from jinja2 import Template


def render_message(template_name: str, **kwargs) -> str:
    with open(template_name, 'r') as f:
        template = Template(f.read())

    message = template.render(**kwargs)
    return message
