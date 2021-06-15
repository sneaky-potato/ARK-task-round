import csv
import KalmanEqn
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import statistics

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
class Tower():
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []
        location = [0,0,0]
    def get_relative(self, other):
        common_len = len(self.x) if len(self.x) < len(other.x) else len(other.x)
        sum_x = sum_y = sum_z = 0
        for i in range(common_len):
            sum_x += other.x[i] - self.x[i]
            sum_y += other.y[i] - self.y[i]
            sum_z += other.z[i] - self.z[i]
        return [sum_x/common_len, sum_y/common_len, sum_z/common_len]

firstTower = Tower()
secondTower = Tower()

choice = 0
while(choice < 1 or choice > 3):
    choice = int(input("Enter 1 for Data1, 2 for Data2, 3 for Data3:\n"))
    if(choice == 1): file = 'Data1'
    elif(choice == 2): file = 'Data2'
    elif(choice == 3): file = 'Data3' 

f = open('./Output/'+ file + '_localization.txt', 'w')

# open file in read mode
with open('./Data files/'+file+'.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        firstTower.x.append(float(row[0]))
        firstTower.y.append(float(row[1]))
        firstTower.z.append(float(row[2]))

        secondTower.x.append(float(row[3]))
        secondTower.y.append(float(row[4]))
        secondTower.z.append(float(row[5]))
    
print('Number of data points read =',len(firstTower.x))
secondTower.location = firstTower.get_relative(secondTower)
f.write(str(secondTower.location))

del_x = statistics.variance(firstTower.x)
del_y = statistics.variance(firstTower.y)
del_z = statistics.variance(firstTower.z)

"""
R = measurement noise covariance
Q = estiamtion model noise covariance
"""

A = np.identity(3)
C = A
temp = np.matrix([firstTower.x, firstTower.y, firstTower.z])
R = np.cov(temp)
temp = np.matrix([secondTower.x, secondTower.y, secondTower.z])
Q = np.cov(temp)

P_post = A

kalman_x = []
kalman_y = []
kalman_z = []

predicted_x = []
predicted_y = []
predicted_z = []

for i in range(10000):
    measurement = np.matrix([[(firstTower.x[i])],[(firstTower.y[i])],[(firstTower.z[i])]])
    r_prior = np.matrix([[secondTower.x[i] - secondTower.location[0]], [secondTower.y[i] - secondTower.location[1]], [secondTower.z[i] - secondTower.location[2]]])
    predicted_x.append(r_prior[0,0])
    predicted_y.append(r_prior[1,0])
    predicted_z.append(r_prior[2,0])

    P_prior = KalmanEqn.prior_covariance(A, P_post, Q)
    K = KalmanEqn.kalman_gain(P_prior, C, R)
    r_post = KalmanEqn.post_estimate(r_prior, K, measurement, C)
    P_post = KalmanEqn.post_covariance(K, C, P_prior, 3)

    kalman_x.append(r_post[0,0])
    kalman_y.append(r_post[1,0])
    kalman_z.append(r_post[2,0])

ax.plot(firstTower.x, firstTower.y, firstTower.z, 'green')
ax.plot(predicted_x, predicted_y, predicted_z, 'gray')
ax.plot(kalman_x, kalman_y, kalman_z, 'blue')
ax.autoscale()

plt.savefig('./Output/'+file+'_1-2.png')
plt.show()
print("Location of Tower 2: ", secondTower.location)


for k in range(4):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    anotherkalman_x = []
    anotherkalman_y = []
    anotherkalman_z = []
    tempTower = Tower()

    predicted_x = []
    predicted_y = []
    predicted_z = []

    with open('./Data files/'+file+'.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            tempTower.x.append(float(row[6 + k*3]))
            tempTower.y.append(float(row[7 + k*3]))
            tempTower.z.append(float(row[8 + k*3]))
    tempTower.location = firstTower.get_relative(tempTower)
    print("Location of Tower {}: ".format(k + 3), tempTower.location)
    f.write(str(tempTower.location))
    R = P_post
    for i in range(10000):
        measurement = np.matrix([[(kalman_x[i])],[(kalman_y[i])],[(kalman_z[i])]])
        r_prior = np.matrix([[tempTower.x[i] - tempTower.location[0]], [tempTower.y[i] - tempTower.location[1]], [tempTower.z[i] - tempTower.location[2]]])
        predicted_x.append(r_prior[0,0])
        predicted_y.append(r_prior[1,0])
        predicted_z.append(r_prior[2,0])

        P_prior = KalmanEqn.prior_covariance(A, P_post, Q)
        K = KalmanEqn.kalman_gain(P_prior, C, R)
        r_post = KalmanEqn.post_estimate(r_prior, K, measurement, C)
        P_post = KalmanEqn.post_covariance(K, C, P_prior, 3)

        anotherkalman_x.append(r_post[0,0])
        anotherkalman_y.append(r_post[1,0])
        anotherkalman_z.append(r_post[2,0])

    ax.plot(kalman_x, kalman_y, kalman_z, 'green')
    #ax.plot(predicted_x, predicted_y, predicted_z, 'gray')
    ax.plot(anotherkalman_x, anotherkalman_y, anotherkalman_z, 'blue')
    plt.savefig('./Output/'+file+'_1-' + str(k + 3)+ '.png')
    plt.show()

    kalman_x = anotherkalman_x
    kalman_y = anotherkalman_y
    kalman_z = anotherkalman_z

print("Final uncertainty in estimated location:\n", P_post)
f.close()