# -*- coding: utf-8 -*-
"""
@author: jmzhao
"""

from osgeo import gdal, ogr, osr
import os


#读取数据与位数变化
class GRID:
  #读图像文件
  def read_img(self,filename):
    dataset=gdal.Open(filename)    #打开文件
    im_width = dataset.RasterXSize  #栅格矩阵的列数
    im_height = dataset.RasterYSize  #栅格矩阵的行数
    im_geotrans = dataset.GetGeoTransform() #仿射矩阵
    im_proj = dataset.GetProjection() #地图投影信息
    im_data = dataset.ReadAsArray(0,0,im_width,im_height) #将数据写成数组，对应栅格矩阵
    del dataset 
    return im_proj,im_geotrans,im_data

  #写文件(tif)
  def write_img(self,filename,im_proj,im_geotrans,im_data):
    #gdal数据类型包括
    #gdal.GDT_Byte, 
    #gdal.GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
    #gdal.GDT_Float32, gdal.GDT_Float64
    #判断栅格数据的数据类型
    if 'int8' in im_data.dtype.name:
      datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
      datatype = gdal.GDT_UInt16
    else:
      datatype = gdal.GDT_Float32

    #判读数组维数
    if len(im_data.shape) == 3:
      im_bands, im_height, im_width = im_data.shape
    else:
      im_bands, (im_height, im_width) = 1,im_data.shape 

    #创建文件
    driver = gdal.GetDriverByName("GTiff")      #数据类型必须有，因为要计算需要多大内存空间
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)
    dataset.SetGeoTransform(im_geotrans)       #写入仿射变换参数
    dataset.SetProjection(im_proj)          #写入投影
    
    if im_bands == 1:
      dataset.GetRasterBand(1).WriteArray(im_data) #写入数组数据
    else:
      for i in range(im_bands):
        dataset.GetRasterBand(i+1).WriteArray(im_data[i])
    del dataset


#TIF文件转为SHP文件
def tif2shp(folder):
    os.chdir(folder)
    for raster in os.listdir(): #遍历路径中每一个文件，如果存在gdal不能打开的文件类型，则后续代码可能会报错。
        inraster = gdal.Open(raster)  #读取路径中的栅格数据
        inband = inraster.GetRasterBand(1)  #这个波段就是最后想要转为矢量的波段，如果是单波段数据的话那就都是1
        prj = osr.SpatialReference()  
        prj.ImportFromWkt(inraster.GetProjection())   #读取栅格数据的投影信息，用来为后面生成的矢量做准备
        outshp = raster[:-4] + ".shp" #给后面生成的矢量准备一个输出文件名，这里就是把原栅格的文件名后缀名改成shp了
        drv = ogr.GetDriverByName("ESRI Shapefile")
        if os.path.exists(outshp):  #若文件已经存在，则删除它继续重新做一遍
            drv.DeleteDataSource(outshp)
        Polygon = drv.CreateDataSource(outshp)  #创建一个目标文件
        Poly_layer = Polygon.CreateLayer(raster[:-4], srs = prj, geom_type = ogr.wkbMultiPolygon) #对shp文件创建一个图层，定义为多个面类
        newField = ogr.FieldDefn('value',ogr.OFTReal)  #给目标shp文件添加一个字段，用来存储原始栅格的pixel value
        Poly_layer.CreateField(newField)
        gdal.FPolygonize(inband, None, Poly_layer, 0) #核心函数，执行的就是栅格转矢量操作
        Polygon.SyncToDisk() 
        Polygon = None

if __name__ == "__main__":

    """---------------------------需要修改的部分-------------------------------"""
    pathTrue = "E:/GZInsar/Sample1"  #含有经纬度的文件夹
    path = "E:/GZInsar/samplefuse" #不含经纬度的文件夹 （需要添加的）
    output = "E:/GZInsar/out" #输出的文件夹
    """---------------------------需要修改的部分-------------------------------"""
    
    for i in range(len(os.listdir(path))):
        input_file_name = pathTrue + '/'+os.listdir(pathTrue)[i]
        input_file_name1 = path + '/'+os.listdir(path)[i]
        print('---------------------------------'*2)
        print('input_file_name',input_file_name)
        print('input_file_name1',input_file_name1)
        # im_width, im_height, im_bands, im_proj, im_geotrans, im_data = read_img(input_file_name)
        # im_data1 = cv2.imread(input_file_name1,0)
        run = GRID()
        im_proj,im_geotrans,im_data = run.read_img(input_file_name)    #读数据
        im_proj1,im_geotrans1,im_data1 = run.read_img(input_file_name1)#E:\GZInsar\samplefuse
        print('正在处理第{:.0f}张图片'.format(i+1))
        
        if i < 10:
            OutPut = output +'/'+'0' + str(i)+'.tif'
        else:
            OutPut = output +'/'+ str(i)+'.tif'
        run.write_img(OutPut,im_proj,im_geotrans, im_data1)
    #对栅格数据进行处理，转变为矢量.
    folder = output 
    tif2shp(folder)#调用函数
    os.chdir(folder)
    #输出的shp结果，均在一个文件夹中output的地址中.
print("FINISHED! ")