import cvxpy as cvx
import sys
import numpy as np
import matplotlib.pyplot as plt


def main():
    # x[0] == x(k)
    x0, y0 = (2, 3)
    ux0, uy0 = (3, 4)
    (x_target, y_target) = (22, 25)
    steps = 50
    delta_t = 0.1
    x_limits, y_limits = (1, 30), (1, 30)
    ux_limits, uy_limits = (1, 10), (1, 10)

    x = cvx.Variable(steps)
    ux = cvx.Variable(steps - 1)
    constraint_x = [x[0] == x0, ux[0] == ux0]
    constraint_x += [x[index + 1] == x[index] + delta_t * ux[index]
                     for index in xrange(0, steps - 1)]
    constraint_x += [x >= x_limits[0], x <= x_limits[1],
                     ux >= ux_limits[0], ux <= ux_limits[1]]
    objective_xpath = cvx.Minimize(cvx.square(x_target - x[steps - 1]))
    delta_xvelocity = np.sum([(ux[index] - ux[index + 1])**2
                              for index in xrange(0, steps - 2)])
    objective_xvelocity = cvx.Minimize((delta_xvelocity))
    objective_x = objective_xpath + objective_xvelocity

    y = cvx.Variable(steps)
    uy = cvx.Variable(steps - 1)
    constraint_y = [y[0] == y0, uy[0] == uy0]
    constraint_y += [y[index + 1] == y[index] + delta_t * uy[index]
                     for index in xrange(0, steps - 1)]
    constraint_y += [y >= y_limits[0], y <= y_limits[1],
                     uy >= uy_limits[0], uy <= uy_limits[1]]
    objective_ypath = cvx.Minimize(cvx.square(y_target - y[steps - 1]))
    delta_yvelocity = np.sum([(uy[index] - uy[index + 1])**2
                              for index in xrange(0, steps - 2)])
    objective_yvelocity = cvx.Minimize((delta_yvelocity))
    objective_y = objective_ypath + objective_yvelocity

    constraints = constraint_x + constraint_y
    objective = objective_x + objective_y
    prob = cvx.Problem(objective, constraints)
    print 'DCP followed:', prob.is_dcp()
    prob.solve()
    print prob.status

    print 'cost function: ', np.round(prob.value, 5)
    print 'x coordinates: ', np.round(x.value, 3)
    print 'y coordinates:', np.round(y.value, 3)
    # print 'ux velocity: ', np.round(ux.value, 3)
    # print 'uy velocity: ', np.round(uy.value, 3)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(x.value, y.value, 'ro', x0, y0, 'go', x_target, y_target, 'go')
    plt.xlabel('x coordinate')
    plt.ylabel('y coordinate')

    plt.subplot(212)
    velocity = np.array([np.sqrt(vx**2 + vy**2)
                         for vx, vy in zip(ux.value, uy.value)])
    time = np.linspace(0.1, 5, 49)
    print 'velocity:', velocity
    plt.plot(time, velocity, 'bo', time[0], np.sqrt(ux0**2 + uy0**2), 'go')
    plt.xlabel('Time')
    plt.ylabel('Velocity')
    plt.show()


if __name__ == '__main__':
    main()
