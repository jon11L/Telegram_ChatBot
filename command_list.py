def get_list_command():
    with open("command_list.md", "r") as file:
        commands = file.read()
        return commands
