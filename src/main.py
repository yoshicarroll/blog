import yaml
import markdown
import os
from jinja2 import Environment, FileSystemLoader


def parse_md_file(file_path):
    """
    This function takes a path to a markdown file, extracts the front matter and 
    the body, and returns them as a tuple.
    """
    with open(file_path, 'r') as f:
        contents = f.read().split('---')

    # If the contents list has more than one element, that means there is front matter
    if len(contents) > 1:
        front_matter = yaml.safe_load(contents[1])
        body_md = '---'.join(contents[2:]).strip()
    else:
        front_matter = {}
        body_md = contents[0].strip()

    return front_matter, body_md


def convert_md_to_html(body_md):
    """
    This function takes the body of a markdown file and converts it to HTML.
    """
    body_html = markdown.markdown(body_md)
    return body_html

def render_template(template_path, output_path, variables):
    """
    This function takes a template file and a dictionary of variables, 
    renders the template with those variables, and writes the output to a file.
    """
    # Set up the jinja2 environment
    env = Environment(loader=FileSystemLoader('src/templates'))

    # Load the template file
    template = env.get_template(template_path)

    # Render the template with the given variables
    output = template.render(variables)

    # Write the output to the output file
    with open(output_path, 'w') as f:
        f.write(output)


# Let's test these functions with our first_post.md
file_path = 'content/first_post.md'
front_matter, body_md = parse_md_file(file_path)
body_html = convert_md_to_html(body_md)

print(front_matter)
print(body_html)

# The path to our template file
template_path = 'post_template.html'

# The path to the output HTML file
output_path = 'output/first_post.html'

# The variables to insert into the template
variables = {
    'title': front_matter['title'],
    'content': body_html,
}

# Render the template and write the output
render_template(template_path, output_path, variables)
