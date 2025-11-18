from models.example_model import ExampleModel

class ExampleController:
    def __init__(self):
        self.model = ExampleModel()

    def add_one(self):
        return self.model.increment()
