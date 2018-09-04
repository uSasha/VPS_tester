import time

import implicit
import numpy as np
import scipy


def test_cpu(data_shape=20000, density=0.01, iterations=45):
    dataset = scipy.sparse.random(data_shape, data_shape,
                                  density=density,
                                  format='csr',
                                  random_state=42,
                                  data_rvs = lambda x: np.ones(x))

    t = time.time()
    estimator = implicit.als.AlternatingLeastSquares(iterations=iterations)
    estimator.fit(dataset)
    return int(time.time() - t)

print(test_cpu())
