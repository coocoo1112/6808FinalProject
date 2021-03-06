import numpy as np
from numpy.linalg import inv

# code pulled from https://medium.com/@jaems33/understanding-kalman-filters-with-python-2310e87b8f48


x_observations = np.array([4000, 4260, 4550, 4860, 5110])
v_observations = np.array([280, 282, 285, 286, 290])


def prediction2d(x, v, t, a):
    A = np.array([[1, t],
                  [0, 1]])
    X = np.array([[x],
                  [v]])
    B = np.array([[0.5 * t ** 2],
                  [t]])
    X_prime = A.dot(X) + B.dot(a)
    return X_prime


def covariance2d(sigma1, sigma2):
    cov1_2 = sigma1 * sigma2
    cov2_1 = sigma2 * sigma1
    cov_matrix = np.array([[sigma1 ** 2, cov1_2],
                           [cov2_1, sigma2 ** 2]])
    return np.diag(np.diag(cov_matrix))


def get_position_update(x_observations, v_observations):
    z = np.c_[x_observations, v_observations]
    # Initial Conditions
    a = 0  # Acceleration
    v = 0
    t = 0.1  # Difference in time

    # Process / Estimation Errors
    error_est_x = .1
    error_est_v = .1

    # Observation Errors
    error_obs_x = .1  # Uncertainty in the measurement
    error_obs_v = .1
    
    #initial covariance matrix estimation
    P = covariance2d(error_est_x, error_est_v)
    A = np.array([[1, t],
                [0, 1]])

    # Initial State Matrix
    X = np.array([[z[0][0]],
                [v]])
    n = len(z[0])

    for data in z[1:]:
        X = prediction2d(X[0][0], X[1][0], t, a)
        # To simplify the problem, professor
        # set off-diagonal terms to 0.
        P = np.diag(np.diag(A.dot(P).dot(A.T)))

        # Calculating the Kalman Gain
        H = np.identity(n)
        R = covariance2d(error_obs_x, error_obs_v)
        S = H.dot(P).dot(H.T) + R
        K = P.dot(H).dot(inv(S))

        # Reshape the new data into the measurement space.
        Y = H.dot(data).reshape(n, -1)

        # Update the State Matrix
        # Combination of the predicted state, measured values, covariance matrix and Kalman Gain
        X = X + K.dot(Y - H.dot(X))

        # Update Process Covariance Matrix
        P = (np.identity(len(K)) - K.dot(H)).dot(P)
    
    return np.array(float(X[0][0]))



print(get_position_update(x_observations, v_observations))