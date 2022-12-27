# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:33:08 2022

@author: gunes
"""
import csv
import numpy as np
import flowpsi as flow_solver
#nfunction takes x vector, Def and structural parameters and gives out results
#vector for residual calculation.
def nfunction(x,Def,parameters,Less_Iteration):
  #Take parameters.
  m = parameters[0];    I = parameters[1]
  Kh = parameters[2];   Ka = parameters[3]
  b = parameters[4];    xa = parameters[5]
  a = parameters[6]
  Sa = m*b*xa
  Mcenter = (1+a)*b
  #Take variables.
  N = x.shape[0] - 1
  w = x[N-1]
  V = x[N]
  damping = 0
  #Define residual vector as result.
  result = np.zeros((N+1, 1))
  #Define DOF vectors.
  Alphar = Def 
  Alphai = 0
  hr = x[0]
  hi = x[1]
  hamp=np.sqrt(x[0]*x[0]+x[1]*x[1])
  hang=np.arctan2(x[1],x[0])
  # hr = x[0]
  # hi = x[1]
  #Take lift and moment information from solver code.
  Lr,Li,Mr,Mi = flow_solver.LandM(V, w, hamp, hang, Alphar, Alphai, Mcenter,Less_Iteration)
  #Residual equations.(Ax-B = R)
  # result[0,] = ((damping*damping-w*w)*m+Kh)*hr-(2*damping*w)*m*hi+(damping*damping-w*w)*Sa*ar-Sa*(2*damping*w)*ai+Lr
  # result[1,] = ((damping*damping-w*w)*m+Kh)*hi+(2*damping*w)*m*hr+(damping*damping-w*w)*Sa*ai+Sa*(2*damping*w)*ar+Li
  # result[2,] = (((damping*damping-w*w)*I+Ka)*ar-(2*damping*w)*I*ai+(damping*damping-w*w)*Sa*hr-Sa*(2*damping*w)*hi-Mr)*10
  # result[3,] = (((damping*damping-w*w)*I+Ka)*ai+(2*damping*w)*I*ar+(damping*damping-w*w)*Sa*hi+Sa*(2*damping*w)*hr-Mi)*100
  result[0,] = (((damping*damping-w*w)*m+Kh)*hr-(2*damping*w)*m*hi+(damping*damping-w*w)*Sa*Alphar-Sa*(2*damping*w)*Alphai+Lr)/Lr
  result[1,] = (((damping*damping-w*w)*m+Kh)*hi+(2*damping*w)*m*hr+(damping*damping-w*w)*Sa*Alphai+Sa*(2*damping*w)*Alphar+Li)/Li
  result[2,] = (((damping*damping-w*w)*I+Ka)*Alphar-(2*damping*w)*I*Alphai+(damping*damping-w*w)*Sa*hr-Sa*(2*damping*w)*hi-Mr)/Mr
  result[3,] = (((damping*damping-w*w)*I+Ka)*Alphai+(2*damping*w)*I*Alphar+(damping*damping-w*w)*Sa*hi+Sa*(2*damping*w)*hr-Mi)/Mi
  return result
#Newton Numeric takes x vector, error criteria iteration criteria and assumed
#deflection amplitude and structural parameters and gives roots of the
#nonlinear equation defined in nfunction using numerical derivative newton
#rhapson method.
def NewtonNumeric(xi,errcriteria,itcriteria,Def,parameters):
  N = xi.shape[0]
  x = xi
  i = 0
  maxerr = 1000
  #Define residuals without perturbation for numerical derivative using
  #forward difference.
  R = nfunction(x,Def,parameters,0)
  #Perturbation size.
  h = 1e-8
  #Relaxation.
  lamda = 1
  J = np.zeros((N,N))
  xcalc = np.zeros((N,itcriteria))
  while (itcriteria>i) and (maxerr>errcriteria):
    #Jacobian calculation for loop.
    for j in range(N):
      xh = x.copy()
      xh[j] = x[j]+h
      Rif = nfunction(xh,Def,parameters,1)
      J[0:N,j] = ((Rif-R)/h).reshape((4,))
    #variable calculation for next iteration.
    xcalc[0:N,i] = (x-np.matmul(np.linalg.inv(J),R)).reshape((4,))
    #Relaxation.
    x = (xcalc[:,i]*lamda+(1-lamda)*x[:,0]).reshape((4,1))
    #Define residuals without perturbation for numerical derivative using
    #forward difference.
    R = nfunction(x,Def,parameters,0)
    #Error.
    abserr = np.absolute(R)
    maxerr = np.amax(abserr)
    i = i+1
    print("_____________________________________________________________________")
    print(f"Iteration Number:{i}\n|h_amplitude:{x[0][0]}||h_phase:{x[1][0]/np.pi*180}|\
          |Frequency:{x[2][0]/2/np.pi}||Velocity:{x[3][0]}|\nError:{maxerr}\n")
    print("_____________________________________________________________________")
    # Open a file for writing
    with open('output.csv', 'a', newline='') as csvfile:
    # Create a CSV writer object
      writer = csv.writer(csvfile)

      # Write the header row
      writer.writerow(['Iteration Number', 'h_amplitude', 'h_phase','Frequency','Velocity','Error1','Error2','Error3','Error4'])

      # Write the data rows
      writer.writerow([i,x[0][0],x[1][0]/np.pi*180,x[2][0]/2/np.pi,x[3][0],abserr[0],abserr[1],abserr[2],abserr[3]])
  roots = x
  iterationnumber = i
  return roots,maxerr,iterationnumber