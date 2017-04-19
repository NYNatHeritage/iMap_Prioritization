import arcpy
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
snap_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.extent="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"
arcpy.env.snapRaster = "D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\LCA2_2013_Final1"

eo_raster="D:\\GIS Projects\\StateParks\\EO_Processing.gdb\\EO_Raster_Scores_test_4_w_0"

#EDM_raster="D:\\GIS Projects\\StateParks\\Clipped_Layers.gdb\\EDM_total_Richness_reclass"
EDM_raster="D:\GIS Projects\StateParks\Base_Layers.gdb\EDM_hyp344_norm_no0_for_add"
#bap="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\BAP_Raster"
bap="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\BAP_Raster_Null_is_0"
#mussels="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Mussels_pred_Conservative"
mussels="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Mussels_pred_Conservative_Null_is_0"


ecol_sig="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Ecological_Significance_8_12"

wrk="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\"
out_name="Ecological_Significance_8_12" 
out_raster=wrk+out_name   
comp_score=arcpy.sa.Raster(eo_raster)+arcpy.sa.Raster(EDM_raster)+arcpy.sa.Raster(bap)+arcpy.sa.Raster(mussels)
##Check raster

print arcpy.GetRasterProperties_management(comp_score,"COLUMNCOUNT")
print arcpy.GetRasterProperties_management(comp_score,"ROWCOUNT")
print arcpy.GetRasterProperties_management(comp_score,"ANYNODATA")
print arcpy.GetRasterProperties_management(comp_score,"MINIMUM")
print arcpy.GetRasterProperties_management(comp_score,"MAXIMUM")
print arcpy.GetRasterProperties_management(eo_raster,"MAXIMUM")

print arcpy.GetRasterProperties_management(eo_raster,"COLUMNCOUNT")


comp_score.save(out_raster)

##Make Protected Areas Raster to add to Ecological Significance
#Use categories of the NYPAD GAP IUCN codes

nypad="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\NYPADUS_G23"

nypadus="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\NY_PADUS_G23_UTM18N"

nypad="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\NYPADUS_G23_Null_is_0"


##Get list of npyad attribute values to rank/quantify in terms of conservation protection value

fields_list=["Loc_Ds"]
location_types=[]
with arcpy.da.SearchCursor(nypadus,fields_list) as rows:
    for row in rows:
        type=row[0]
        location_types.append(type)

distinct_types=set(location_types)
distinct_types_list=sorted(list(distinct_types))
##Score the NPYAD polys for the State Parks Biodiversity Index, use Mean values to rank

State_parks_score="D:\\GIS Projects\\StateParks\\Results.gdb\\Comprehensive_Score_05_10_4_1_1_July21mask"

out_table="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\NYPAD_SPR_score_inds"

zone="Loc_Nm"

arcpy.sa.ZonalStatisticsAsTable(nypadus,zone,State_parks_score,out_table)

out_table="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\NYPAD_SPR_score_Loc_Ds"

zone="Loc_Ds"

arcpy.sa.ZonalStatisticsAsTable(nypadus,zone,State_parks_score,out_table)

LCA="D:\\GIS Projects\\TreesforTribs\\BaseLayers.gdb\\LCA2_2013_ProjectRaster"




mock_score=(arcpy.sa.Raster(ecol_sig)+0.1)*(1.0+(arcpy.sa.Raster(nypad)*100.0))*(1.0+arcpy.sa.Raster(LCA))
mock_addition=(arcpy.sa.Raster(ecol_sig)+0.1)*(1.0+(arcpy.sa.Raster(nypad)*100.0))+(1.0+arcpy.sa.Raster(LCA))

mock_name="Mock_Comp_5_18_plus1_1_NYPAD_100"
mock_add_name="Mock_Comp_5_18_add"
wrk="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\"
mock_raster=wrk+mock_name
mock_add=wrk+mock_add_name
mock_addition.save(mock_add)


########################

#Transform the EO data
#EO data being used is the EO raster from the State Parks Ranks project. But those values have a huge tail. While this was important for the State Parks Ranks, we don't need this level of distinction between extremely rare and rariet sfor the Invasives Prioitization Project
#So we will log transform the data
input="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_06_17_con"
#eo_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_06_17_norm"
eo_raster="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_06_17_con"

wrk="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\"
in_raster=eo_raster
print arcpy.GetRasterProperties_management(in_raster,"COLUMNCOUNT")
print arcpy.GetRasterProperties_management(in_raster,"ROWCOUNT")
print arcpy.GetRasterProperties_management(in_raster,"ANYNODATA")
print arcpy.GetRasterProperties_management(in_raster,"BOTTOM")
print arcpy.GetRasterProperties_management(in_raster,"MAXIMUM")
print arcpy.GetRasterProperties_management(in_raster,"MINIMUM")

outLN=arcpy.sa.Ln(in_raster)

outLN.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\eo_6_17_logtrans")


