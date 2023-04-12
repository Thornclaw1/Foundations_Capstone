def int_input(prompt = ""):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except:
            print("Input must be an integer number.")