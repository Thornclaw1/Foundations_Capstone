def int_input(prompt = ""):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except:
            print("Input must be an integer number.")

def strict_input(prompt = "", valid_inputs = []):
    if len(valid_inputs) <= 0:
        return
    valid_inputs = [i.lower() for i in valid_inputs]
    while (user_input := input(prompt).lower()) not in valid_inputs:
        print("Invalid Input")
    return user_input