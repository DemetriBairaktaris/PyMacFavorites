import pytest
import getpass
import tempfile
import os
import py_mac_favorites


def test_get_favorites():
    assert py_mac_favorites.get_favorites(getpass.getuser()) is not None


def test_is_favorite():
    favorites = py_mac_favorites.get_favorites(getpass.getuser())
    assert favorites
    assert py_mac_favorites.is_favorite(getpass.getuser(), favorites[0])


def test_is_favorite_input_is_missing_trailing_slash():
    favorites = py_mac_favorites.get_favorites(getpass.getuser())
    assert favorites
    favorite = favorites[0]
    favorite = favorite.rstrip('/')
    assert py_mac_favorites.is_favorite(getpass.getuser(), favorite)


def test_is_favorite_input_has_trailing_slash():
    favorites = py_mac_favorites.get_favorites(getpass.getuser())
    assert favorites
    favorite = favorites[0]
    favorite = favorite.rstrip('/') + '/'
    assert py_mac_favorites.is_favorite(getpass.getuser(), favorite)


def test_is_favorite_none_path():
    with pytest.raises(Exception):
        py_mac_favorites.is_favorite(getpass.getuser(), None)


def test_is_favorite_empty_str():
    with pytest.raises(Exception):
        py_mac_favorites.is_favorite(getpass.getuser(), "")


def test_add_favorite():
    current_favorites = py_mac_favorites.get_favorites(getpass.getuser())
    new_dir = tempfile.TemporaryDirectory()

    assert new_dir.name not in current_favorites
    assert os.path.exists(new_dir.name)
    py_mac_favorites.set_favorite(getpass.getuser(), new_dir.name)
    assert py_mac_favorites.is_favorite(getpass.getuser(), new_dir.name)
    py_mac_favorites.delete_favorite(getpass.getuser(), new_dir.name)
    new_dir.cleanup()


def test_delete_favorite():
    current_favorites = py_mac_favorites.get_favorites(getpass.getuser())
    new_dir = tempfile.TemporaryDirectory()

    assert new_dir.name not in current_favorites
    assert os.path.exists(new_dir.name)
    py_mac_favorites.set_favorite(getpass.getuser(), new_dir.name)
    assert py_mac_favorites.is_favorite(getpass.getuser(), new_dir.name)
    py_mac_favorites.delete_favorite(getpass.getuser(), new_dir.name)
    assert not py_mac_favorites.is_favorite(getpass.getuser(), new_dir.name)
    new_dir.cleanup()



