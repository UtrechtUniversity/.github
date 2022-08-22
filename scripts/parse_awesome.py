import datetime
import random
import re
from pathlib import Path

import requests
from jinja2 import Template

NUMBER_OF_CARDS = 3
CARD_WIDTH = 260
README_URL = "https://raw.githubusercontent.com/UtrechtUniversity/awesome-utrecht-university/main/README.md"


def get_repo_features(project):
    git_org = re.search(r"git.*?/(.*?)([) ]|[/])", project).group(1)
    repo_name = re.search(r"git.*?/.*?/(.*?)\) ", project)
    if repo_name is not None:
        repo = repo_name.group(1)
    else:
        repo = git_org
    link = re.search(r"([A-Za-z0-9]+://.*?)\)", project).group(1)
    return git_org, repo, link


def create_svg(idx, repo, owner):

    with open(Path("scripts", "featured_template.svg")) as f:
        template = Template(f.read())

    text_size = 74
    if len(repo) > 14:
        text_size = 50
    if len(repo) > 24:
        text_size = 32
    if len(repo) > 36:
        text_size = 24

    if len(repo) > 50:
        repo = repo[0:48] + "..."

    with open(Path("img", f"featured_{idx}.svg"), "w") as f:
        f.write(template.render(idx=idx, repo=repo, owner=owner, text_size=text_size))


def create_html(url_list, width=CARD_WIDTH):

    html_images = []
    for i, url in enumerate(url_list):
        html_images.append(
            f'<a href="{url}"><img align="center" src="/img/featured_{i+1}.svg" width="{width}" ></a>'
        )

    return '<p align="center">' + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(html_images) + "</p>"


def update_readme(html_block):
    with open(Path("profile", "README.md")) as f_read:
        readme = f_read.read()
        readme_top = readme.split("<!-- START FEATURED -->")[0]
        readme_bottom = readme.split("<!-- END FEATURED -->")[1]
        readme_new = (
            readme_top
            + "<!-- START FEATURED -->\n\n"
            + html_block
            + "\n\n<!-- END FEATURED -->"
            + readme_bottom
        )
    with open(Path("profile", "README.md"), "w") as f_write:
        f_write.write(readme_new)


def main():

    awesome = requests.get(README_URL)
    projects_section = re.search(
        r"<!-- START PROJECTS -->.*<!-- END PROJECTS -->", awesome.text, re.DOTALL
    )
    projects = re.findall(r"^- .*", projects_section.group(), flags=re.MULTILINE)

    random.seed((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).days)
    selection = random.sample(projects, k=NUMBER_OF_CARDS)

    url_list = []

    for idx, item in enumerate(selection):

        git_org, repo, link = get_repo_features(item)
        url_list.append(str(link))

        create_svg(idx + 1, repo, git_org)

    html_block = create_html(url_list, width=CARD_WIDTH)

    update_readme(html_block)


if __name__ == "__main__":
    main()
