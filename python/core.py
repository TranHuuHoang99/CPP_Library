from helper import *
from NeuralBase import NeuralBase


class core(NeuralBase):
    def __init__(self, image: np.ndarray) -> None:
        super().__init__(image)
    
    def sigmoid(self, features: np.float64) -> np.float64:
        return 1 / (1 + np.exp(-features))

    def softmax(self, features: np.ndarray) -> np.ndarray:
        return np.exp(features) / np.exp(features).sum()

    def lerp(self, alpha: np.float64, omega: np.float64, range_rate = 0.5) -> np.float64:
        return alpha + (omega - alpha) * range_rate