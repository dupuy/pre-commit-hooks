from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.trailing_whitespace_fixer import fix_trailing_whitespace
from testing.util import cwd


def test_fixes_trailing_whitespace(tmpdir):
    with cwd(tmpdir.strpath):
        for filename, contents in (
                ('foo.py', 'foo \nbar \n'),
                ('bar.py', 'bar\t\nbaz\t\n'),
        ):
            with open(filename, 'w') as file_obj:
                file_obj.write(contents)  # pragma: no branch (26 coverage bug)

        ret = fix_trailing_whitespace(['foo.py', 'bar.py'])
        assert ret == 1

        for filename, after_contents in (
                ('foo.py', 'foo\nbar\n'),
                ('bar.py', 'bar\nbaz\n'),
        ):
            assert open(filename).read() == after_contents


def test_fixes_trailing_markdown_whitespace(tmpdir):
    with cwd(tmpdir.strpath):
        for filename, contents in (
                ('foo.md', 'foo  \nbar \n  '),
                ('bar.markdown', 'bar   \nbaz\t\n\t\n'),
        ):
            with open(filename, 'w') as file_obj:
                file_obj.write(contents)  # pragma: no branch (26 coverage bug)

        ret = fix_trailing_whitespace(['foo.md', 'bar.markdown'])
        assert ret == 1

        for filename, after_contents in (
                ('foo.md', 'foo  \nbar\n\n'),
                ('bar.markdown', 'bar  \nbaz\n\n'),
        ):
            assert open(filename).read() == after_contents


def test_markdown_linebreak_ext_opt(tmpdir):
    with cwd(tmpdir.strpath):
        for filename, contents in (
                ('foo.txt', 'foo  \nbar \n  \n'),
                ('bar.MD', 'bar   \nbaz\t   \n\t\n'),
                ('bar.markdown', 'baz   \nquux  \t\n\t\n'),
        ):
            with open(filename, 'w') as file_obj:
                file_obj.write(contents)  # pragma: no branch (26 coverage bug)

        ret = fix_trailing_whitespace(['--markdown-linebreak-ext=md,TxT',
                                       'foo.txt', 'bar.MD', 'bar.markdown'])
        assert ret == 1

        for filename, after_contents in (
                ('foo.txt', 'foo  \nbar\n\n'),
                ('bar.MD', 'bar  \nbaz\n\n'),
                ('bar.markdown', 'baz\nquux\n\n'),
        ):
            assert open(filename).read() == after_contents


def test_markdown_linebreak_ext_opt_all(tmpdir):
    with cwd(tmpdir.strpath):
        for filename, contents in (
                ('foo.baz', 'foo  \nbar \n  '),
                ('bar', 'bar   \nbaz\t\n\t\n'),
        ):
            with open(filename, 'w') as file_obj:
                file_obj.write(contents)  # pragma: no branch (26 coverage bug)

        # need to make sure filename is not treated as argument to option
        ret = fix_trailing_whitespace(['--markdown-linebreak-ext', '--',
                                       'foo.baz', 'bar'])
        assert ret == 1

        for filename, after_contents in (
                ('foo.baz', 'foo  \nbar\n\n'),
                ('bar', 'bar  \nbaz\n\n'),
        ):
            assert open(filename).read() == after_contents


def test_no_markdown_linebreak_ext_opt(tmpdir):
    with cwd(tmpdir.strpath):
        for filename, contents in (
                ('bar.md', 'bar   \nbaz\t   \n\t\n'),
                ('bar.markdown', 'baz   \nquux  \t\n\t\n'),
        ):
            with open(filename, 'w') as file_obj:
                file_obj.write(contents)  # pragma: no branch (26 coverage bug)

        ret = fix_trailing_whitespace(['--no-markdown-linebreak-ext',
                                       'bar.md', 'bar.markdown'])
        assert ret == 1

        for filename, after_contents in (
                ('bar.md', 'bar\nbaz\n\n'),
                ('bar.markdown', 'baz\nquux\n\n'),
        ):
            assert open(filename).read() == after_contents


def test_returns_zero_for_no_changes():
    assert fix_trailing_whitespace([__file__]) == 0
