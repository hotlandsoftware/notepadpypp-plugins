from PyQt6.QtWidgets import QMessageBox

def register(plugin_api):
    """Registers the Brainfuck Interpreter plugin."""

    plugin_api.add_action_to_plugin_menu(
        "Brainfuck Interpreter", "Interpret Open Document", lambda: interpret_bf(plugin_api)
    )
    plugin_api.add_action_to_plugin_menu(
        "Brainfuck Interpreter", "About", lambda: about_box(plugin_api.app)
    )

def about_box(parent=None):
    """Displays an about box."""
    QMessageBox.about(
        parent,
        "Brainfuck Interpreter",
        "<h3><center>Brainfuck Interpreter</center></h3>"
        "<p>A Brainfuck Interpreter for NotepadPy++</p>"
        "<p>By Hotlands Software</p>"
    )

def brainfuck_interpreter(code, input_func=None):
    """
    executes brainfuck code
    """
    array = [0]
    index = 0
    x = 0
    output = []
    loop_stack = []

    if input_func is None:
        input_func = lambda: input(">>> ")

    bracket_map = {}
    stack = []
    for i, char in enumerate(code):
        if char == "[":
            stack.append(i)
        elif char == "]":
            if not stack:
                raise ValueError("unmatched ']' at position {}".format(i))
            start = stack.pop()
            bracket_map[start] = i
            bracket_map[i] = start
    if stack:
        raise ValueError("unmatched '[' at position {}".format(stack[-1]))

    while x < len(code):
        char = code[x]
        if char == ">":
            index += 1
            if index == len(array):
                array.append(0)
        elif char == "<":
            index -= 1
            if index < 0:
                raise IndexError("pointer moved to negative position")
        elif char == "+":
            array[index] = (array[index] + 1) % 256
        elif char == "-":
            array[index] = (array[index] - 1) % 256
        elif char == ".":
            output.append(chr(array[index]))
        elif char == ",":
            user_input = input_func()
            if user_input:
                array[index] = ord(user_input[0])
            else:
                array[index] = 0
        elif char == "[":
            if array[index] == 0:
                x = bracket_map[x]
        elif char == "]":
            if array[index] != 0:
                x = bracket_map[x]
        x += 1

    return ''.join(output)


def interpret_bf(plugin_api):
    """Runs the Brainfuck interpreter on the current text."""
    text = plugin_api.get_text_of_document()
    if text is None:
        return

    try:
        output = brainfuck_interpreter(text) 
        if output:
            QMessageBox.information(None, "Brainfuck Output", f"Output:\n{output}")
        else:
            QMessageBox.information(None, "Brainfuck Output", f"No output was produced...")
    except Exception as e:
        QMessage.criticial(None, "Error", f"Error: {e}")