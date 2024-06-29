from dataclasses import dataclass
import json
from json import JSONEncoder


class Recipe(JSONEncoder):
    db = {}

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
            self.id_ = len(Recipe.db)
        Recipe.db[self.id_] = self
        Recipe.save_db()

    @classmethod
    def clear(cls):
        cls.db.clear()

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
        print(f"Get {id} from {cls.db.values()}")
        if id > len(cls.db.values()):
            return None
        else:
            return list(cls.db.values())[id]

    @classmethod
    def save_db(cls):
        with open("data.json", "w") as file:
            file.write(json.dumps(list(cls.db.values())))

    def default(self, o):
        if isinstance(o, Recipe):
            return {
                "name": self.name_,
                "description": self.description_,
                "ingredients": [i.__dict__ for i in self.ingredients_],
                "instructions": self.instructions_,
            }
        return super().default(o)

    @classmethod
    def load_db(cls):
        pass

    @classmethod
    def load_recipe(cls):
        pass


@dataclass
class Ingredient:
    name: str
    qty: int
    unit: str
