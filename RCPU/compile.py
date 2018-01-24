from RCPU.compiler import compiler_frontend
import argparse
import logging

from pprint import pformat


def pretty_log_debug(stage, msg, *args, **kwargs):
    logging.debug(stage + '\n' + pformat(msg), *args, **kwargs)


def main():  # pragma: no cover
    parser = argparse.ArgumentParser(description='Compile code.')

    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('compiler', type=str, choices=list(compiler_frontend.keys()))
    parser.add_argument('--debug', action='store_const', const=logging.DEBUG,
                        default=logging.INFO, dest='loglevel')
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format='%(levelname)s: %(message)s')

    compiler = compiler_frontend[args.compiler]
    c = compiler(args.infile)
    print(c.compile())


if __name__ == '__main__':
    main()
