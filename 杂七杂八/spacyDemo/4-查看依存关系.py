from pathlib import Path

import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_trf")

sentence = "However, learning to understand and to share the value system of a society cannot be achieved only in home."
doc = nlp(sentence)

for token in doc:
    print(token.text, token.dep_, token.pos_, token.tag_)

# 生成树状结构
# svg = displacy.render(doc, style="dep", jupyter=False)
# out_path = Path("./dependency_plot.svg")
# out_path.open("w", encoding="utf-8").write(svg)

displacy.serve(doc, style='dep', host="127.0.0.1", port=5000)
