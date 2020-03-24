'''Basic arcpy script to prepare shapefile for further analysis
AUTHOR: Gifty E. A. Attiah
DATE_CREATED: 23/03/2020'''

#Import arcpy
import arcpy
from arcpy import env

# get the map document
mxd = arcpy.mapping.MapDocument("CURRENT")

# get the data frame
df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

#Path to shapefile
shapefile = r'C:\Users\Gift\Desktop\git\arcgis\arcgis_flower_analysis\output_shapefiles\Flower.shp'

#create a new layer
newlayer = arcpy.mapping.Layer(shapefile)

# add the layer to the map at the bottom of the TOC in data frame 0
arcpy.mapping.AddLayer(df, newlayer,"BOTTOM")

#Fxn to add fields to the data
def add_field(str):
    arcpy.AddField_management(newlayer,str,"TEXT")

#Calling add field function
add_field("Date")
add_field("Code")
add_field("Flo_color")
add_field("Flo_count")
add_field("Flo_shape")
add_field("Matured")

#Fxn to calculate fields 
def calc_field(field,exp):
    arcpy.CalculateField_management(newlayer,field,exp,"PYTHON")   

#Calling calculate field function    
calc_field("Date",'!Year! + "/" + !Month! +"/" + !Day!')
calc_field("Flo_color",'!Flower!')
calc_field("Flo_count",'!F_count!')
calc_field("Flo_shape",'!F_shape!')
calc_field("Code",'!Flower![0:2].upper()+!Flower![-1:].upper()')
calc_field("Matured",'!Developed!')

#Fxn to delete fields 
def del_field(str):
    arcpy.DeleteField_management(newlayer,str)

#Calling delete field function    
del_field("Flower")
del_field("F_count")
del_field("F_shape")
del_field("Key")
del_field("Developed")

#END
