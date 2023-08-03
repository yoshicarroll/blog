import datetime
import os

# Post content template
content_template = """---
title: {title}
date: {date}
---

This is a test post.
"""

# Create a directory for the content if it doesn't exist
os.makedirs("content", exist_ok=True)

for i in range(26):
    post_date = datetime.datetime(2020, 1, 1) + datetime.timedelta(days=i*11)

    # Create a title for the post
    post_title = f"Test Post {i+1}"

    # Generate the content for the post
    post_content = content_template.format(title=post_title, date=post_date.strftime('%Y-%m-%d %H:%M:%S'))

    # Write the post content to a Markdown file
    with open(f"content/test_post_{i+1}.md", "w") as file:
        file.write(post_content)
