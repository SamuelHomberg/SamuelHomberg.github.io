import sys
import os
import subprocess

def create_pandoc_yaml(filename: str, keywords: str) -> str:
    if filename != 'index':
        pagetitle = filename_to_pagetitle(filename)
    else: 
        pagetitle = 'Samuel’s PhD Blog'
    
    pandoc_yaml = f"\n---\n\
pagetitle: {pagetitle}\n\
header-includes: |\n\
    <link rel='icon' href='../images/favicon.svg' type='image/x-icon'/>\n\
    <meta name='keywords' content='{keywords}'/>\n\
...\n"
    return pandoc_yaml

def filename_to_pagetitle(filename: str) -> str:
    pagetitle = filename.split('_')
    pagetitle = [s.capitalize() if (len(s) > 4) else s for s in pagetitle]
    pagetitle = " ".join(pagetitle)
    return pagetitle

def create_author_date(author_date_xeditdate:str ) -> str:
    lst = author_date_xeditdate.split(',')
    lst = [s.strip() for s in lst]
    if len(lst) == 3:
        has_editdate = True
        author, date, editdate = lst
    elif len(lst) == 2:
        has_editdate = False
        author, date = lst
    else:
        assert 0, f"Unexpected entries in author/date/editdate field:\n{lst}"

    if author == "Samuel Homberg":
        author = "[Samuel Homberg](../index.html)"
    html_str = f"\n<p class='author-date'>\n\
<span class='author'>Author:</span> <span class='name'>{author}</span><br>\n\
<span class='published'>Published:</span> <span class='date'>{date}</span><br>\n"
    if has_editdate:
        html_str = html_str + f"<span class='edited'>Edited:</span> <span class='date'>{editdate}</span><br>"
        html_str = html_str + "</p>"
    else:
        html_str = html_str + "</p>"
    return html_str

def find_md_h1(md: list[str]) -> int:
    for i, l in enumerate(md):
        if l.startswith("# "):
            return i
    assert 0, f"Didn't finde H1 heading."

def find_html_h1(html_lines: list[str]) -> int:
    for i, l in enumerate(html_lines):
        if l.startswith("<h1 "):
            return i
    assert 0, f"Didn't finde H1 heading."


def add_footer(html_lines: list, author: str, position: int=-4) -> list[str]:
    if author == "Homberg":
        footer = f"<footer id='footer'>\n\
    <p class='copyright'>&copy; <a href='../index.html'>Homberg</a> 2023. Design: <a href='https://html5up.net'>HTML5 UP</a>.</p>\n\
</footer>\n"

    else:
        footer = f"<footer id='footer'>\n\
    <p class='copyright'>&copy; {author} 2023. Design: <a href='https://html5up.net'>HTML5 UP</a>.</p>\n\
</footer>\n"
    html_lines.insert(position, footer)
    return html_lines

def insert_html_snippet(html_lines: list, snippet_filename: str, position: int) -> list[str]:
    with open(snippet_filename, 'r') as f:
        snippet_lines = f.readlines()
    for i, l in enumerate(snippet_lines):
        html_lines.insert(position, l)
    return html_lines
    
def add_wrapper_start(html_lines: list[str], position: int) -> list[str]:
    html_lines.insert(position, "<!-- begin wrapper -->\n")
    html_lines.insert(position, "<div id='wrapper'>\n")
    return html_lines

def add_wrapper_end(html_lines: list[str], position: int=-2) -> list[str]:
    html_lines.insert(position, "<!-- end wrapper -->\n")
    html_lines.insert(position, "</div>\n")
    return html_lines

def move_footnotes_up(): # TODO
    return None

def main():
    # take filename as argument
    if len(sys.argv) > 2:
        print(f"Please give only the title of the .md file.\nYou supplied {sys.argv[1:]}")
    elif len(sys.argv) < 2:
        print(f"Please give the title of the .md file.")
        sys.exit()
    else:
        try:
            filename = sys.argv[1].split('.')[0]
            if sys.argv[1].split('.')[1] == 'html':
                print(f"You tried opening a HTML file, please use a markdown file insted!")
                sys.exit()
            with open(sys.argv[1], 'r') as f:
                raw_md = f.readlines()
                keywords = raw_md[0].strip()[4:-4].strip()
                if filename != 'index':
                    author_date_xeditdate = raw_md[1].strip()[4:-4].strip()
        except FileNotFoundError:
            print(f"The file {sys.argv[1]} was not found or does not exist.")
            sys.exit()

    mod_md = raw_md.copy()
    pandoc_yaml = create_pandoc_yaml(filename, keywords)
    mod_md.insert(2, pandoc_yaml)

    if filename != 'index':
        author_date_html = create_author_date(author_date_xeditdate)
        mod_md.insert(find_md_h1(mod_md)+1, author_date_html)

    filename_mod = filename+"_mod.md"
    with open(filename_mod, 'w') as f:
        f.writelines(mod_md)
    
    pandoc_cmd = f"pandoc {filename_mod} -o {filename}.html -s \
--highlight-style=pygments -c css/template.css -M document-css=false \
-M highlighting-css=false"
    subprocess.run(pandoc_cmd.split(" "))

    remove_modified_md = True
    if remove_modified_md:
        os.remove(filename_mod)
    
    filename_html = filename+".html"
    with open(filename_html, 'r') as f:
        html_lines = f.readlines()
    html_lines = add_wrapper_start(html_lines, find_html_h1(html_lines)-1)
    html_lines = add_wrapper_end(html_lines)
    if filename != 'index':
        author = author_date_xeditdate.split(',')[0].split(" ")[-1].strip()
    else:
        author = 'Homberg'
    html_lines = add_footer(html_lines, author)
    # move_footnotes_up(html_lines)
    if filename != 'index':
        html_lines = insert_html_snippet(html_lines, 'html_snippets/back_button_to_blog.html', -2)
    else:
        html_lines = insert_html_snippet(html_lines, 'html_snippets/back_button_to_main.html', -2)

    with open(filename_html, 'w') as f:
        f.writelines(html_lines)

    
if __name__ == '__main__':
    main()
