# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 19:20:36 2020

@author: comingboy
"""

import gdal, ogr, osr, os
import numpy as np

# 读取tif文件变成array
def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    return band.ReadAsArray()


#把array写入tif
def array2raster(rasterfn,newRasterfn,array):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = raster.RasterXSize
    rows = raster.RasterYSize

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()


fileone = 'source\dem.tif'
rasterArray = raster2array(fileone)

# 对dem进行一列的操作,比如映射某种关系,分级.....个人觉得会比 arcgis 栅格计算更方便一些
dem2 = rasterArray;
  
array2raster(fileone,'dem2.tif',dem2)