mussels="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Mussels_pred_Conservative_Null_is_0"
in_raster=mussels
print arcpy.GetRasterProperties_management(in_raster,"COLUMNCOUNT")
print arcpy.GetRasterProperties_management(in_raster,"ROWCOUNT")
print arcpy.GetRasterProperties_management(in_raster,"ANYNODATA")
print arcpy.GetRasterProperties_management(in_raster,"BOTTOM")
print arcpy.GetRasterProperties_management(in_raster,"MAXIMUM")
print arcpy.GetRasterProperties_management(in_raster,"MINIMUM")

#mussel values represent predicted species so range from 0-17, re-scale so that max is 1, then weight
mussels="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Mussels_pred_Conservative_Null_is_0"
mussels_rast=arcpy.Raster(mussels)
max=mussels_rast.maximum
mussels_0_1=arcpy.sa.Raster(mussels)/(1.0*max)
mussels_0_1.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_mussels")

EDMS="D:\GIS Projects\StateParks\Base_Layers.gdb\EDM_hyp344_norm_no0_for_add"
##Did not need to normalize because the layer from Stat Parks Ranks was already normalized

##For reference this is the original layer
EDM_orignal="D:\\GIS Projects\\StateParks\\state_parks_baselayers.gdb\\Minus_hyp_345"
EDMS_rast=arcpy.Raster(EDM_orignal)
max=EDMS_rast.maximum
#EDMS_0_1=arcpy.sa.Raster(EDMS)/(1.0*max)
#EDMS_0_1.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EDMS")

BAP="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\BAP_Raster_Null_is_0"
BAP_rast=arcpy.Raster(BAP)
max=BAP_rast.maximum
BAP_0_1=arcpy.sa.Raster(BAP)/(1.0*max)
BAP_0_1.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_BAP")


EO="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\eo_6_17_logtrans"
EO_rast=arcpy.Raster(EO)
max=EO_rast.maximum
EO_0_1=arcpy.sa.Raster(EO)/(1.0*max)
EO_0_1.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO")

EO_layer="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO"

EO_isNull=arcpy.sa.IsNull(EO_layer)
EO_isNull.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO_isNull")
#####################################################
EO="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_06_17_con"
EO_rast=arcpy.Raster(EO)
max=EO_rast.maximum
EO_0_1=arcpy.sa.Raster(EO)/(1.0*max)
EO_0_1.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO_notLog")

EO_layer="D:\\GIS Projects\\StateParks\\Base_Layers.gdb\\Scored_EO_06_17_con"

EO_isNull=arcpy.sa.IsNull(EO_layer)
EO_isNull.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO_isNull_notLog")

EO="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\eo_sqrt_trans"
EO_rast=arcpy.Raster(EO)
max=EO_rast.maximum
EO_0_1=arcpy.sa.Raster(EO)/(1.0*max)
EO_0_1.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO_sqrt")

EO="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\eo_cubert_trans"
EO_rast=arcpy.Raster(EO)
max=EO_rast.maximum
EO_0_1=arcpy.sa.Raster(EO)/(1.0*max)
EO_0_1.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO_cubert")

##Transfor Distance to Campgrounds, Boat Launches, and Trails into score where the maximum value is closest to the stressor, and diminimshes as you get farther away

campgrounds="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Distance_to_Campgrounds_1000"
trails="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Distance_to_Trails_1000"
boat_launches="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Distance_to_BoatLaunches_1000"

campground_score= 1.0/(1.0+arcpy.sa.Raster(campgrounds))
trails_score= 1.0/(1.0+arcpy.sa.Raster(trails))
boat_launches_score= 1.0/(1.0+arcpy.sa.Raster(boat_launches))

campground_score.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_Campgrounds_1000")
trails_score.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_Trails_1000")
boat_launches_score.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_Boat_Launches_1000")


LCA="D:\\GIS Projects\\TreesforTribs\\BaseLayers.gdb\\LCA2_2013_ProjectRaster"
LCA_rast=arcpy.Raster(LCA)
max=LCA_rast.maximum

LCA_0_1=arcpy.sa.Raster(LCA)/(max*1.0)
LCA_0_1.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_LCA")
#########################################################################################################################
##Components for Priority Areas
##Natural Land
natural="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Natural_binary_noNulls"
#NYPAD
#NYPAD="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\NYPAD_Ranked_10_1_No_Null"
#out_NYPAD="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\NYPAD_Ranked_10_1_No_Null_project"
#arcpy.ProjectRaster_management(NYPAD,out_NYPAD,"D:\\GIS Projects\\Coordinate_Systems\\NAD 1983 UTM Zone 18N.prj")

NYPAD="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\NYPAD_Ranked_10_1_No_Null_project"
#Priority Areas Layer
##Weights: NPYAD *40 + Natural Land *10

Priority_Areas=(arcpy.sa.Raster(NYPAD)*1.5)+(arcpy.sa.Raster(natural)*5.0)
Priority_Areas.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Priority_Areas_919_15_5")

