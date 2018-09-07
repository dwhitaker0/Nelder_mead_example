import numpy as np
import pandas as pd
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


############USER INPUT###############

initial_x = float(raw_input("Initial V1: "))
initial_y = float(raw_input("Initial V2: "))
initial_step_x = float(raw_input("Initial x step: "))
initial_step_y = float(raw_input("Initial y step: "))
max_iterations = 10
n = 2 #Number of variables
col_names = ['V1', 'V2', 'Obj']
no_improv_break = 3

a = 1	#NM algorithm factor
b = 2	#NM algorithm factor
g = 0.5		#NM algorithm factor
k = 1.5 #NM algorithm factor
d = 0.5			#NM algorithm factor

###################################

#######INITIALISE#####################
iterations =  0
no_improv_thresh = 1

Results	 = pd.DataFrame()
#To initialise simplex a starting co-ordinate is required (Xin), n+1 points are generated with step_size (initial_step_x & y) away from Xin

Xin = np.array((initial_x,initial_y))
Xin1 = Xin + np.array((initial_step_x,0))
Xin2 = Xin + np.array((0,initial_step_y))

#####################################

###########SET UP GRAPHING##############
#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.setWindowTitle('pyqtgraph example: PlotWidget')
mw.resize(1000,1000)
cw = QtGui.QWidget()
mw.setCentralWidget(cw)
l = QtGui.QHBoxLayout()
cw.setLayout(l)

pw = pg.PlotWidget()
l.addWidget(pw)

mw.show()

## Create an empty plot curve to be filled later, set its pen
p1 = pw.plot()
p1.setSymbol('o')
p1.setPen(None)



pw.setLabel('left', 'V1', units='arb')
pw.setLabel('bottom', 'V2', units='arb')
pw.setXRange(0, 200)
pw.setYRange(0, 200)
############################################


##############
#EVALUATE RESONSE AT Xin, Xin1, Xin2
##############



Res_Xin = float(raw_input("Obj_Res_Initial_0: "))
Res_Xin1 =float(raw_input("Obj_Res_Initial_1: "))
Res_Xin2= float(raw_input("Obj_Res_Initial_2: "))

Results = pd.DataFrame([(initial_x,initial_y,Res_Xin)], columns=col_names)
Results = Results.append(pd.DataFrame([(Xin1[0], Xin1[1], Res_Xin1)], columns=col_names), ignore_index=True)
Results = Results.append(pd.DataFrame([(Xin2[0], Xin2[1], Res_Xin2)], columns=col_names), ignore_index=True)
print(Results)
p1.setData(y=np.array(Results.iloc[:,0]), x=np.array(Results.iloc[:,1]))

##############
no_improv = 0

###########OPTIMISATION ALGORITHM###############

while iterations < max_iterations:

	sorted = Results.sort_values(by='Obj', ascending = False)
	Obj_h = sorted.iloc[n,n]
	Obj_s = sorted.iloc[n-1,n]
	Obj_l = sorted.iloc[n-2,n]

	if Obj_l - Obj_s >= no_improv_thresh:
		no_improv = 0
	else:
		no_improv = no_improv + 1

	if no_improv == no_improv_break:
		print 'No Further Improvement, exiting......'
		#close_connections gracefully
		print (Results)
		break


	h = sorted.iloc[n,:n]
	s = sorted.iloc[n-1,:n]
	l = sorted.iloc[n-2,:n]

	best_vertex = [(s.iloc[0],l.iloc[0]),(s.iloc[1],l.iloc[1])]
	centroid = (sum(best_vertex[0])/len(best_vertex[0]),sum(best_vertex[1])/len(best_vertex[1]))



####Reflection####

	Xr = centroid + (centroid - h)
	print "Next Point = "+ "\n" + str(Xr)

	Res_Xr = float(raw_input("Xr_Obj_Res: ")) ##User Inserts Result##

	Results = Results.append(pd.DataFrame([(Xr.iloc[0], Xr.iloc[1], Res_Xr)], columns=col_names), ignore_index=True)
	print(Results)
	p1.setData(y=np.array(Results.iloc[:,0]), x=np.array(Results.iloc[:,1]))




####NO MOVE####

	if Res_Xr < Obj_l and Res_Xr >= Obj_s:
		iterations = iterations +1
		print "No Move"
		continue



####Expand####

	if Res_Xr > Obj_l:
		Xe = centroid + b*(centroid - h)
		print "Next Point = " + "\n" + str(Xe)
		Res_Xe = float(raw_input("Xe_Obj_Res: "))

