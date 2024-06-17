class Recipe:
    db = {}

    def __init__(self, id, name, ingredients, instructions) -> None:
        self.id_ = id
        self.name_ = name
        self.ingredients_ = ingredients
        self.instructions_ = instructions

    def id(self):
        return self.id_

    def name(self):
        return self.name_
