import yaml
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from io import StringIO

__DEBUG = True

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=Path)
parser.add_argument("-o", "--output", type=Path)
parser.add_argument(
    "-t",
    "--templates",
    type=Path,
    help="directory where the templates live",
    action="append",
    default=Path(__file__).parent / "templates",
)
args = parser.parse_args()

env = Environment(loader=FileSystemLoader(args.templates))

if __DEBUG:
    print(env.list_templates())


results = []
with args.input.open() as f:
    for manifest in yaml.load_all(f.read(), yaml.SafeLoader):
        for m in manifest:
            copies = m.get("copies")
            for i in range(0, copies or 1):
                results.append(
                    env.get_template(f"{m['template']}.yaml.j2").render(index=i, **m)
                )

output = ""
for r in results:
    r = r.strip()
    if not r.startswith("---"):
        output += "\n---\n"
    output += r + "\n"

if args.output:
    with args.output.open("w") as f:
        f.write(output)
else:
    print(output)
