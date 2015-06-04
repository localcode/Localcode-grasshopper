## 'import' loads in a module: a collection of Python files in a folder.
import postsites

## assign your folder of GIS files and your DB login to a variable
my_data_folder = 'C:\LA2'
dbinfo = {'user':'postgres', 'dbname':'LA2', 'password':'postgrespass'}

## If the database already exists, you can connect to it by
## creating a 'DataSource'.
## 'DataSource' acts as a middleman between you and the database.
ds = postsites.DataSource (dbinfo)

## copy/paste desired layers to resemble dictionary below. Delete '/n' symbols.
## create formatted dictionary 'myLayerDict'. eliminate unneeded 'cols' 
myLayerDict = {'culvertpoint':{ 'name': 'culvertpoint', 'cols':['objectid', 'ogc_fid']},'basin':{ 'name': 'basin', 'cols':['objectid', 'ogc_fid']},'culvert':{ 'name': 'culvert', 'cols':['shape_leng', 'objectid', 'ogc_fid']},'catchbasin':{ 'name': 'catchbasin', 'cols':['objectid', 'ogc_fid']},'channelpoint':{ 'name': 'channelpoint', 'cols':['objectid', 'ogc_fid']},'gravitymain':{ 'name': 'gravitymain', 'cols':['shape_leng', 'objectid', 'ogc_fid']},'lateralline':{ 'name': 'lateralline', 'cols':['shape_leng', 'objectid', 'ogc_fid']},'lowflowpoint':{ 'name': 'lowflowpoint', 'cols':['objectid', 'ogc_fid']},'naturaldrainage':{ 'name': 'naturaldrainage', 'cols':['shape_leng', 'objectid', 'ogc_fid']},'openchannel':{ 'name': 'openchannel', 'cols':['shape_leng', 'objectid', 'ogc_fid']},'proposed_sites':{'name': 'proposed_sites', 'cols':['count_1', 'sum_buff_d', 'sum_longit', 'sum_latitu', 'sum_oid_', 'count_', 'has_bb', 'shape_len','shape_area', 'tot_units', 'pm_ref', 'unit_no', 'parcel_typ', 'editorname', 'udate', 'block', 'usecode', 'tract', 'subdtype', 'pcltype', 'tra', 'moved', 'unit', 'lot', 'phase', 'ain', 'perimeter', 'assrdata_m', 'objectid', 'fid_1_1', 'fid_1', 'ogc_fid']},'proposed_sites_buffer100a':{ 'name': 'proposed_sites_buffer100a', 'cols':['buff_dist', 'count_1', 'sum_buff_d', 'sum_longit', 'sum_latitu','sum_oid_', 'count_', 'has_bb', 'shape_len', 'shape_area', 'tot_units', 'pm_ref', 'unit_no', 'parcel_typ', 'editorname', 'udate', 'block', 'usecode', 'tract', 'subdtype', 'pcltype', 'tra', 'moved', 'unit', 'lot', 'phase', 'ain', 'perimeter', 'assrdata_m', 'objectid', 'fid_1_1', 'fid_1', 'ogc_fid']},'pseudoline':{ 'name': 'pseudoline', 'cols':['shape_leng', 'objectid', 'ogc_fid']},'random_pts150':{ 'name': 'random_pts150', 'cols':['sum', 'f9953cat_3', 'f9953cat_2', 'f9953cat_1', 'f9953catd1', 'f9953catd_', 'f9953catd', 'f9952cat_3', 'f9952cat_2', 'f9952cat_1', 'f9952catd1', 'f9952catd_', 'f9952catd', 'f9930catd', 'f9006cat_7', 'f9006cat_6', 'f9006cat_5', 'f9006cat_4', 'f9006cat_3', 'f9006cat_2', 'f9006cat_1', 'f9006catd1', 'f9006catd_', 'f9006catd', 'cid', 'ogc_fid']}}

## DataSource can now be loaded with your layer dictionary
ds.loadLayerDict(myLayerDict)

## a DataSource contains a 'config' object with useful variables
ds.config.setSiteLayer('proposed_sites')

ds.config.siteRadius = 150

## get the id of polygon of interest from a GIS program
## 'getSiteJson' returns everything within 'siteRadius' of the polygon 'id'
## on your site layer. It is returned as a string in geoJSON format.
def batchSites(start, numSites, file_path):
    for n in range(start,(numSites)):
        mysiteJson = ds.getSiteJson(id=n)
        f=open(file_path+str(n)+'.txt','w')
        f.writelines(mysiteJson)
        f.close()

file_path = 'E:/Local Code/Work/Local Code - Los Angeles/02 geoJSON/15_06_03/'
batchSites(390, 768, file_path) #or any number of sites