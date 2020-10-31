import intellEQData as data
import numpy as np
from nnet import NNet
from verbosePrint import vprint
import verbosePrint


nn = NNet(sizes=[6, 10, 6], bias=False)
# nn = NNet(
#     [
# [[ -4.63062667,   5.55534467,  -6.26795674,   8.71788279,
#    -3.11965529,   8.45680339,  -3.75482917,   2.69648063,
#    -3.55995718,   5.67967537],
#  [ -9.13485854,  -0.93347476,   2.83015148,  -2.63206899,
#     3.66757328,  -3.47390989,   0.7282168 ,  -0.07214673,
#    -0.39770918,   0.4783496 ],
#  [ -7.4200791 ,  -3.17101485,   3.2039981 ,  -2.50007489,
#     0.60453387,  -2.21378867,   1.09984089,   0.87755381,
#     3.80336622,  -3.0866793 ],
#  [ -1.99866325,  -0.49572462,   0.49011899,   3.23738815,
#    -0.27288502,   1.52611754,  -1.53040481,  -0.37754143,
#    -0.05229698,  -1.37360362],
#  [ -3.2229334 ,   0.08163043,  -2.69336342,   5.25900123,
#    -3.74544744,   7.25113436,  -1.73482223,  -1.88707165,
#     2.12460176,  -2.9443471 ],
#  [-20.56720696,   0.83424906,   4.16223675,   7.01755949,
#     3.28225537,  -0.65694406,  -7.24202993,  -0.66570467,
#    -0.75064523,   0.58505399]],
#
# [[ 1.61467417, -7.9255745 ,  0.72500528,  4.62848202,  5.2149996 ,
#   -3.37342491],
#  [ 1.76821003, -4.81288625,  0.77511274, -0.99992006,  2.89071572,
#   -0.17603975],
#  [-2.58707043,  5.13553077,  2.33521361, -2.18657136, -5.50967429,
#    2.21987187],
#  [ 1.41752586, -8.23689651, -1.02871536,  5.1408611 ,  4.86486689,
#   -3.84201542],
#  [-1.11598594,  2.38288176,  3.56441339, -3.03265452, -3.8318429 ,
#    2.49088945],
#  [ 3.51797288, -4.30403529, -3.67428102,  3.11394713,  6.61974672,
#   -4.32946125],
#  [-0.8270185 ,  5.49291557, -0.61610242, -2.43111137,  0.1465889 ,
#    0.56452161],
#  [ 0.73574445, -0.56110153, -0.25599447, -1.92165886,  2.15144415,
#    1.07560305],
#  [ 0.24746464,  4.55708372, -1.74484014,  0.69004326, -1.53094026,
#   -1.33841757],
#  [-0.5930905 , -4.43709331,  1.99206425, -2.30516911,  3.26082548,
#    1.72717205]],
#     ], bias=False)

nn.setActivations(['tanh', 'softmax'])
nn.setAlpha(0.1)
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