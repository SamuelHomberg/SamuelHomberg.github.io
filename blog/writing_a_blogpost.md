<!-- cheminformatics, computationsl drug design, machine learning, programming, blog, blog posts, samuel homberg, academia, research, Münster, pandoc -->
<!-- Samuel Homberg, 21.JUL.2023 -->

# Writing a blogpost (like this) in pure markdown

## Motivation

I wanted to write a blog for when I find useful or interesting things, mainly when programming.
Not only will I have an easy way of looking them up, they might also be useful to someone that stumbles upon this blog.
[This blogpost](https://www.blopig.com/blog/2023/02/creating-a-personal-website/) here was a great help, and the the [OPIG Blog](https://www.blopig.com/blog/) inspired me to get started with blogging.

## pandoc

To reduce the barrier of entry for writing a post, I wanted to be able to write in pure markdown. While there are multple ways to convert markdown to html, `pandoc` seems to be the most powerful and versatile. It might also be interesting to use `pandoc` to convert a draft of some sort to pdf via LaTeX, which `pandoc` is also capable of.
The installation for windows is apparently not straightforward (I want to write on my surface), but installing pandoc on WSL is very easy.

## parsing (almost) pure markdown

While it is possible to add header-info (like a favicon, keywords and the pagetitle) within markodown in a yaml-block, I chose to write a short python program, that will take the necessary keywords from a comment at the top and thus keep the markdown-file itself as pure as possible.

## building the rest of the website

Using a template from [HTML5 UP!](https://html5up.net/), I created a personal website (following the steps outlined in the [blog post](https://www.blopig.com/blog/2023/02/creating-a-personal-website/) mentioned above).
With the `template.md` file I adjusted the CSS from the template (adding code-highlighting, ...). I then added a link to the blog via a page `blog/index.html`, where I will (have to manually) add the blog entries, as I write them. The complete workflow for creating a blogpost is as follows:

## Steps to write a blogpost this way

1. Copy the `template.md` file.
2. Rename it with a shorttitle. (This will be displayed in the browser.)
3. Write the blogpost, add keywords and the correct date.
4. Switching to WSL, run `python _md_to_html.py <blogpost>.md` from the `blog` folder.
5. Edit the `blog/index.md` and run `python _md_to_html.py index.md`
6. Add/commit/push the new/changed files (from Windows, WSL sees a lot of files as changed).
