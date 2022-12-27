# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:39:22 2022

@author: gunes
"""
import numpy as np
from scipy.special import jv, yv
def H0(k):
  return jv(0, k) - 1j * yv(0, k)

def H1(k):
  return jv(1, k) - 1j * yv(1, k)
def LandM(U,w,hamp,hang,ar,ai):
    hr=hamp*np.cos(hang);
    hi=hamp*np.sin(hang);
    h=hr+1j*hi
    alpha=ar+1j*ai
    b=0.15;
    p_inf=1.1341;
    a=-0.5;
    k=w*b/U;
    C=H1(k)/(H1(k)+1j*H0(k));
    L=2*np.pi*p_inf*U*b*C*(h*w*1j+U*alpha+b*(1/2-a)*w*1j*alpha)+np.pi*p_inf*b*b*(-w*w*h+U*1j*w*alpha+b*a*alpha*w*w);
    Lr=L.real;
    Li=L.imag;
    Mx=-np.pi*p_inf*b*b*b*(-1/2*w*w*h+U*alpha*1j*w-b*(1/8-a/2)*alpha*w*w);
    M=Mx+b*(1/2+a)*L;
    Mr=M.real;
    Mi=M.imag;
    return(Lr,Li,Mr,Mi)

    


