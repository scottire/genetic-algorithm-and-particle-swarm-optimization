
import numpy as np

from optproblems.base import Individual, BoundConstraintsChecker
from optproblems.continuous import RastriginFunction, WeierstrassFunction
from optproblems.continuous import griewank, ackley, sphere, TestProblem
from optproblems.cec2005.helper import HybridCompositionFunction



class F15(TestProblem):
    """Hybrid composition function F15."""

    bias = 120.0

    offsets = [[3.3253, -1.2835, 1.8984, -0.4095, 0.0881, 2.758, 0.9776, -1.809, -2.4957, 2.7367, -2.8961, -2.9413, 3.2682, 3.6495, 0.5031, -4.2187, -0.7888, 3.8384, 1.3397, 2.9312, -3.2869, 3.6213, 3.4834, -4.226, -1.0784, -0.4473, 2.7601, 0.0462, 4.3606, -2.0347, -3.5089, -2.2028, -1.6626, -1.7293, 0.0183, -4.0478, -1.4034, -1.7866, -2.4212, -0.7434, -1.5438, -3.0272, 2.6055, -3.1007, 2.801, 1.4532, 2.9887, 0.1249, 3.0169, -1.314, 3.4259, 2.4992, 0.9794, -1.8358, -3.8253, 2.7079, 1.9604, 1.3197, -2.4128, -0.4755, 2.1681, 3.2344, 3.359, -0.0144, -1.8732, -1.9496, 0.4711, 0.8211, -0.1998, 3.735, -0.3372, -1.7267, -0.6595, -3.0531, -4.1052, 2.3991, -0.3267, 1.3279, 3.7907, -1.88, 2.9056, 1.8643, -0.528, -1.9298, -0.8583, 0.6057, -1.4152, 4.0411, 2.1519, 3.6699, -1.3395, 1.5661, -2.4511, -2.3292, 0.1275, -3.0202, -1.09, -3.6965, -1.1674, 1.5488],
               [-2.2465, 3.9382, -0.7999, -4.2205, -2.9393, -4.3433, 1.6348, 3.1011, -0.9269, -2.5328, 1.1839, -2.9094, 2.8157, -2.2581, -0.1202, 4.1264, -3.5397, 0.9927, -3.5492, 3.5247, 0.1342, -3.6413, 1.8572, -3.8112, -0.5177, -4.3274, -3.9499, 1.6129, -3.6689, 3.7438, -2.7323, -3.7832, -0.8912, 2.7046, 4.3176, 1.633, -0.7331, -1.7864, 0.7877, -0.7484, -4.2517, 1.906, -2.8498, -1.5533, 0.469, -2.437, -1.4181, 2.5617, 2.5139, 1.4288, -4.4704, 1.7249, -3.366, -3.3114, 3.7927, 4.3542, -4.1577, -2.0797, -4.1467, 0.9295, -3.0638, 0.3216, -3.3978, -1.011, 2.9571, -2.8415, 3.9917, -0.8307, -2.4358, -0.446, -4.3041, -1.6925, 2.2654, 3.4818, 4.1474, -0.2995, -3.9534, 4.3495, -1.9537, 4.3235, 1.807, 1.8991, 0.436, -2.7083, -2.8008, -3.8717, -2.8596, 3.3523, 1.0176, 0.3075, 1.0646, -2.15, -2.8102, -4.4798, 0.5491, -3.5628, -2.9116, 4.2015, -4.0054, -1.786],
               [1.7378, -4.4943, 0.3191, -3.2414, 1.2388, 2.4878, -4.1218, -2.6083, -0.281, 3.4336, -0.9179, 1.8598, 3.0641, -0.3621, 0.5576, -2.4441, -2.2366, -0.5266, 4.3657, 1.923, 4.1786, -4.0957, -3.1427, 3.2389, 1.5794, -4.2122, 3.6131, -3.7048, -1.1209, -1.3074, 0.3317, -0.7883, -4.1121, 3.4491, 0.8004, 0.464, -2.319, -1.5837, 2.6929, -1.0506, 2.1719, -1.4665, 2.9197, 1.1862, 2.7782, -1.8744, 3.7281, -1.988, 1.7553, -0.0022, 1.8093, -0.1875, 1.0918, 1.4909, -0.3683, -2.6889, 3.4836, -3.856, 2.18, 0.2308, -3.9911, 1.7939, 2.1553, -0.6733, 0.0311, 0.3181, 1.1508, 4.0126, 0.3366, 0.1681, -2.7874, -2.8053, 2.0216, -1.216, -1.0253, -4.3512, 1.047, -4.2517, 1.1389, 1.9587, -2.1917, -3.0772, 1.7597, -1.8843, 0.6544, -3.1522, -2.92, 3.8666, -3.8922, 0.8791, -3.5768, -0.8539, 2.5625, 4.2585, -4.4818, -3.8622, 3.3085, -4.3596, 0.8178, 0.912],
               [-1.5504, -4.3339, 0.8978, -1.3839, 4.2338, 2.6283, -0.859, -1.8942, 1.7407, -1.2537, 1.3161, -3.1738, 2.8559, 0.0554, 4.4044, -0.9942, -4.2987, 3.1463, 2.7438, 0.5779, -0.1439, 0.1275, 0.6657, -4.231, -0.9996, -0.5897, -0.4524, 1.2225, -2.2496, -0.8321, 3.0274, -2.5083, -0.2941, 4.0227, 0.5575, -1.7082, -3.4266, -1.3186, -4.4435, 3.815, -2.4026, -1.9805, -3.9941, 1.7521, -2.4486, -3.564, 2.8962, -4.0694, -2.1251, -0.6647, 0.8677, 1.6697, -3.1888, 2.2569, -4.0996, -2.2851, 3.3932, -2.112, -0.4288, -2.5799, 1.4335, 1.8559, 3.8649, -2.8086, -4.26, 3.8483, -1.1864, 3.9864, 3.1897, -3.5196, 0.0517, -1.6459, 0.6225, 1.6034, -0.2551, 2.3951, -2.9564, 3.4064, -2.692, -2.0972, -4.2272, -4.2909, -1.9785, 2.6433, -2.436, -3.6061, -3.3946, 1.2882, 1.3625, -2.2262, -0.5273, 0.021, -2.2951, 3.5702, 2.355, -3.5396, 4.3945, -0.0075, 1.515, -1.8038],
               [-2.7358, 0.4853, 2.8932, 0.1775, 1.5936, 2.3591, 3.4123, -3.1076, 3.8696, 2.3145, -3.7018, -4.3772, -2.1313, -1.1746, 2.2956, 1.3502, 3.2284, 1.6749, -4.3424, -1.0206, -4.3462, -1.703, 1.6973, -1.5694, -3.0295, 4.1132, -2.1307, -3.9905, -0.4026, -1.662, -0.2478, -3.2789, -1.6622, -1.2509, 3.8842, -1.5414, 3.8323, 3.8892, 0.9131, 1.0501, 0.9815, -2.0173, -1.4322, -2.4151, 1.0046, -3.6765, -1.1788, 0.2702, -0.2876, -0.9539, 2.1957, -0.1247, -4.1052, 3.54, -4.3878, 2.9056, 4.2666, 3.9671, 3.5829, 3.9816, -1.4905, -1.0256, 2.7029, 0.2633, -1.1798, 2.3091, -0.2593, -0.7006, 4.3161, 3.7458, 0.4037, -2.0975, 4.3694, 2.4717, 4.1478, -3.5657, -0.1033, 3.7534, 1.9894, 3.479, -1.8541, 3.847, 1.1231, 4.4799, -3.9805, 1.8823, -1.0147, 4.1805, 4.3017, 1.4542, 2.0347, 2.7745, -1.6727, 3.5495, -0.1187, -3.1237, -3.2825, -0.2343, 1.4084, 2.5355],
               [-1.8717, 1.8285, -3.7085, 2.166, 0.2798, -2.5635, -2.1321, -2.9868, -2.5391, -1.3354, -0.27, -3.0712, -1.7479, 0.042, -3.8396, -3.3518, 3.2361, 3.9031, -3.8211, -0.9072, -4.2347, -3.2265, -1.3196, -0.4069, 2.2933, -1.8828, -1.7421, -1.3624, 2.2034, -1.5554, 3.9148, 3.006, -2.7808, 3.143, -4.3288, 3.1607, 2.9885, 3.477, -3.254, 3.5659, -2.3289, -0.6332, -1.3463, 1.4149, -3.1376, 2.8234, -1.7904, 1.4993, -2.8887, 2.1925, -2.6683, -4.2745, 3.9368, 3.676, 0.3261, 1.3481, -2.0259, -0.352, 0.4502, 1.2222, -1.7436, 3.0571, 1.5054, 0.599, -3.7241, 3.8567, -1.6305, -1.7861, -4.2061, 3.1688, -2.5142, 1.4365, -4.2584, -2.9095, -2.7201, -3.978, -3.8197, 3.2116, -2.0274, 3.379, 2.0176, 3.7376, -1.7626, 3.1218, 1.6559, 3.3415, 1.5242, 1.725, 2.0883, 3.4093, -1.7778, -2.4508, -1.7771, 2.9953, -0.0094, -1.5103, 4.3057, -1.2379, 2.5305, -0.5928],
               [-3.9243, -2.7541, -0.2973, 0.1385, -1.8557, -2.6559, -3.6582, -0.7301, -1.1095, 3.357, 3.0578, -0.9765, 3.6632, 4.0256, -3.2321, -1.0683, -0.2443, -2.6259, -3.6503, -0.2215, 3.5501, 1.5428, -2.3871, 3.3152, -3.1084, -0.6189, 1.6179, -4.4262, 0.3702, 2.644, -0.2132, -3.042, 3.9154, 1.1186, -4.2283, -0.0699, -2.667, -2.9021, 0.0838, 0.5869, 4.4932, -2.5687, 2.3839, -0.5072, -2.3617, -2.2267, -1.8803, 4.0205, -4.3917, -1.3007, 2.2299, -3.8293, -0.0266, -0.4176, 3.4822, -4.377, 1.7739, -3.071, -1.9767, 2.6253, 4.2554, -0.0231, 0.9287, 1.5838, -3.7755, -0.1704, -3.5334, 1.5598, 1.9987, 0.8379, -4.3789, -0.9071, -2.3975, -3.0816, -2.6495, -1.1391, 1.1763, -0.4394, -2.1198, -0.1203, 3.7726, 2.3534, -3.5806, 4.4012, -2.5145, -3.7623, -2.4466, -1.0585, -3.6637, -3.1811, -0.2319, -3.0277, 4.3686, -0.3805, 0.5239, -3.102, 3.6013, -3.2767, 0.8749, 3.7456],
               [-4.4362, -1.0142, 0.2618, 2.5649, 0.9511, -1.2742, -2.099, 0.208, -2.2216, 1.9331, -3.0628, 2.5846, -3.4871, -1.4314, 2.9744, -1.6853, 1.7319, 0.0119, -2.2333, -3.6649, 0.6961, -1.33, -4.0811, 0.23, 1.015, 2.4349, 2.6735, -4.03, 0.6632, -4.3627, 3.9411, -2.8084, -1.2894, 3.2805, 0.087, 0.7132, 1.8993, 2.563, -3.2035, 1.8894, -1.0149, 4.357, 2.6677, -3.4265, -2.6617, 1.4306, -0.32, 3.4067, -0.6862, -0.2662, -2.2974, 0.6611, -0.1139, -0.2793, -4.0534, -2.9895, 2.46, 4.068, 0.6113, -2.1785, 3.5749, 4.2679, 0.7205, -0.3493, -2.4683, 2.8913, -2.7926, -4.4259, 1.6203, -0.7078, 0.0669, 3.3265, -0.8965, 3.8144, 1.8644, -3.874, -4.4329, -2.7533, 1.5199, 2.4951, -4.0784, -1.5782, 2.4547, 1.3106, -1.6517, -2.7385, -1.8217, 2.5841, 3.5956, -4.4051, 1.9856, -1.0218, 1.1335, 3.2501, -0.1125, -3.3356, 0.7337, 0.81, -3.4267, -1.7573],
               [-1.4198, 3.6078, 2.0771, 2.7252, -3.3609, -2.0665, -3.8042, -3.9882, 1.9212, 2.717, -3.6992, 3.0584, 3.1365, 2.5994, -2.2861, 3.2691, -4.3166, 1.5112, -3.4301, -3.1168, -0.4861, -0.2152, -4.4595, -4.4585, 2.749, -3.6245, -4.094, 3.0953, 1.8911, 3.3585, 0.1474, 0.5514, -4.1774, 2.6014, -1.8385, -3.6295, -2.1696, -0.8117, 2.7015, -3.0258, -3.0333, -0.8491, -2.6945, 2.5817, -3.9572, 1.5827, 4.4099, -1.1827, 2.0778, -4.1023, -0.8079, -4.3809, -3.5968, 3.3155, -2.2298, 3.5023, -0.1481, 1.9668, -2.9158, 2.4857, 4.1099, -4.116, -1.6791, -3.2401, 1.3775, 0.9058, 3.7376, 2.2668, 3.8236, -0.9997, 1.4778, 0.1698, -1.4464, 0.7047, -2.8071, -0.8797, -1.8638, 1.7548, -1.9996, 1.5675, 2.9245, -0.1109, -2.0504, -1.2071, -2.4366, -3.8301, 4.1004, -4.1967, -0.0933, -1.1239, 2.9965, 0.9228, -1.4416, -0.0095, -3.3145, 3.4467, -0.9867, 2.5468, 0.3522, 3.4812],
               [-2.4369, -2.3015, 1.1539, 1.5121, -0.2417, 0.2086, -1.4078, 3.2117, 0.1618, -2.6028, -0.528, -1.7132, -0.4461, -3.618, 2.4411, 1.512, 0.069, -1.1301, -1.9017, -2.742, -2.613, -3.4728, 2.7522, 4.2066, -0.6171, -2.9867, 3.4816, 3.3065, -3.1555, 2.4976, 1.4455, -1.9139, -2.411, -3.8611, 4.487, 3.3597, 1.9467, -3.0049, 2.6107, 3.7599, -2.3608, -4.4512, -2.7817, 3.6587, -0.0434, 1.3095, -4.2113, 1.0998, 1.5087, 1.8103, 2.7342, 0.1698, 4.1891, -4.2409, 4.1945, -1.4423, 2.0603, 3.5687, 0.225, 2.9241, 3.2211, 2.0296, 2.3792, 2.8299, 1.1196, 3.5512, -3.7236, 4.1712, -0.7013, -3.1732, 0.0377, 4.3992, -1.0487, -3.2646, 4.1234, -1.2268, 3.0004, 2.2522, -1.4002, 2.0008, 2.7492, 0.3219, 0.2304, 1.9087, 0.6672, 0.9471, -1.3234, -1.1531, 1.6404, 3.7113, 1.1623, 2.8554, -2.2389, -1.465, -3.6592, -0.7341, -2.8758, 2.2515, 1.578, -3.7634]]

    sigmas = [1.0,	1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    lambdas = [1.0, 1.0, 10.0, 10.0, 5.0 / 60.0, 5.0 / 60.0, 5.0 / 32.0,
               5.0 / 32.0, 5.0 / 100.0, 5.0 / 100.0]

    biases = [0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]

    def __init__(self, num_variables,
                 matrices=None,
                 offsets=None,
                 phenome_preprocessor=None,
                 **kwargs):
        rastrigin = RastriginFunction()
        weierstrass = WeierstrassFunction()
        basic_functions = [rastrigin, rastrigin, weierstrass, weierstrass,
                           griewank, griewank, ackley, ackley, sphere, sphere]
        if matrices is None:
            matrices = [np.identity(num_variables)] * 10
        if offsets is None:
            offsets = self.offsets
        self.hybrid_composition_function = HybridCompositionFunction(num_variables,
                                                                     basic_functions,
                                                                     matrices,
                                                                     self.sigmas,
                                                                     self.lambdas,
                                                                     self.biases,
                                                                     offsets,
                                                                     2000.0,
                                                                     name="Hybrid Composition Function 1")
        self.num_variables = num_variables
        self.is_deterministic = True
        self.do_maximize = False
        self.min_bounds = [-5.0] * num_variables
        self.max_bounds = [5.0] * num_variables
        bounds = (self.min_bounds, self.max_bounds)
        preprocessor = BoundConstraintsChecker(bounds, phenome_preprocessor)
        TestProblem.__init__(self, self.objective_function,
                             phenome_preprocessor=preprocessor,
                             **kwargs)


    def get_optimal_solutions(self, max_number=None):
        return [Individual(self.offsets[0][:self.num_variables])]


    def objective_function(self, phenome):
        obj_value = self.hybrid_composition_function(phenome) + self.bias
        return obj_value
