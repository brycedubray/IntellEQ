import intellEQData as data
import numpy as np
from nnet import NNet
from verbosePrint import vprint
import verbosePrint

# single hidden layer
# nn = NNet(sizes=[6, 12, 6], bias=False)

#dropout mask
# nn.setMaskPr({1:0.1,})

#multiple hidden layers
# nn = NNet(sizes=[6, 12, 8, 6, 6], bias=False)

nn = NNet(
    [
        [[  2.84713837,  -8.78179412,   8.10642596,  -3.07793699,
  -10.80106264,  14.01156433, -18.9043836 ,  -4.55229157,
   -9.9537589 ,  -5.20987197,  -3.21562769,  -4.5607828 ],
 [  5.30913524,   0.6314736 ,  18.14815193,   6.72997545,
    2.9721378 ,  -0.36195361,   5.79830519,  -2.15274801,
   -1.12867008,  -2.20018947,   0.80194759,  -0.24958515],
 [ -2.32867818,   7.14527551,  19.18658728,   1.08424264,
    1.79629953, -11.87324217,  -6.4333367 ,   0.72700125,
    5.97294048,   4.26465857,   2.71164742,   2.8539153 ],
 [ -0.32870074,   3.16858712,   1.03051466,   0.2930736 ,
   -8.94892582,  -0.25599383,   2.14446   ,   1.6952578 ,
   -0.07452218,  -0.15187008,   0.88328428,   1.21156438],
 [  3.67849772,   1.30959682,   1.31214265,   7.76681032,
  -11.00540518,   5.63113094, -21.03427057,   3.14642769,
    0.34106142,   1.51081889,   0.1954099 ,   2.75789373],
 [ -1.08633587,   3.96052528,  37.63333947,  -4.1849973 ,
  -17.66288288,  -6.18750346,   4.80467367,  -1.64123495,
    0.42739357,   0.06805955,   0.16489447,   0.05045559]],

[[  0.27059243,  -1.28155827,   2.18912658,  -0.56854281,
    1.49552506,  -1.02965568],
 [ -1.4523649 ,   2.04294604,   1.79014307,   1.4962308 ,
   -2.31881794,   0.46701864],
 [-12.24161793,  14.10357459,  -3.02604739,  -2.30608958,
   -3.51082185,   5.50803644],
 [ -0.26170974,   3.07415144,  -1.59509651,  -0.44449528,
    1.80013705,  -4.04822311],
 [-12.74406728,  15.97083107,  -4.30440871,  -0.98917903,
    1.60299493,   1.48986101],
 [  2.8961228 ,  -3.63141757,  -1.72788706,   0.37525444,
    3.63204028,  -2.68670456],
 [ -0.98194825,   1.54797654,   8.36244941,  -2.98278101,
  -11.72353983,   5.46823633],
 [  1.22599138,   2.52183056,  -2.62403899,   2.15309222,
    0.90253033,  -2.4040307 ],
 [ -0.05004978,   3.31078448,  -2.42175962,   1.486422  ,
   -1.20490127,  -1.56176666],
 [ -0.56573403,   2.47968879,  -2.08230618,   0.47269856,
   -0.90033001,  -0.70002158],
 [  0.1043163 ,   0.33045004,   0.49502941,   1.18612121,
   -0.86582592,   0.49505496],
 [ -0.79519934,   2.76698927,  -1.23578411,  -0.05324828,
   -0.06226757,  -1.12721533]],

    ], bias=False)

# single hidden layer
nn.setActivations(['tanh', 'softmax'])

#multiple hidden layers
# nn.setActivations(['tanh', 'tanh', 'tanh', 'softmax'])
nn.setAlpha(0.1)
nn.setVerbose([])

nn.checkup(data.inputData, data.targetData)

verbosePrint.vIteration = -1
verbosePrint.stage = ''

cycles = 1000
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