import pytest


@pytest.mark.usefixtures("delete_objects")
def test_pass():
    pass
