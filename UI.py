from PyInquirer import prompt


#UI
class UI:
    separator = "-"*15
    def menu(type_of = "list", name = "def", message = "def", choises = []):
        questions = [{
            "type": f"{type_of}",
            "name": f"{name}",
            "message": f"{message}",
            "choices": choises
        }]
        return prompt(questions)[f"{name}"]
        

    def confirming(message, name):
        questions = [
        {
            'type': 'confirm',
            'message': message,
            'name': f'{name}',
            'default': True,
        }
    ]
        return prompt(questions)[f"{name}"]