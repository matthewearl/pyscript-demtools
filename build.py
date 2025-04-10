from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

pages = [
    ("index.html", "index.html", "demtools"),
    ("superimpose.html", "superimpose.html", "demsuperimpose"),
]

for template_name, output_path, page_title in pages:
    template = env.get_template(template_name)
    html = template.render(title=page_title)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
