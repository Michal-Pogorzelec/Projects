import turtle
import pandas as pd

screen = turtle.Screen()
screen.title("U.S States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pd.read_csv("50_states.csv")
states = data.state.to_list()

score = 0
guessed_states = []
while len(guessed_states) < 50:
    answer_state = screen.textinput(title=f"{score}/50 states guessed", prompt="What's another state's name?").title()

    if answer_state == "Exit":
        states_to_learn = pd.DataFrame([state for state in states if state not in guessed_states])
        states_to_learn.to_csv("states_to_learn.csv")
        break
    if answer_state in states and answer_state not in guessed_states:
        score += 1
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == answer_state]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(answer_state) # == state_data.state.item()
        print(answer_state)
