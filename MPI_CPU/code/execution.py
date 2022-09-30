# Importing necessary modules

import numpy as np
import os

#define a set of parameters (number of node, task per node)
ProcNumbers = [[1,1],[1,2],[1,4],[2,4],[4,4],[8,4]]

#Clear previous data in Result file
Result = open ("/export/home/grp08/monte_carlo/Result.dat", "w")
Result.close()
   
for nb in ProcNumbers:
    num = nb[0]*nb[1]
    # Copy template input file into txt object
    Job = "Performance_monte_carlo.job"
    inp = open( Job, "r" )
    txt = inp.read()
    inp.close()

    # Copy proc number
    NodeNumber = "%d" % nb[0]
    TaskNumber = "%d" % nb[1]

    # Replace reserved number of nodes with chosen values
    newTxt = txt.replace( "NODESNUMBER", NodeNumber )

    # Replace reserved reserved number of tasks with chosen values
    newTxt2 = newTxt.replace( "TASKSNUMBER", TaskNumber )


    # Create jobname for submission and write info to screen
    Filename = "Job-%02d.job" % num
    print ("Filename:", Filename)

    # Write input file for job submission
    out = open(Filename, "w")
    out.write(newTxt2)
    out.close()

    # Submit to Slurm

    command = 'sbatch Job-%02d.job' % num

    os.system(command)
