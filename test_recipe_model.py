from recipe_model import Recipe


class TestRecipe:
    def setup_method(method):
        Recipe.clear()  # Clear the db before each test

    def test_save_recipe(self):
        r = Recipe("Test1", [], [])
        r.save()
        recipes = Recipe.all()
        assert len(recipes) == 1
        assert recipes[0].id() == 0
        assert recipes[0].name() == "Test1"
        assert recipes[0].ingredients() == []
        assert recipes[0].instructions() == []

    def test_save_two_recipes(self):
        r1 = Recipe("Test2", [], [])
        r2 = Recipe("Test3", [], [])
        r1.save()
        r2.save()
        recipes = Recipe.all()
        assert len(recipes) == 2
        assert recipes[0].id() == 0
        assert recipes[0].name() == "Test2"
        assert recipes[0].ingredients() == []
        assert recipes[0].instructions() == []
        assert recipes[1].id() == 1
        assert recipes[1].name() == "Test3"
        assert recipes[1].ingredients() == []
        assert recipes[1].instructions() == []

    def test_find_recipe_exact(self):
        r = Recipe("sandwich", [], [])
        r.save()
        result = Recipe.find("sandwich")
        assert len(result) == 1

    def test_find_recipe_partial(self):
        r = Recipe("sandwich", [], [])
        r.save()
        result = Recipe.find("sand")
        assert len(result) == 1

    def test_find_recipe_not_found(self):
        r = Recipe("sandwich", [], [])
        r.save()
        result = Recipe.find("omelette")
        assert len(result) == 0