#Final condition#

		if Res_Xe >= Obj_l:
			Results = Results.append(pd.DataFrame([(Xe.iloc[0], Xe.iloc[1], Res_Xe)], columns=col_names), ignore_index=True)
			print(Results)
			p1.setData(y=np.array(Results.iloc[:,0]), x=np.array(Results.iloc[:,1]))

			iterations = iterations + 1
			continue

		else: #doing nothing will just keep R as the new point
			Results = Results.append(pd.DataFrame([(Xe.iloc[0], Xe.iloc[1], Res_Xe)], columns=col_names), ignore_index=True)
			iterations = iterations + 1
			continue



####Inside Contraction####

	if Res_Xr <= Obj_h:

		#Xic = g*centroid + g*h
		Xic = centroid - g*(Xr - centroid)
		print "Next Point = " + "\n" + str(Xic)

		Res_Xic = float(raw_input("Xic_Obj_Res: "))

	#Final Condition#

		if Res_Xic >= Obj_h:

			Results = Results.append(pd.DataFrame([(Xic.iloc[0], Xic.iloc[1], Res_Xic)], columns=col_names), ignore_index=True)
			print(Results)
			p1.setData(y=np.array(Results.iloc[:,0]), x=np.array(Results.iloc[:,1]))

			iterations = iterations + 1
			continue

		else: ##Shrink##

			Xredh = l + d*(h - l)
			print "Next Set Points = " + "\n" + str(Xredh)


			Res_Xredh = float(raw_input("Xredh_Obj_Res: "))

			Results = Results.append(pd.DataFrame([(Xic.iloc[0], Xic.iloc[1], Res_Xic)], columns=col_names), ignore_index=True)
			Results = Results.append(pd.DataFrame([(Xredh.iloc[0], Xredh.iloc[1], Res_Xredh)], columns=col_names), ignore_index=True)
			print(Results)
			p1.setData(y=np.array(Results.iloc[:,0]), x=np.array(Results.iloc[:,1]))


			Xreds = l + d*(s - l)
			print "Next Set Points = " + "\n" + str(Xreds)


			Res_Xreds = float(raw_input("Xreds_Obj_Res: "))


			Results = Results.append(pd.DataFrame([(Xreds.iloc[0], Xreds.iloc[1], Res_Xreds)], columns=col_names), ignore_index=True)
			print(Results)
			p1.setData(y=np.array(Results.iloc[:,0]), x=np.array(Results.iloc[:,1]))


			iterations = iterations + 1
			continue



####Outside Contraction####

	if Res_Xr > Obj_h and Res_Xr <= Obj_s:

		#Xoc = k*centroid - g*h
		Xoc = centroid + g*(Xr - centroid)
		print "Next Point = " + "\n" + str(Xoc)

		Res_Xoc = float(raw_input("Xoc_Obj_Res: "))



#Final Condition#

		if Res_Xoc > Res_Xr:

			Results = Results.append(pd.DataFrame([(Xoc.iloc[0], Xoc.iloc[1], Res_Xoc)], columns=col_names), ignore_index=True)
			print(Results)
			p1.setData(y=np.array(Results.iloc[:,0]), x=np.array(Results.iloc[:,1]))

			iterations = iterations + 1
			continue

		else: ##Shrink##

			Xredh = l + d*(h - l)
			print "Next Set Points = "  + "\n" + str(Xredh)


			Res_Xredh = float(raw_input("Xredh_Obj_Res: "))

			Results = Results.append(pd.DataFrame([(Xoc.iloc[0], Xoc.iloc[1], Res_Xoc)], columns=col_names), ignore_index=True)
			Results = Results.append(pd.DataFrame([(Xredh.iloc[0], Xredh.iloc[1], Res_Xredh)], columns=col_names), ignore_index=True)
			print(Results)
			p1.setData(y=np.array(Results.iloc[:,0]), x=np.array(Results.iloc[:,1]))


			Xreds = l + d*(s - l)
			print "Next Set Points = "+ "\n" + str(Xreds)


			Res_Xreds = float(raw_input("Xreds_Obj_Res: "))


			Results = Results.append(pd.DataFrame([(Xreds.iloc[0], Xreds.iloc[1], Res_Xreds)], columns=col_names), ignore_index=True)
			print(Results)
			p1.setData(y=np.array(Results.iloc[:,0]), x=np.array(Results.iloc[:,1]))


			iterations = iterations + 1
			continue
