"""python -m synesis [--teks] [--sungguhan]"""

import sys

from . import cli, jendela


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    (cli if "--teks" in argv else jendela).main(argv)


if __name__ == "__main__":
    main()
