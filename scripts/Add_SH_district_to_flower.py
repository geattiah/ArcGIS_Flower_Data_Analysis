'''Basic arcpy script to add district information to flower data
AUTHOR: Gifty E. A. Attiah
DATE_CREATED: 23/03/2020'''

#Import arcpy
import arcpy
from arcpy import env

# get the map document
mxd = arcpy.mapping.MapDocument("CURRENT")

# get the data frame
df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

#Path to flower data shapefiles
flower = r'C:\Users\Gift\Desktop\git\arcgis\arcgis_flower_analysis\output_shapefiles\Flower.shp'

#Path to schleswig holstein district shapefile
sh_districts = r'C:\Users\Gift\Desktop\git\arcgis\arcgis_flower_analysis\output_shapefiles\SH_district.shp'

#Path to Flower data with schleswig holstein district
flower_dataset = r'C:\Users\Gift\Desktop\git\arcgis\arcgis_flower_analysis\output_shapefiles\Flower_Dataset.shp'

#create a new layers
flower_data = arcpy.mapping.Layer(flower)
sh_district = arcpy.mapping.Layer(sh_districts)

# add the layer to the map at the bottom of the TOC in data frame 0
arcpy.mapping.AddLayer(df, flower_data,"BOTTOM")
arcpy.mapping.AddLayer(df, sh_district,"BOTTOM")

# join shapefile districts to flower data
arcpy.SpatialJoin_analysis(flower, sh_districts,flower_dataset)

#Fxn to add fields to the data
def add_field(str):
    arcpy.AddField_management(flower_dataset,str,"TEXT")

#Calling add field function
add_field("Districts")
add_field("States")

#setting code for field calculator to tranform empty Districts fields with "outside"
expression = "district(!District!)"
codeblock = """def district(x):
   if x == " ":
      r = 'Outside'
   else:
      r = x 
   return r"""

#Calculate districts field
arcpy.CalculateField_management(flower_dataset, "Districts", expression, "PYTHON", codeblock)  

#setting code for field calculator to tranform empty State fields with "None"
expression = "state(!State!)"
codeblock = """def state(x):
   if x == " ":
      r = 'None'
   else:
      r = x 
   return r"""

#Calculate states field
arcpy.CalculateField_management(flower_dataset, "States", expression, "PYTHON", codeblock)  

#Fxn to delete fields 
def del_field(str):
    arcpy.DeleteField_management(flower_dataset,str)
    
#Calling delete field function    
del_field("Join_count")
del_field("TARGET_FID")
del_field("District")
del_field("State")

#END
