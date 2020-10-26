from verbosePrint import vprint
import verbosePrint

def runPredictions(inputData, inputTraining, targetData, targetTraining,
                    nn, cycles):
    if cycles > 0:
        report = max(1, cycles/10)
        nn.checkup(inputData, targetData, inputTraining)
        for iteration in range(cycles + 1):
            vprint(iteration, '~~~~~~~~~~~ Iteration %d ~~~~~~~~~~~' % iteration)
            combinedError = 0
            for row_index in range(len(targetTraining)):
                datain = inputTraining[row_index:row_index + 1]
                goal_prediction = targetTraining[row_index:row_index + 1]
                prediction = nn.fire(datain)
                # print('Prediction:' + str(prediction))
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
    nn.checkup(inputData, targetData, inputTraining)

import p010, f010, intellEQData
from predict import name, nnets

verbosePrint.vIteration = -1
verbosePrint.stage = ''

if 'p010' in nnets:
    runPredictions(
        p010.inputData,
        p010.inputTraining,
        p010.targetData,
        p010.targetTraining,
        nnets['p010']['nnet'],
        nnets['p010']['cycles'],
    )
if 'f010' in nnets:
    runPredictions(
        f010.inputData,
        f010.inputTraining,
        f010.targetData,
        f010.targetTraining,
        nnets['f010']['nnet'],
        nnets['f010']['cycles'],
    )

if 'intellEQData' in nnets:
    runPredictions(
        intellEQData.inputData,
        intellEQData.inputTraining,
        intellEQData.targetData,
        intellEQData.targetTraining,
        nnets['intellEQData']['nnet'],
        nnets['intellEQData']['cycles'],
    )
