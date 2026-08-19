import mistletoe



with open('README.md', 'r') as fin:
    rendered = mistletoe.markdown(fin)
    print(rendered)
    print(type(rendered))