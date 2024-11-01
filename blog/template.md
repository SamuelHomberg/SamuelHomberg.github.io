<!-- cheminformatics, computational drug design, machine learning, programming, blog, blog posts, samuel homberg, academia, research, Münster --> 
<!-- Samuel Homberg, 21.JUL.2023 -->

# Blogpost template

This is a markdown template that may be converted to html using pandoc. This was also used to alter the .css files to alter the design for the actual blog entries. The template is kept as pure markdown (except for two comments at the top with keywords and the date / authro) which is preprocessed using a python script. 

Different markdown elements are shown in the next sections.

## Basic Markdown Syntax

- **Bold**
- *Italic*
- ***Both***
- `Inline code`

> Blockquote: Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.

### Lists

1. Ordered List
    1. abc
    2. cba
    3. bac
2. Unordered List
    - xyz
    - zab
    - bac

### Code

```py
# techincally this fenced code is also extended syntax
def some_func(arg1: int, arg2: int) -> str:
    var = arg1 + arg2
    return str(var)

some_func(1, 3)
>>> '4'
```

### Links & Images

Text with an [important link](https://www.youtube.com/watch?v=dQw4w9WgXcQ) embedded. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.

Also, here is a picture:

![Alttext / image description](./images/template.gif)

Some more text.  At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

## Extended Syntax

### Table

| Syntax | Description |
| ----------- | ----------- |
| Header | Title |
| Paragraph | Text |

### Tasklist, Superscript, Subscript, Emoji, Footnote

- [ ] Unticked box~5~
- [x] Ticked box^7^
- [x] Text with Footnote. [^1]


### Strikethrough, Highrule

 At vero eos et accusam et justo duo dolores et ea rebum. Stet clita, no sea takimata sanctus est ~~Lorem ipsum~~ dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.

---

## These markdown features don't work

- Emojis: :joy:
- highlight: ===highlight===

[^1]: This is the footnote.
