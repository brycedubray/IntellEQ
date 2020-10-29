import intellEQData as data
import numpy as np
from nnet import NNet
from verbosePrint import vprint
import verbosePrint


nn = NNet(sizes=[6, 12, 6], bias=False)
# nn = NNet([[[...]],
#   [...]], bias=True)

nn.setActivations(['tanh', 'softmax'])
nn.setAlpha(0.01)
nn.setVerbose([])

nn.checkup(data.inputData, data.targetData)

verbosePrint.vIteration = -1
verbosePrint.stage = ''

cycles = 100
report = cycles/10

for iteration in range(cycles + 1):
    vprint(iteration, '~~~~~~~~~~~ Iteration %d ~~~~~~~~~~~' % iteration)
    combinedError = 0
    for row_index in range(len(data.targetTraining)):
        datain = data.inputTraining[row_index:row_index + 1]
        goal_prediction = data.targetTraining[row_index:row_index + 1]
        prediction = nn.fire(datain)
        vprint(iteration, nn)

        error = (goal_prediction - prediction) ** 2
        combinedError += error

        nn.learn(datain, goal_prediction)

    if iteration % report == 0:
        print('Iteration: %d Error: %s' % (iteration, str(combinedError)))
    vprint(iteration, '')
    vprint(iteration, '~~~~~~~~~~~~~~~ End ~~~~~~~~~~~~~~~~')
    vprint(iteration, nn, quit=True)

print()
nn.checkup(data.inputData, data.targetData)