import prompt_toolkit
from prompt_toolkit.filters.cli import IsDone
from prompt_toolkit.layout.containers import ConditionalContainer, FloatContainer, HSplit, Window
from prompt_toolkit.layout.dimension import D

chss = ["choice 1", "choice 2", "choice 3", "choice 4", "choice 5"]

from prompt_toolkit import print_formatted_text, HTML

for item in chss:
    print_formatted_text(HTML(f'<style fg="ansigreen">{item}</style>'))
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.layout import Container
from prompt_toolkit.layout import Layout

def generate_menu(choises: list):
    checkpoints = []
    i = 1
    for item in choises:
        checkpoints.append((str(f"{item}"), item))
        i+=1
    return checkpoints
print(generate_menu(chss))
buttons_style = Style.from_dict({
    'button.arrow': 'bg:#ffffff'
})
layout = FloatContainer(content=Window(content=button_dialog(buttons=generate_menu(chss))))
result = prompt_toolkit.Application(layout=layout)