import os,sys,json
import exifread
import requests
from pprint import pprint


#apiKey是高德地图的自己申请就完事了
def geocode1(location, apiKey):
    r = requests.get("https://restapi.amap.com/v3/geocode/regeo?output=json&location=" + location + "&key=" + apiKey + "&radius=1000&extensions=all")
    result = r.json()
    if result != None:
        result = result.get("regeocode")
    if result != None:
        result = result.get("addressComponent")
    if result != None:
        pprint(result)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[-] 请传递一个图片地址")
    else:
        ImageName = str(sys.argv[1])
        with open(ImageName,'rb') as f:
            tags = exifread.process_file(f)
            if  'Image Make' in tags:
                print("设备品牌: {}".format(tags['Image Make']))
            if  'Image Model' in tags:   
                print("具体型号: {}".format(tags['Image Model']))
            if  'EXIF ExifImageWidth' and 'EXIF ExifImageLength' in tags:
                print('照片尺寸: {} x {}'.format(tags['EXIF ExifImageWidth'], tags['EXIF ExifImageLength']))
            if  'Image DateTime' in tags:
                print("创建日期: {}".format(tags['Image DateTime']))
            if  'EXIF DateTimeOriginal' in tags:
                print("拍摄时间: {}".format(tags["EXIF DateTimeOriginal"].printable))
            if  'GPS GPSProcessingMethod' in tags:
                print("GPS处理方法: {}".format(tags['GPS GPSProcessingMethod']))
            if  'GPS GPSTimeStamp' in tags:
                print("GPSTimeStamp: {}".format(tags['GPS GPSTimeStamp']))
            if  'Image Software' in tags:
                print("拍摄软件版本: {}".format(tags['Image Software']))
            #纬度
            LatRef=tags["GPS GPSLatitudeRef"].printable
            Lat=tags["GPS GPSLatitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
            Lat=float(Lat[0])+float(Lat[1])/60+float(Lat[2])/float(Lat[3])/3600
            if LatRef != "N":
                Lat=Lat*(-1)
            #经度
            LonRef=tags["GPS GPSLongitudeRef"].printable
            Lon=tags["GPS GPSLongitude"].printable[1:-1].replace(" ","").replace("/",",").split(",")
            Lon=float(Lon[0])+float(Lon[1])/60+float(Lon[2])/float(Lon[3])/3600
            if LonRef!="E":
                Lon=Lon*(-1)
            f.close()
            #print("目标所在经纬度: {},{}".format(Lat,Lon))
            Lat = str(Lat)
            Lon = str(Lon)
            Lat = Lat[:Lat.rfind('.') + 7]
            Lon = Lon[:Lon.rfind('.') + 7]
            locationslocations= Lon + ',' + Lat
            #print(locationslocations)
            geocode1(locationslocations, "6666666666666666666")
