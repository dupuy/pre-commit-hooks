from __future__ import print_function

import argparse
import fileinput
import sys
import os

from pre_commit_hooks.util import cmd_output


def _fix_file(filename, markdown=False):
    for line in fileinput.input([filename], inplace=True):
        # preserve trailing two-space for non-blank lines in markdown files
        if markdown and (not line.isspace()) and (line.endswith("  \n")):
            line = line.rstrip(' \n')
            # only preserve if there are no trailing tabs or unusual whitespace
            if not line[-1].isspace():
                print(line + "  ")
                continue

        print(line.rstrip())


def fix_trailing_whitespace(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-markdown-linebreak-ext', action='store_const',
                        const=[], default=argparse.SUPPRESS,
                        dest='markdown_linebreak_ext',
                        help='Do not preserve linebreak spaces in Markdown')
    parser.add_argument('--markdown-linebreak-ext', action='append', const='*',
                        default=argparse.SUPPRESS, metavar='EXTS', nargs='?',
                        help='Markdown extensions (or *) for linebreak spaces')
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    bad_whitespace_files = cmd_output(
        'grep', '-l', '[[:space:]]$', *args.filenames, retcode=None
    ).strip().splitlines()

    # combine all extension arguments, splitting at ',' and normalizing them
    # (lowercase and remove unnecessary leading '.' which may be present)
    md_args = vars(args).get('markdown_linebreak_ext', ['md', 'markdown'])
    md_exts = [x.lower().lstrip('.') for x in ','.join(md_args).split(',')]
    all_markdown = '*' in md_exts

    if bad_whitespace_files:
        for bad_whitespace_file in bad_whitespace_files:
            # get extension ([1]); remove leading '.' ([1:]); and make lowercase
            extension = os.path.splitext(bad_whitespace_file)[1][1:].lower()

            print('Fixing {0}'.format(bad_whitespace_file))
            _fix_file(bad_whitespace_file, all_markdown or extension in md_exts)
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(fix_trailing_whitespace())