#####################################################################################
#Components for Ecological Significance
#EO_layer="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO_noNull"
#EO_layer="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO_notLog"
EO_layer="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO_sqrt"
#EO_layer="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_EO_cubert"
#Mussel_layer="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_mussels"
Mussel_layer="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_mussels_LIfix"
EDM_layer="D:\GIS Projects\StateParks\Base_Layers.gdb\EDM_hyp344_norm_no0_for_add"
#BAP_layer="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_BAP"
BAP_layer="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_BAP_LIfix"
Ecological_Significance=arcpy.sa.Raster(EO_layer)*50.0 +arcpy.sa.Raster(EDM_layer)*30.0+arcpy.sa.Raster(Mussel_layer)*5.0+arcpy.sa.Raster(BAP_layer)*5.0




#Ecological_Significance.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Ecological_Sig_930_50_30_5_5_sqrt")
Ecological_Significance.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Ecological_Sig_930_50_30_5_5_sqrt_LIfix")
######################################################################################

#Components for Risk of Spread_ Conventional

LCA="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_LCA"
Trails="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_Trails_1000_noNull"
Boat_Launches="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_Boat_Launches_1000_noNull"
Campgrounds="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Score_Campgrounds_1000_noNull"

Risk_of_Spread=(arcpy.sa.Raster(LCA)*35.0)+(arcpy.sa.Raster(Trails)*5.0)+(arcpy.sa.Raster(Boat_Launches)*5.0)+(arcpy.sa.Raster(Campgrounds)*5.0)

Risk_of_Spread.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Risk_of_Spread_912_35_5_5_5b")


######################################
#Comprehensive Score Components

#Ecol_Sig="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Ecological_Sig_912_50_30_10_10"
#Ecol_Sig="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Ecological_Sig_913_50_30_1_1"
#Ecol_Sig="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Ecological_Sig_915_50_30_10_10_cube"

#Ecol_Sig="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Ecological_Sig_930_50_30_5_5_sqrt"
Ecol_Sig="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Ecological_Sig_930_50_30_5_5_sqrt_LIfix"
#Priority_Areas="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Priority_Areas_912_40_10"

Priority_Areas="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Priority_Areas_919_15_5"

Risk="D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Risk_of_Spread_912_35_5_5_5"

sub_Score=arcpy.sa.Raster(Ecol_Sig)+arcpy.sa.Raster(Risk)
sub_Score.save("W:\\Projects\\iMap\\Prioritization\\NYNHP prioritization project\\Oct_Data\\Ecol_Sig_Plus_Risk.tif")

sub_Score=arcpy.sa.Raster(Ecol_Sig)+arcpy.sa.Raster(Priority_Areas)
sub_Score.save("W:\\Projects\\iMap\\Prioritization\\NYNHP prioritization project\\Oct_Data\\Ecol_Sig_Plus_Priority_Areas.tif")

sub_Score=arcpy.sa.Raster(Risk)+arcpy.sa.Raster(Priority_Areas)
sub_Score.save("W:\\Projects\\iMap\\Prioritization\\NYNHP prioritization project\\Oct_Data\\Risk_Plus_Priority_Areas.tif")

Comprehensive=arcpy.sa.Raster(Ecol_Sig)+arcpy.sa.Raster(Priority_Areas)+arcpy.sa.Raster(Risk)
Comprehensive.save("W:\\Projects\\iMap\\Prioritization\\NYNHP prioritization project\\Oct_Data\\Comprehensive_Score.tif")

Comprehensive.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Comprehensive_Score_LI")
#sub_score_Times=(arcpy.sa.Raster(Ecol_Sig))*(1.0+arcpy.sa.Raster(Risk)*1.0)
#sub_score_Times.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Ecol_Sig_Times_Risk")

sub_Score=arcpy.sa.Raster(Ecol_Sig)+arcpy.sa.Raster(Risk)
sub_Score.save("W:\\Projects\\iMap\\Prioritization\\NYNHP prioritization project\\Sept_Data\\Ecol_Sig_Plus_Risk.tif")

Comprehensive=arcpy.sa.Raster(Ecol_Sig)+arcpy.sa.Raster(Priority_Areas)+arcpy.sa.Raster(Risk)

Comprehensive.save("D:\\GIS Projects\\InvasivesPrioritization\\BaseLayers.gdb\\Comprehensive_Score_919")

arcpy.RasterToOtherFormat_conversion(Ecol_Sig,"W:\\Projects\\iMap\\Prioritization\\NYNHP prioritization project\\Oct_Data","TIFF")
arcpy.RasterToOtherFormat_conversion(Priority_Areas,"W:\\Projects\\iMap\\Prioritization\\NYNHP prioritization project\\Oct_Data","TIFF")
arcpy.RasterToOtherFormat_conversion(Risk,"W:\\Projects\\iMap\\Prioritization\\NYNHP prioritization project\\Oct_Data","TIFF")