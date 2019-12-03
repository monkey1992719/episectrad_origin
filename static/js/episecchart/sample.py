import tinycss

cssfile = open("episecchart.css", "r")
css = cssfile.read()

stylesheet = tinycss.make_parser().parse_stylesheet(css)

for rule in stylesheet.rules:
    if rule.selector.as_css() == '.voi_pos':
        print(rule.

