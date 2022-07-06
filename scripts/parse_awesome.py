import requests
import re
import random
awesome = requests.get('https://raw.githubusercontent.com/UtrechtUniversity/awesome-utrecht-university/main/README.md')
projects_section = re.search(r'<!-- START PROJECTS -->.*<!-- END PROJECTS -->', awesome.text, re.DOTALL)
projects = re.findall(r'^- .*', projects_section.group(), flags=re.MULTILINE)
selection = random.sample(projects, k=3)
print(selection)

url_list = []
for idx, item in enumerate(selection):

    git_org = re.search(r'git.*?/(.*?)/', item).group(1)
    repo = re.search(r'git.*?/.*?/(.*?)\) ', item).group(1)
    link = re.search(r'([A-Za-z0-9]+://.*?)\)', item).group(1)
    print(link)
    url_list.append(str(link))
    print(url_list)
    with open('../img/featured_'+str(idx+1)+'.svg', 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>'
                '<svg id="a" xmlns="http://www.w3.org/2000/svg" viewBox="200 0 792.09 300">' #508.83">'
                '<defs>'
                '<style>.c{letter-spacing:-.01em;}.'
                'd{letter-spacing:0em;}.'
                'e{letter-spacing:0em;}.'
                'f{letter-spacing:0em;}.'
                'g{letter-spacing:0em;}.'
                'h{letter-spacing:-.03em;}.'
                'i{letter-spacing:0em;}.'
                'j{fill:#ffcd00;stroke:#fff;stroke-miterlimit:10;}.'
                'k{fill:#fff;opacity:.21;}.'
                'l{letter-spacing:0em;}.'
                'm{font-size:87.42px;}.'
                'm,.'
                'n,.'
                'o{font-family:Arial;}.'
                'n{font-size:25.25px;}.'
                'o{font-size:16.2px;}'
                '</style>'
                '</defs>'
                '<rect id="b" class="j" x="265.09" y="12.82" width="526.5" height="274.36" rx="19.24" ry="19.24"/>'
                '<ellipse class="k" cx="352.33" cy="254.42" rx="352.33" ry="254.42"/>'
                '<text class="o" transform="translate(695.6 46.14)">'
                '<tspan class="h" x="0" y="0">Featured ' + str(idx+1) + '</tspan>'
                '</text>'
                '<text class="m" transform="translate(291.76 177.51)">'
                '<tspan x="0" y="0">'+
                repo +
                '</tspan>'
                '</text>'
                '<text class="n" transform="translate(291.76 221.47)">'
                '<tspan class="e" x="0" y="0">By ' +
                git_org +
                '</tspan>'
                '</text>'
                '</svg>')


html_images = '<p float="left">' + \
  '<a href="'+url_list[0]+'"> <img src="/img/featured_1.svg" width="250" ></a>' + \
  '<a href="'+url_list[1]+'"> <img src="/img/featured_2.svg" width="250" ></a>' + \
  '<a href="'+url_list[2]+'"> <img src="/img/featured_3.svg" width="250" ></a>' + \
  '</p>'

with open("../profile/README.md") as f_read:
        readme = f_read.read()
        readme_top = readme.split("<!-- START FEATURED -->")[0]
        readme_bottom = readme.split("<!-- END FEATURED -->")[1]
        readme_new = readme_top + "<!-- START FEATURED -->\n\n" +  \
                        html_images +\
                    "\n\n<!-- END FEATURED -->" + readme_bottom
        with open("../profile/README.md", "w") as f_write:
                f_write.write(readme_new)
