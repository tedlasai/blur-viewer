# build.py
def inline(file):
    with open(file, 'r') as f:
        return f.read()

with open("index.html", "w") as out:
    out.write(inline("components/header.html"))
    out.write(inline("components/js_links.html"))
    out.write(inline("components/title_block.html"))
    out.write(inline("components/inthewild.html"))
    out.write(inline("components/historical.html"))
    out.write(inline("components/simulated.html"))
    out.write(inline("components/baseline.html"))
    out.write(inline("components/ending.html"))