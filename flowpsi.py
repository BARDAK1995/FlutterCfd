# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 11:34:38 2022

@author: gunes
"""
import subprocess
import concurrent.futures
import numpy as np
import text_rw as TRW
from math import pi

def run_subprocess(cmd):
    return subprocess.run(cmd, shell=True, check=False)

def LandM(V, w, hamp, hphase, Alphar, Alphai, Mcenter, Less_Iteration):
    rho = 1.1766
    T = 300
    #sabun
    #alpha = ar + 1j*ai
    aamp = Alphar/pi*180                        #radyandi degree cevirdim BC icine yazan yer
    aphase = Alphai
    case_name  =  "NACA012"
    old_harmonic_iter = 200
    if Less_Iteration == 1:
        steady_iter = 1
        harmonic_iter = 200
    else:
        steady_iter = 1000
        harmonic_iter = 200
    TRW.text_write(case_name+".vars", "harmonicRedFreq", f"    harmonicRedFreq: {w[0]/2/np.pi}", case_name + ".vars")
    TRW.text_write(case_name+".vars", "stop_iter", f"    stop_iter: {steady_iter}", case_name + ".vars")
    TRW.text_write(case_name+".vars", "harmonicStop", f"    harmonicStop: {harmonic_iter}", case_name + ".vars")
    #Define the new line to be added.
    BC1_new_line = f'        BC_1 = reflecting(\n\
                X_flut_plunging_AMP=[0,{hamp[0]},0],  phase_plunging={hphase[0]*180/pi+180},\n\
                pitch_center_Z=[{Mcenter},0,005],  phase_pitch_Z={aphase},   \
Theta_flut_pitch_Z={aamp},\n                       momentCenter=[{Mcenter},0,0], Z_thickness = 0.003\n\
            )'
    BC3_new_line = f'        BC_3 = inflow(u=[{V} m/s,0 ,0],rho={rho},T={T}),'
    #def text_write(text_name,to_be_searched,new_line,wfile_name) one can also
    #include folders in wfile_name to write them in folders. The searched text
    #should appear only once in the input file.
    TRW.text_write2(case_name + ".vars", "BC_1", BC1_new_line,case_name + ".vars")
    TRW.text_write(case_name + ".vars", "BC_3", BC3_new_line,case_name + ".vars")
    #Types the command in terminal and pyhton waits for the execution.
    if Less_Iteration == 1:
        cmd = f"mpirun -np 20 flowpsi NACA012 harmonic_{old_harmonic_iter}"
    else:
        cmd = f"mpirun -np 20 flowpsi NACA012"

    max_workers = 1
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Launch subprocesses in parallel, up to max_workers at a time
        results = executor.submit(run_subprocess, cmd)
    # subprocess.run(cmd)
    Lamp,Lphase,Mamp,Mphase = TRW.readcsv("Moment_Lift_reflecting_BC.csv")
    Lr = Lamp*np.cos(Lphase/180*pi); Li = Lamp*np.sin(Lphase/180*pi)
    Mr = -Mamp*np.cos(Mphase/180*pi); Mi = -Mamp*np.sin(Mphase/180*pi)
    return(Lr,Li,Mr,Mi)
