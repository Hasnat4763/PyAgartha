from string import Template
import os
import regex

regex_pattern = r'\{\s*([\w\-/]+\.html)\s*\}'

template_dir = os.path.join(os.path.dirname(__file__), "templates")

def render_template(template_name, **context):
    path = os.path.join(template_dir, template_name)
    with open(path, "r", encoding = "utf-8") as f:
        content = f.read()

    template = Template(content)
    
    content = evaluate_include(content, lambda match: render_template(match.group(1), **context))
    
    return template.safe_substitute(**context)

def evaluate_include(content, replace):
    return regex.sub(regex_pattern, replace, content)