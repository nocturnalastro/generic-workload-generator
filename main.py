import yaml # might be better to use ruamel in the future
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action="store_true", default=False)
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

__DEBUG = args.debug

env = Environment(loader=FileSystemLoader(args.templates), keep_trailing_newline=False)
def from_yaml(input, indent=2):
    return yaml.load(input, Loader=yaml.SafeLoader)
env.filters["from_yaml"] = from_yaml

def to_yaml(input, indent=2):
    return yaml.dump(input, indent=indent, Dumper=yaml.SafeDumper)
env.filters["to_yaml"] = to_yaml


if __DEBUG:
    print(" Templates ".center(30, "*"))
    print(env.list_templates())
    print("*"*30)



results = []
with args.input.open() as f:
    for manifest in yaml.load_all(f.read(), yaml.SafeLoader):
        for m in manifest:
            copies = m.get("copies")
            for i in range(0, copies or 1):
                res = env.get_template(f"{m['template']}.yaml.j2").render(index=i, **m)

                if __DEBUG:
                    print(" Raw result ".center(30, "#"))
                    print(res)
                    print("#"*30)

                results.append(
                    to_yaml(from_yaml(res), 2)
                )

output_list = []
for r in results:
    r = r.strip()
    if not r.startswith("---"):
        output_list.append("---")
    output_list.append(r)
output = "\n".join(output_list)

if args.output:
    with args.output.open("w") as f:
        f.write(output)
else:
    print(output)
