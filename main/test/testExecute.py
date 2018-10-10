from main.src.application.Execute import *
from main.src.application.predication.PredictionURL import *


def rate(x):
    random = np.random.normal(0, 0.1, 1)[0]
    # print(random)
    return -0.012 * x + 18 + random


if __name__ == '__main__':
    x = [round(rate(x), 2) for x in range(300)]
    history = x[:100]
    fit = Polyfit(range(len(history)), history, 1)
    execute = Execute()
    execute.set_algorithm(fit)
    execute.execute()
