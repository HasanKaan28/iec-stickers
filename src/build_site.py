import json, pathlib, sys
here = pathlib.Path(__file__).parent
out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
data = json.loads((here / "stickers.json").read_text(encoding="utf-8"))
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", r"<\/")
html = (here / "site_template.html").read_text(encoding="utf-8").replace("__STICKERS__", blob)
(out / "index.html").write_text(html, encoding="utf-8")
(out / ".nojekyll").write_text("", encoding="utf-8")
print(len(html), "bytes ->", out / "index.html")
