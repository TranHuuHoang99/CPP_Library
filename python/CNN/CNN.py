from lib import *
import helper as nn

class CNN:
    def __init__(self) -> None:
        self.model = nn.sequence(
            conv=[
                nn.conv3d(kernel_size=[3,3,3]),
                nn.conv3d(kernel_size=[3,3,3]),
                nn.maxpooling(kernel_size=[2,2,3]),

                nn.conv3d(kernel_size=[3,3,3]),
                nn.conv3d(kernel_size=[3,3,3]),
                nn.maxpooling(kernel_size=[2,2,3]),

                nn.conv3d(kernel_size=[3,3,3]),
                nn.conv3d(kernel_size=[3,3,3]),
                nn.maxpooling(kernel_size=[2,2,3]),
            ],
            fc=[
                nn.flatten(),
                nn.linear(features_in=243, features_out=124),
                nn.relu(),
                
                nn.linear(features_in=124, features_out=62),
                nn.relu(),

                nn.linear(features_in=62, features_out=31),
                nn.relu(),

                nn.linear(features_in=31, features_out=7),
                nn.relu()
            ]
        )