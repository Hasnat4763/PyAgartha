from string import Template
import os
import regex

regex_pattern = r'\{\s*([\w\-/]+\.html)\s*\}'

dir_name = ""
template_dir = os.path.join(os.path.dirname(__file__), "templates")
def template_path(name):
    global dir_name
    global template_dir
    dir_name = name
    template_dir = os.path.join(os.path.dirname(__file__), str(dir_name))

def render_template(template_name, **context):
    path = os.path.join(template_dir, template_name)
    with open(path, "r", encoding = "utf-8") as f:
        content = f.read()
    content = evaluate_include(content, lambda match: render_template(match.group(1), **context))
    content = evaluate_loops(content, context)
    content = evaluate_if_statement(content, context)
    content = evaluate_variables(content, context)
    return content

def evaluate_include(content, replace):
    return regex.sub(regex_pattern, replace, content)


def evaluate_loops(content, context):
    loop_pattern = r'%\s*for\s+(\w+)\s+in\s+(\w+)\s*:\s*(.*?)%\s*end'

    def replace(match):
        variable, iterable_name, block = match.groups()
        output = ""
        iterable = context.get(iterable_name, [])
        for item in iterable:
            loop_context = {**context, variable: item}
            processed_block = evaluate_loops(block, loop_context)
            processed_block = evaluate_if_statement(processed_block, loop_context)
            processed_block = evaluate_variables(processed_block, loop_context)
            output += processed_block
        return output
    while regex.search(loop_pattern, content, regex.DOTALL):
        content = regex.sub(loop_pattern, replace, content, flags=regex.DOTALL)

    return content

def evaluate_variables(content, context):
    var_pattern = r'\$(\w+)(?:\.(\w+)|\[([\'"]?)(\w+)\3\])?'
    
    def replace(match):
        variable_name = match.group(1)
        property_name = match.group(2)
        bracket_key = match.group(4)
        
        value = context.get(variable_name, "")
        
        if property_name:
            if isinstance(value, dict):
                return str(value.get(property_name, ""))
            elif hasattr(value, property_name):
                return str(getattr(value, property_name, ""))
            return ""
        
        if bracket_key:
            if isinstance(value, dict):
                return str(value.get(bracket_key, ""))
            elif isinstance(value, (list, tuple)):
                try:
                    return str(value[int(bracket_key)])
                except (ValueError, IndexError):
                    return ""
            return ""
        
        return str(value)
    return regex.sub(var_pattern, replace, content)
    
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
