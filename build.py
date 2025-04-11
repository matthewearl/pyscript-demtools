from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

pages = [
    ("index.html", "index.html", None, None),
    ("superimpose.html", "superimpose.html", "superimpose",
     "add players from other demos into a base demo"),
    ("showros.html", "showros.html", "showros",
     "unhide players with Ring of Shadows"),
    ("demtext.html", "demtext.html", "demtext",
     "generate a text file for a demo"),
]

tools = [
    {"output_path": output_path, "title": title, "desc": desc}
    for _, output_path, title, desc in pages
    if desc
]

for template_name, output_path, title, desc in pages:
    template = env.get_template(template_name)
    if template_name == "index.html":
        html = template.render(tools=tools)
    else:
        html = template.render(title=title, desc=desc)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
