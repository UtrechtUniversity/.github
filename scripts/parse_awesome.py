import datetime
import random
import re
from pathlib import Path

import requests
from jinja2 import Template

NUMBER_OF_CARDS = 2
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


def create_card(owner, repo):
    card = (
        "[![Featured Project](https://github-readme-stats.vercel.app/api/pin/?"
        + "username=" + owner
        + "&repo=" + repo
        + "&show_owner=true&bg_color=FFCD00&title_color=000000)]"
        + "(https://github.com/" + owner + "/" + repo + ")"
    )
    return card


def update_readme(featured_projects):
    with open(Path("profile", "README.md")) as f_read:
        readme = f_read.read()
        readme_top = readme.split("<!-- START FEATURED -->")[0]
        readme_bottom = readme.split("<!-- END FEATURED -->")[1]
        readme_new = (
            readme_top
            + "<!-- START FEATURED -->\n\n"
            + featured_projects[0] + "\n"
            + featured_projects[1] + "\n"
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

    featured_projects = []

    for idx, item in enumerate(selection):

        git_org, repo, link = get_repo_features(item)
        
        featured_projects.append(create_card(git_org, repo))

    update_readme(featured_projects)


if __name__ == "__main__":
    main()
