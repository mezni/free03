
import json 

base_dir = "translations"
en_file = base_dir / "en.json"
fr_file = base_dir / "fr.json"

def read_file(ref_file):
    with open(ref, "r", encoding="utf-8") as f:
        ref = json.load(f)
    return ref    

english = read_file(en_file)
french = read_file(fr_file)

missing_keys = sorted(set(english.keys()) - set(french.keys()))

for key in missing_keys:
    french[key] = english[key]


with open(fr_file, "w", encoding="utf-8") as f:
    json.dump(french, f, ensure_ascii=False, indent=2)
    f.write("\n")    

from deep_translator import GoogleTranslator

translator = GoogleTranslator(source="en", target="fr")

for key in missing:
    french[key] = translator.translate(reference[key])