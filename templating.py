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
    
    content = evaluate_loops(content, context)
    content = evaluate_if_statement(content, context)
    return Template(content).safe_substitute(**context)

def evaluate_include(content, replace):
    return regex.sub(regex_pattern, replace, content)


def evaluate_loops(content, context):
    loop_pattern = r'%\s*for\s+(\w+)\s+in\s+(\w+)\s*:\s*(.*?)%\s*end'

    def replace(match):
        variable, iterable_name, block = match.groups()
        output = ""
        for item in context.get(iterable_name, []):
            loop_context = {**context, variable: item}
            output += Template(block).safe_substitute(loop_context)
        return output
    while regex.search(loop_pattern, content, regex.DOTALL):
        content = regex.sub(loop_pattern, replace, content, flags=regex.DOTALL)

    return content

def evaluate_if_statement(content, context):
    if_pattern = r'%\s*if\s+(\w+)\s*:\s*(.*?)(?:%\s*else\s*:\s*(.*?))?%\s*end'
    def replace(match):
        variable, if_block, else_block = match.groups()
        condition = context.get(variable)

        if condition:
            return Template(if_block).safe_substitute(context)
        else:
            return Template(else_block or "").safe_substitute(context)
    while regex.search(if_pattern, content, regex.DOTALL):
        content = regex.sub(if_pattern, replace, content, flags=regex.DOTALL)

    return content
