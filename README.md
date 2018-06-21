# Model-Predictive-Control
Single cycle MPC for path following by a point. Input Parametes:    
Starting point = (2,3)  
End point = (22,25)  
steps = 50  
delta_t = 0.1 seconds. Total = 50 * 0.1 = 5 seconds.  
Starting velocity = (3,4)  
Position limits(m): 1<x<30 and 1<y<30  
Velocity limits(m/s): 1<ux<10 and 1<uy<10

Objective function:  
Minimize((x_target - x[final])^2 + (y_target - y[final]^2) + sum_square(vel[t] - vel[t+1]))    
![alt text](https://raw.githubusercontent.com/UditSinghParihar/Model-Predictive-Control/master/path_and_velocity_profile.png)

