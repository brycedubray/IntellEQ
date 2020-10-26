from nnet import NNet

nn1 = NNet(
    # weights=[[[...],        # start with weights 0-1,
    #            ...          # the reverse of the output
    #           [...]],       # inner []' for each row,
    #          [[...],        # middle []'s for each layer,
    #               ]]]       #
    sizes=[6, 6, 4],           # connect [input, hidden, ..., output] layers
                            # with 2D lists of random weights
                            # comment this out when weights are specified
    # bias=[True],           # specify if any are True
    # batch_size=1,           # raise this for faster training
    )
nn1.scale([1.0])                  # rescale if node sums are too large
nn1.setAlpha([0.1])               # rescale if weights overshoot target
nn1.setActivations(['relu', 'linear'])    # specify if any are non-linear

##############################################################################

nn2 = NNet(
    # weights=[[[...],        # start with weights 0-1,
    #            ...          # the reverse of the output
    #           [...]],       # inner []' for each row,
    #          [[...],        # middle []'s for each layer,
    #               ]]]       #
    sizes=[6, 10, 4,],           # connect [input, hidden, ..., output] layers
                            # with 2D lists of random weights
                            # comment this out when weights are specified
    # bias=[True],           # specify if any are True
    batch_size=1000,           # raise this for faster training
    )

nn2.scale([1.0])                  # rescale if node sums are too large
nn2.setAlpha([0.0001])               # rescale if weights overshoot target
nn2.setActivations(['tanh', 'linear'])    # specify if any are non-linear

##############################################################################

nn3 = NNet(
    # weights=[[[...],        # start with weights 0-1,
    #            ...          # the reverse of the output
    #           [...]],       # inner []' for each row,
    #          [[...],        # middle []'s for each layer,
    #               ]]]       #
    sizes=[6, 4, 1],           # connect [input, hidden, ..., output] layers
                            # with 2D lists of random weights
                            # comment this out when weights are specified
    # bias=[True],           # specify if any are True
    # batch_size=1000,           # raise this for faster training
    )

nn3.scale([1.0])                  # rescale if node sums are too large
nn3.setAlpha([0.01])               # rescale if weights overshoot target
nn3.setActivations(['sigmoid', 'linear'])    # specify if any are non-linear

##############################################################################

name = 'DuBray, Bryce'

nnets = {
    # 'p010' : {
    #     'nnet' : nn1,
    #     'cycles' : 100,
    # },
    # 'f010' : {
    #     'nnet' : nn2,
    #     'cycles' : 10000,
    # },
    'intellEQData': {
        'nnet': nn3,
        'cycles': 1000,
    },
}