from .args import parser
from .run import run

if __name__ == "__main__":
    args = parser.parse_args()
    run(args)
