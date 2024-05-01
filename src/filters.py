from copy import deepcopy
import jinja2
import yaml

def combine(input, other):
    x = deepcopy(input)
    x.update(other)
    return x

def filter_list(input, key, *values):
    return list(filter(lambda x: x[key] in values, input))


def from_yaml(input, indent=2):
    return yaml.load(input, Loader=yaml.SafeLoader)


def to_yaml(input, indent=2):
    return yaml.dump(input, indent=indent, Dumper=yaml.SafeDumper)


def remove_blank_lines(input):
    return "".join([s for s in input.splitlines(True) if s.strip(" \t\r\n")])

@jinja2.pass_context
def eval_as_template(context, input, **vars):
    if input == jinja2.Undefined:
        return input
    return jinja2.Template(input).render(context, **vars)



def bind_filters(env):
    env.filters.update(
        {
            "combine": combine,
            "filter_list": filter_list,
            "from_yaml": from_yaml,
            "to_yaml": to_yaml,
            "remove_blank_lines": remove_blank_lines,
            "eval_as_template": eval_as_template,
        }
    )
