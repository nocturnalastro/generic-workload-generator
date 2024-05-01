import yaml  # might be better to use ruamel in the future
from jinja2 import Environment, FileSystemLoader, ChoiceLoader
import ast
import os

from .filters import *
from .args import parser, DEFAULT_TEMPLATES

__DEBUG = None


def print_if_debug(title, content, symbol, length=30):
    if __DEBUG:
        print(f" {title} ".center(length, symbol))
        print(content)
        print(symbol * length)


def get_extra_vars(args):
    extra_vars = {}
    for ev in args.extra_vars:
        k, raw_v = ev.split("=")
        try:
            v = raw_v = ast.literal_eval(raw_v)
        except ValueError:
            print(f"Unable to parse extra var: '{ev}'")
            os.exit(1)
        extra_vars[k] = v
    return extra_vars


def get_jinja_env(args):
    loader = ChoiceLoader([FileSystemLoader(p) for p in reversed(args.templates)])
    env = Environment(loader=loader, keep_trailing_newline=False)
    bind_filters(env)
    print_if_debug("Templates", env.list_templates(), "*")
    return env


def process_volumes(env, volume_defs):
    volumes = []
    for v in volume_defs:
        copies = v.get("copies")
        for i in range(0, copies or 1):
            vol_res = env.get_template(f"volumes/{v['template']}.yaml.j2").render(
                index=i, **v
            )
            volumes.append(vol_res)

    res = ""
    if len(volumes) > 0:
        res = from_yaml("\n".join(volumes))
        print_if_debug("Volumes", to_yaml(res), "v")
    return res


def join_manifests(manifests):
    output_list = []
    for r in manifests:
        r = r.strip()
        if not r.startswith("---"):
            output_list.append("---")
        output_list.append(r)

    return "\n".join(output_list)


def write(args, results):
    output = join_manifests(results)
    if args.output:
        with args.output.open("w") as f:
            f.write(output)
    else:
        print(output)


def process_manifest_def(m, env):
    result = []
    volumes = m.get("volumes", [])
    if len(volumes) > 0:
        m["volumes"] = process_volumes(env, volumes)

    copies = m.get("copies")
    for i in range(0, copies or 1):
        res = env.get_template(f"{m['template']}.yaml.j2").render(
            index=i, **m
        )
        res = remove_blank_lines(res)
        print_if_debug("Raw result", res, "#")
        result.append(to_yaml(from_yaml(res), 2))
    return result

def run(args):
    env = get_jinja_env(args)
    extra_vars = get_extra_vars(args)
    results = []
    with args.input.open() as f:
        manifests = yaml.load(f.read(), yaml.SafeLoader)

    for m in manifests:
        m.update(extra_vars)
        results.extend(process_manifest_def(m, env))

    write(args, results)


if __name__ == "__main__":
    args = parser.parse_args()
    __DEBUG = args.debug
    run(args)
