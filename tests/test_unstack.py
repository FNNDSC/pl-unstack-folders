import pytest
from pathlib import Path
from unstack import parser, main


def test_copy_file(dirs, empty_args):
    inputdir, outputdir = dirs
    nested_file = inputdir / 'a' / 'b' / 'c.dat'
    nested_file.parent.mkdir(parents=True)
    nested_file.write_text('fish are friends not food')
    main(empty_args, inputdir, outputdir)
    expected = outputdir / 'c.dat'
    assert expected.is_file()
    assert expected.read_text() == 'fish are friends not food'


def test_copy_multiple_dirs(dirs, empty_args):
    inputdir, outputdir = dirs
    multiple_dirs_helper(inputdir, outputdir, empty_args)


def test_ignores_special_files(dirs, empty_args):
    inputdir, outputdir = dirs
    (inputdir / 'input.meta.json').write_text('{}')
    (inputdir / 'output.meta.json').write_text('{}')
    multiple_dirs_helper(inputdir, outputdir, empty_args)


def multiple_dirs_helper(inputdir: Path, outputdir: Path, empty_args):
    file1 = inputdir / 'animals' / 'fish' / 'pufferfish.dat'
    file2 = inputdir / 'animals' / 'mammal' / 'dolphin.dat'

    for f in (file1, file2):
        f.parent.mkdir(parents=True)
        f.write_text('is an animal')

    main(empty_args, inputdir, outputdir)
    assert (outputdir / 'fish').is_dir()
    assert (outputdir / 'fish' / 'pufferfish.dat').is_file()
    assert (outputdir / 'mammal').is_dir()
    assert (outputdir / 'mammal' / 'dolphin.dat').is_file()


@pytest.fixture
def dirs(tmp_path: Path):
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()
    return inputdir, outputdir


@pytest.fixture
def empty_args():
    return parser.parse_args([])
