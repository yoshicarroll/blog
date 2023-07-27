import os
from pprint import pprint
import re
import shutil
import unicodedata

from jinja2 import Environment, FileSystemLoader
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension
import yaml

def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

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

        # A custom build_url function that slugifies the label
    def build_url(label, base, end):
        slugified_label = slugify(label)
        return f'{base}{slugified_label}{end}'
    
    body_html = markdown.markdown(body_md, extensions=['fenced_code', WikiLinkExtension(build_url=build_url)])
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

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the output to the output file
    with open(output_path, 'w') as f:
        f.write(output)


def generate_site():
    """
    This function generates the entire site by converting each Markdown file to HTML
    and creating an index.html file that lists all the posts.
    """

    # Delete the output directory if it exists
    if os.path.exists('output'):
        shutil.rmtree('output')

    # Recreate the output directory
    os.makedirs('output', exist_ok=True)

    # Copy the static_src directory to output/static
    shutil.copytree('static_src', 'output/static')


    # Get a list of all the Markdown files
    md_files = os.listdir('content')

    # This list will hold the metadata for all posts
    posts = []

    # Convert each Markdown file to HTML
    for md_file in md_files:
        # Parse the Markdown file
        front_matter, body_md = parse_md_file(f'content/{md_file}')

        # Find all the wiki-style links in the Markdown text
        links = re.findall(r'\[\[([^\]]+)\]\]', body_md)

        # The URL of the post is the filename with .md replaced by .html
        url = md_file.replace('.md', '.html')

        # Create the post metadata
        post = {
            'title': front_matter['title'],
            'url': url,
            'date': front_matter['date'],
            'links': links,
            'body_md': body_md,
            'slug': slugify(front_matter['title']),
        }
  
        # Add the post's metadata to the list of posts
        posts.append(post)

    for post in posts:
        post['backlinks'] = [other_post for other_post in posts if post['title'] in other_post['links']]


     # Convert each Markdown file to HTML
    for post in posts:
        body_html = convert_md_to_html(post['body_md'])

        # Write the HTML to a new file
        render_template('post_template.html', f'output/{post["slug"]}/index.html', {
            'title': post['title'],
            'content': body_html,
            'backlinks': post['backlinks'],  # Pass the backlinks to the template
        })


    # Sort posts by date & time
    posts.sort(key=lambda post: post['date'], reverse=True)


    # Render the homepage template with the list of posts
    render_template('index_template.html', 'output/index.html', {'posts': posts})



generate_site()
