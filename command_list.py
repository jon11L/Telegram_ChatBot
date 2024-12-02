def get_list_command():
    with open("templates/command_list.md", "r") as file:
        commands = file.read()
        return commands
