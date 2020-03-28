'''Basic arcpy script to prepare schleswig holstein and German
shapefiles(data) to be added Flower data 
AUTHOR: Gifty E. A. Attiah
DATE_CREATED: 28/03/2020'''

#Import arcpy
import arcpy
from arcpy import env

# get the map document
mxd = arcpy.mapping.MapDocument("CURRENT")

# get the data frame
df = arcpy.mapping.ListDataFrames(mxd,"*")[0]

# shapefile containing the german states
german_states =r'C:\Users\Gift\Desktop\git\arcgis\arcgis_flower_analysis\shapefile_data\Germany_states.shp'

# shapefile containing the german states and their districts
german_districts = r'C:\Users\Gift\Desktop\git\arcgis\arcgis_flower_analysis\shapefile_data\Germany_district.shp'

# output shapefile containing the state schleswig holstein
sh_state = r'C:\Users\Gift\Desktop\git\arcgis\arcgis_flower_analysis\output_shapefiles\SH_state.shp'

# output shapefile containing the districts in schleswig holstein
sh_districts = r'C:\Users\Gift\Desktop\git\arcgis\arcgis_flower_analysis\output_shapefiles\SH_district.shp'

#create a new layers
g_states = arcpy.mapping.Layer(german_states)
g_districts = arcpy.mapping.Layer(german_districts)


# add the layer to the map at the bottom of the TOC in data frame 0
arcpy.mapping.AddLayer(df, g_districts,"BOTTOM")
arcpy.mapping.AddLayer(df, g_states,"BOTTOM")

#Select Schleswig holstein from the states
arcpy.Select_analysis(german_states,sh_state, """"GEN" = 'Schleswig-Holstein'""")

#Intersect german states and german districts
inputfeatures = [sh_state,german_districts]
arcpy.Intersect_analysis(inputfeatures,sh_districts,"ALL")

#Fxn to add fields to shapefile
def add_field(str):
    arcpy.AddField_management(sh_districts,str,"TEXT")

#Calling add field function
add_field("District")
add_field("State")

#Fxn to calculate fields 
def calc_field(field,exp):
    arcpy.CalculateField_management(sh_districts,field,exp,"PYTHON")   

#Calling calculate field function    
calc_field("District",'!GEN_1!')
calc_field("State",'!GEN!')

#Fxn to delete fields 
def del_field(str):
    arcpy.DeleteField_management(sh_districts,str)

#Calling delete field function    
del_field("FID_SH_sta")
del_field("USE")
del_field("RS")
del_field("RS_ALT")
del_field("GEN")
del_field("SHAPE_LENG")
del_field("SHAPE_AREA")
del_field("FID_German")
del_field("USE_1")
del_field("RS_1")
del_field("RS_ALT_1")
del_field("GEN_1")
del_field("SHAPE_LE_1")
del_field("SHAPE_AR_1")




