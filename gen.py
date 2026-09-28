
import re, os
import hashlib
import shutil


def hash_file(path):
	with open(path, "rb") as f:
		return hashlib.file_digest(f, "md5").hexdigest()[:6]


css_url = f"style-{hash_file("static/style.css")}.css"

head_template = f"""
	<head>
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">

		<meta charset="UTF-8">
		<link rel="stylesheet" href="{css_url}">
	</head>
"""


htmls = []
for file in os.listdir():
	if file.endswith(".html"):
		htmls.append(file)

def create_link(link, name):
	return f'<a href="{link}">{name}</a>'


def links_template_for_file(name):
	out = ""
	if name in filename_to_human.keys():
		out += f'<p style="font-size: 150%;">{filename_to_human[name]}</p><span style="margin-left: 8px; width: 12px; display: inline-block;">|</span>\n'
	else:
		out += f'<p style="font-size: 150%;">{name[:-1]}</p><span style="margin-left: 8px; width: 12px; display: inline-block;">|</span>\n'
	for file in htmls:
		if file != name and file in filename_to_human.keys():
			out += create_link(file, filename_to_human[file]) + '<span style="margin-left: 8px; width: 8px; display: inline-block;">|</span>' + "\n"
	return out


filename_to_human = {}
for file in htmls:
	name = ""
	with open(file) as f:
		name = f.readline()
	if name != "!hidden":
		filename_to_human[file] = name


for file in htmls:
	out = ""
	with open(file) as f:
		i = 0
		for line in f.readlines():
			if line.strip() == "HEAD":
				line = re.sub(r"\s*(HEAD)\s*", head_template, line)
			if line.strip() == "LINKS":
				line = re.sub(r"\s*(LINKS)\s*", links_template_for_file(f.name), line)
			if i != 0:
				out += line
			i += 1
	with open("generated/" + file, "w") as f:
		f.writelines(out)

for file in os.listdir("static/"):
	if file == "style.css":
		shutil.copy("static/"+file, "generated/"+css_url)
	else:
		shutil.copy("static/"+file, "generated/"+file)
