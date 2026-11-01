"""Two ways of responding to the same thought."""

DECAY = 0.78            # activation settles a little before every new thought
SETTLE = 0.04           # a neutral or positive thought calms things slightly

WEIGHTS = {
    "A": 0.78,          # fused: a thought is treated as a fact
    "B": 0.28,          # observing: the thought is noticed before reacting
}


def respond(activation, thought, agent):
    text, category, intensity = thought
    activation *= DECAY
    if category == "negative":
        activation += intensity * WEIGHTS[agent]
    else:
        activation -= SETTLE
    return max(activation, 0.0)


def simulate(thoughts, agent):
    activation = 0.0
    history = [activation]
    for thought in thoughts:
        activation = respond(activation, thought, agent)
        history.append(activation)
    return history
