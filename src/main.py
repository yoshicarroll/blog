import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
import markdown
import yaml



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


def generate_site():
    """
    This function generates the entire site by converting each Markdown file to HTML
    and creating an index.html file that lists all the posts.
    """
    # Get a list of all the Markdown files
    md_files = os.listdir('content')

    # This list will hold the metadata for all posts
    posts = []

    # Convert each Markdown file to HTML
    for md_file in md_files:
        # Parse the Markdown file
        front_matter, body_md = parse_md_file(f'content/{md_file}')

        # Convert the body to HTML
        body_html = convert_md_to_html(body_md)

        # The URL of the post is the filename with .md replaced by .html
        url = md_file.replace('.md', '.html')

        # Add the post's metadata to the list of posts
        posts.append({
            'title': front_matter['title'],
            'url': url,
            'date': front_matter['date'],

        })

        # Sort posts by date & time
        posts.sort(key=lambda post: post['date'], reverse=True)

        # Write the HTML to a new file
        render_template('post_template.html', f'output/{url}', {
            'title': front_matter['title'],
            'content': body_html,
        })

    # Render the homepage template with the list of posts
    render_template('index_template.html', 'output/index.html', {'posts': posts})



generate_site()
