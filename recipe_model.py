from dataclasses import dataclass
import json
import os


class Recipe:
    db = {}
    maxIdx = 0

    def __init__(
        self,
        name,
        description,
        ingredients,
        instructions,
        id=None,
    ) -> None:
        self.id_ = id
        self.name_ = name
        self.description_ = description
        self.ingredients_ = ingredients
        self.instructions_ = instructions

    def __str__(self):
        return f"{self.id_}:{self.name_}"

    def to_json(self):
        return {
            "id": self.id_,
            "name": self.name_,
            "description": self.description_,
            "ingredients": [i.__dict__ for i in self.ingredients_],
            "instructions": self.instructions_,
        }

    def id(self):
        return self.id_

    def name(self):
        return self.name_

    def description(self):
        return self.description_

    def ingredients(self):
        return self.ingredients_

    def instructions(self):
        return self.instructions_

    def save(self):
        if self.id_ is None:
            Recipe.maxIdx += 1
            self.id_ = Recipe.maxIdx
        Recipe.db[self.id_] = self
        Recipe.save_db()

    def update(self, name, desc, ings, inss):
        self.name_ = name
        self.description_ = desc
        self.ingredients_ = ings
        self.instructions_ = inss
        Recipe.save_db()

    @classmethod
    def clear(cls):
        cls.db.clear()
        cls.maxIdx = -1

    @classmethod
    def all(cls):
        return list(cls.db.values())

    @classmethod
    def find(cls, query):
        result = []
        for r in list(cls.db.values()):
            if r.name().find(query) >= 0:
                result.append(r)
        return result

    @classmethod
    def get_by_id(cls, id: int):
        if id > Recipe.maxIdx:
            return None
        else:
            return cls.db.get(id)

    @classmethod
    def delete(cls, id: int):
        if id in cls.db.keys():
            cls.db.pop(id)
            cls.save_db()
            return True
        else:
            return False

    @classmethod
    def save_db(cls):
        with open("data.json", "w") as file:
            json.dump([r.to_json() for r in cls.db.values()], file)

    @classmethod
    def load_db(cls):
        if not os.path.exists("data.json"):
            return
        with open("data.json", "r") as file:
            data = json.load(file)
            cls.clear()
            for recipe_json in data:
                cls.load_recipe(recipe_json)
            if cls.db:
                cls.maxIdx = max(cls.db.keys())

    @classmethod
    def load_recipe(cls, recipe_json):
        id = recipe_json["id"]
        name = recipe_json["name"]
        description = recipe_json["description"]
        ingredients = [
            Ingredient(i["name"], i["qty"], i["unit"])
            for i in recipe_json["ingredients"]
        ]
        instructions = recipe_json["instructions"]
        recipe = Recipe(name, description, ingredients, instructions, id)
        cls.db[id] = recipe


@dataclass
class Ingredient:
    name: str
    qty: int
    unit: str
