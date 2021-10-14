class Synthesizer:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"the {self.name} synthesizer"

    def play(self):
        return "is playing an electronic song"


class Human:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name} the human"

    def speak(self):
        return "say hello"
