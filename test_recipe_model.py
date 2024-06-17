from recipe_model import Recipe


def test_new_recipe_id():
    r = Recipe(1, "Blob", [], [])
    assert r.id() == 1


def test_new_recipe_name():
    r = Recipe(1, "Blob", [], [])
    assert r.name() == "Blob"
