import argparse
from pathlib import Path


DEFAULT_TEMPLATES = [Path(__file__).parent.parent / "templates"]

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
    default=DEFAULT_TEMPLATES,
)
parser.add_argument(
    "-e",
    "--extra-vars",
    action="append",
    default=[],
)
