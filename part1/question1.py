class Ruban:
    """ représente le ruban d'une machine de Turing """

    def __init__(self, name, content=["#"]):
        self.content = content
        self.name = name
        self.reading = 0

    def move_left(self):
        if self.reading == 0:
            self.content.insert(0, "#")
            return "#"
        else:
            self.reading -= 1
            return self.content[self.reading]

