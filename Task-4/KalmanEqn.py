import numpy as np

def prior_estimate(A, B, x_k_1, u_k):
    return np.dot(A,x_k_1) + np.dot(B, u_k)

def prior_covariance(A, P_k_1, Q):
    return np.dot(A,np.dot(P_k_1, np.matrix(A).T)) + Q

def kalman_gain(P_k, C, R):
    return np.dot(np.dot(P_k, np.matrix(C).T), np.linalg.inv(np.dot(np.dot(C, P_k), np.matrix(C).T) + R))

def post_estimate(x_k, K, y_k, C):
    return x_k + np.dot(K, y_k - np.dot(C, x_k))

def post_covariance(K, C, P_k, n):
    return np.dot(np.identity(n) - np.dot(K, C), P_k)