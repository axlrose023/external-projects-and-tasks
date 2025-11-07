import re
from urllib.parse import urlparse


def is_internal_link(base_url, link):
    link_domain = urlparse(link).netloc
    return urlparse(base_url).netloc == link_domain

def replace_internal_links(base_url, user_site_name, content):
    parsed_base_url = urlparse(base_url)
    modified_content = content.replace(f'href="{base_url}', f'href="/{user_site_name}/')
    modified_content = modified_content.replace(f'src="{base_url}', f'src="/{user_site_name}/')

    def replace_link(match):
        link = match.group(1)
        if is_internal_link(base_url, link):
            return f'href="/{user_site_name}/{link}"'
        else:
            return f'href="{link}"'

    modified_content = re.sub(r'href=["\'](.*?)["\']', replace_link, modified_content)

    return modified_content
