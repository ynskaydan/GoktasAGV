import mapping

db_state_a = open("./Database/db_state.txt", "w")
db_state_r = open("./Database/db_state.txt", "r")
last_state = ""
def main():
    global last_state
    lines = db_state_r.readlines()
    if len(lines) > 0:
        last_state = str(lines[len(lines)-1])
        print(last_state)
    else:
        last_state = "explore"

    mode_functions = {
        "explore": run_explore_mode,
        "import": run_import_mode,
        "export": run_export_mode,
        "duty": run_duty_mode,
    }
    if last_state in mode_functions:
        mode_functions[last_state]()


def run_explore_mode():
    print("Mapping active")
    save_last_state("explore")
    try:
        result = mapping.main()
        if result:
            run_duty_mode()
    except AssertionError:
        print("Cannot start a process twitce")


def run_duty_mode():
    print("Duty active")
    save_last_state("duty")




def run_import_mode():
    save_last_state("import")
    try:
        print("importing")
    except AssertionError:
        print("Cannot start a process twitce")


def run_export_mode():
    save_last_state("export")
    try:
        print("exporting")
    except AssertionError:
        print("Cannot start a process twitce")


def save_last_state(to_save_state):
    global last_state
    last_state = to_save_state
    db_state_a.write(str(last_state))
