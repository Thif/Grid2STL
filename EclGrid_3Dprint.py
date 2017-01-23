######################################################################
# Thibaut Forest,Statoil                                             #
# 03/06/2016                                                         #
# The purpose of this script is to export STL file for 3D printing   #
# from the eclipse EGRID file.                                       #
######################################################################


import numpy as np
import ert.ecl as ecl #Make sure Ert library is installed
import sys
import os
from collections import Counter
import gc

# This function generates a square in STL (based on two triangles)


def GenerateSquare(x,file):
	l=[[0,1,2],[1,3,2]]
		
	for v in l:

		a=x[:,v[0]]
		b=x[:,v[1]]
		c=x[:,v[2]]

		MakeFacet(a,b,c,file)
		

# This function writes the coordinates of the triangle in the file

def MakeFacet(a,b,c,file):
	file.write("facet normal 0 0 0\nouter loop\nvertex "+str(a[0])+" "+str(a[1])+" "+str(a[2])+"\nvertex "+str(b[0])+" "+str(b[1])+" "+str(b[2])+"\nvertex "+str(c[0])+" "+str(c[1])+" "+str(c[2])+"\nendloop\nendfacet\n\n") 

# This function reads the EGRID file, gets the xyz coordinates of the corners of the cells and creates arrays containing them

def GetCornersXYZ():
	    z_value_top=int(sys.argv[2])
	    z_value_bottom=int(sys.argv[3])
	    z_scale=int(sys.argv[4])
	    
	    grid = ecl.EclGrid( Eclipsename+".EGRID" )
	    #init_file = ecl.EclFile(Eclipsename+".INIT")
	    #fipnum = init_file.iget_named_kw("FIPNUM",0)
		
	    region_slice = ecl.EclRegion(grid, False); region_slice.select_kslice(z_value_top, z_value_bottom)
	    #region_fipnum1=ecl.EclRegion(grid, False); region_fipnum1.select_equal(fipnum, 1)
	    #region_fipnum2=ecl.EclRegion(grid, False); region_fipnum2.select_equal(fipnum, 2)
	    #region_fipnum3=ecl.EclRegion(grid, False); region_fipnum3.select_equal(fipnum, 3)
	    #region_fipnum4=ecl.EclRegion(grid, False); region_fipnum4.select_equal(fipnum, 4)
	    #region_intersect  = region_slice & (region_fipnum1  | region_fipnum2 | region_fipnum3 | region_fipnum4)
	    Surface=[]
    
    	    print "Exporting coordinates..."
	    for i,ia in enumerate(region_slice.active_list):
	    	gc.disable()
	        sys.stdout.write("\r"+str(i*100/len(region_slice.active_list))+"%")
		(x0,y0,z0) = grid.get_corner_xyz(0 , active_index = ia)
		(x1,y1,z1) = grid.get_corner_xyz(1 , active_index = ia)
		(x2,y2,z2) = grid.get_corner_xyz(2 , active_index = ia)
		(x3,y3,z3) = grid.get_corner_xyz(3 , active_index = ia)
		(x4,y4,z4) = grid.get_corner_xyz(4 , active_index = ia)
		(x5,y5,z5) = grid.get_corner_xyz(5 , active_index = ia)
		(x6,y6,z6) = grid.get_corner_xyz(6 , active_index = ia)
		(x7,y7,z7) = grid.get_corner_xyz(7 , active_index = ia)
		
		Surface.append(str(x0)+","+str(y0)+","+str(z0)+","+str(x1)+","+str(y1)+","+str(z1)+","+str(x2)+","+str(y2)+","+str(z2)+","+str(x3)+","+str(y3)+","+str(z3))
		Surface.append(str(x4)+","+str(y4)+","+str(z4)+","+str(x5)+","+str(y5)+","+str(z5)+","+str(x6)+","+str(y6)+","+str(z6)+","+str(x7)+","+str(y7)+","+str(z7))
		Surface.append(str(x0)+","+str(y0)+","+str(z0)+","+str(x1)+","+str(y1)+","+str(z1)+","+str(x4)+","+str(y4)+","+str(z4)+","+str(x5)+","+str(y5)+","+str(z5))
		Surface.append(str(x5)+","+str(y5)+","+str(z5)+","+str(x1)+","+str(y1)+","+str(z1)+","+str(x7)+","+str(y7)+","+str(z7)+","+str(x3)+","+str(y3)+","+str(z3))
		Surface.append(str(x2)+","+str(y2)+","+str(z2)+","+str(x3)+","+str(y3)+","+str(z3)+","+str(x6)+","+str(y6)+","+str(z6)+","+str(x7)+","+str(y7)+","+str(z7))			
		Surface.append(str(x4)+","+str(y4)+","+str(z4)+","+str(x0)+","+str(y0)+","+str(z0)+","+str(x6)+","+str(y6)+","+str(z6)+","+str(x2)+","+str(y2)+","+str(z2))
	 
	    
	    c = Counter(Surface)
	    Surface=[k for k,v in c.items() if v == 1 ]

	    print "\n\nCreating STL..."
	    for i,u in enumerate(Surface):
	    	sys.stdout.write("\r"+str(i*100/len(Surface))+"%")
	    	split = map(float, u.split(","))
	    	x=np.array([[split[0],split[3],split[6],split[9]],[split[1],split[4],split[7],split[10]],[split[2]*z_scale,split[5]*z_scale,split[8]*z_scale,split[11]*z_scale]])
		x=np.divide(x,100)
		GenerateSquare(x,file)

	
# Open new file for export

file = open(os.path.splitext(sys.argv[1])[0]+".STL", "w")
file.write("solid EclGrid\n")

# write STL file with coordinates
Eclipsename=str.split(sys.argv[1],".")[0]
GetCornersXYZ()

file.write("endsolid EclGrid\n")

print "\n\nScript finished"
