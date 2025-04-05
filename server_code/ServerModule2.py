import anvil.users
import anvil.server
import anvil.tables as tables
import pandas as pd

import openmeteo_requests
import requests_cache
from retry_requests import retry

from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from anvil.tables import app_tables
from aquacrop import AquaCropModel, IrrigationManagement, InitialWaterContent, GroundWater,Crop,Soil 
import copy

def GetForecastWeather(lat,lon,Day):#获取预报气象数据
   
    #使用缓存设置Open-Meteo API客户端，并在出现错误时重试
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": lat,#银川
	    "longitude": lon,
	    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "et0_fao_evapotranspiration"],
	    "wind_speed_unit": "ms",
	    "timezone": "Asia/Shanghai",
      "past_days": Day,
      # "forecast_days": 7,
	    "models": "cma_grapes_global"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
 
    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    daily_et0_fao_evapotranspiration = daily.Variables(3).ValuesAsNumpy()
  
    daily_data = {"Date": pd.date_range(
  	  start = pd.to_datetime(daily.Time()+28800 , unit="s", utc = True).replace(tzinfo = None).floor("D"),
	    end = pd.to_datetime(daily.TimeEnd()+28800 , unit = "s", utc = True).replace(tzinfo = None).floor("D"),
	    freq = pd.Timedelta(seconds = daily.Interval()),
	    inclusive = "left"
    )}

    daily_data["MaxTemp"] = daily_temperature_2m_max
    daily_data["MinTemp"] = daily_temperature_2m_min
    daily_data["Precipitation"] = daily_precipitation_sum
    daily_data["ReferenceET"] = daily_et0_fao_evapotranspiration

    daily_dataframe = pd.DataFrame(data = daily_data)
  
    #按要求交换列的顺序
    daily_dataframe=daily_dataframe[['MinTemp','MaxTemp','Precipitation','ReferenceET','Date']]

    return daily_dataframe

def GetHistoryWeather(lat,lon,start_date,end_dat):#获取历史气象数据

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
	    "latitude": lat,
	    "longitude": lon,
	    "start_date": start_date,
	    "end_date": end_dat,
	    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "et0_fao_evapotranspiration"],
	    "timezone": "Asia/Singapore",
    }

    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    daily_et0_fao_evapotranspiration = daily.Variables(3).ValuesAsNumpy()

    daily_data = {"Date": pd.date_range(
	    start = pd.to_datetime(daily.Time()+28800, unit = "s", utc = True).replace(tzinfo = None).floor("D"),
	    end = pd.to_datetime(daily.TimeEnd()+28800, unit = "s", utc = True).replace(tzinfo = None).floor("D"),
	    freq = pd.Timedelta(seconds = daily.Interval()),
	    inclusive = "left"
    )}

    daily_data["MaxTemp"] = daily_temperature_2m_max
    daily_data["MinTemp"] = daily_temperature_2m_min
    daily_data["Precipitation"] = daily_precipitation_sum
    daily_data["ReferenceET"] = daily_et0_fao_evapotranspiration

    daily_dataframe = pd.DataFrame(data = daily_data)
    #把时间列放在最后,日最低温度列放在第一列
    daily_dataframe=daily_dataframe[['MinTemp','MaxTemp','Precipitation','ReferenceET','Date']]

    return daily_dataframe


def Get_weather_data(simStartDate, location):
    
    Start_Date=datetime.strptime(simStartDate, "%Y/%m/%d")
    sim_Start_Date=Start_Date.strftime('%Y-%m-%d')
    # day=3#历史气象数据最晚到3天前的数据
    # 定义北京时区
    beijing_tz = ZoneInfo('Asia/Shanghai')
    # 获取北京时间
    beijing_time = datetime.now(beijing_tz).replace(tzinfo=None)
    d=(beijing_time-Start_Date)/ timedelta(days=1)
    if d >= 3:

      end_date =beijing_time-timedelta(days=3)
      end_date=end_date.strftime('%Y-%m-%d')
      #获取历史气象数据
      history_weather=GetHistoryWeather(location[0],location[1],sim_Start_Date,end_date)
      #获取预测气象数据(里面包含了2天的历史数据)
      forecast_weather=GetForecastWeather(location[0],location[1],2)
      return pd.concat([history_weather,forecast_weather])
    else:

      #获取预测气象数据(里面包含了1天的历史数据)
      forecast_weather=GetForecastWeather(location[0],location[1],d)
      return forecast_weather
      
   

def CustomSoil(soilParam):

    soilType =soilParam[0]
    Sand =soilParam[1]
    Clay =soilParam[2]
    thWP =soilParam[3]
    thFC =soilParam[4]
    orgMat =soilParam[5]
    ksat =soilParam[6]
  
    built_inSoilTypes={'自定义':"custom", '黏土':"Clay", '黏壤土':"ClayLoam", '默认':'Default',
                      '壤土':"Loam", '壤砂土':"LoamySand", '砂土':"Sand", '砂黏土' :"SandyClay",
                      '砂质黏壤土':"SandyClayLoam", '砂壤土':"SandyLoam", '粉土':"Silt",
                      '粉砂黏壤土':"SiltClayLoam", '粉质壤土':"SiltLoam", '粉质黏土':"SiltClay"}
    # Clay:黏土    # Loam:壤土    # Sand:砂土    # Silt：粉土
    if soilType != '自定义':
      custom = Soil(soil_type=built_inSoilTypes[soilType])
    else:
      #自定义土壤类别可以通过在创建 土壤 时传递 'custom' 作为土壤类型来创建。
      custom = Soil('custom',cn=46,rew=7)# 我们创建了一个具有曲线数（CN=46）和易蒸发水（REW=7）的自定义土壤。
      # custom.zSoil = float(soil_depth)#土壤剖面的总深度 [m]。
      #土壤水力特性随后使用 .add_layer() 指定。
      custom.add_layer(thickness=0.3,#此函数需要第一层土壤层厚度 [m]
                    thWP=thWP,#萎蔫点含水量 [m^3/m^3]
                    thFC=thFC,#田间持水量 [m^3/m^3]
                    thS=0.50,#饱和度 [m^3/m^3]
                    Ksat=ksat,#以及水力传导率 [mm/day]
                    penetrability=100)
      '''土壤水力特性也可以通过土壤质地组成来指定。这两种层创建方法可以组合在一起来创建多层土壤。
      注意：请注意，当您使用多层土壤剖面时，还必须指定多层初始含水量剖面，否则模型将所有层设置为默认的田间持水量'''
      custom.add_layer_from_texture(thickness=1.2,#第二层土壤厚度 [m]
                              Sand=Sand,#土壤中的砂含量 [%]
                              Clay=Clay,#土壤中的粘土含量 [%]
                              OrgMat=orgMat,#土壤中的有机物质含量 [%]
                              penetrability=100)
    return custom

def CustomCrop(crop_param):

    crop_name=crop_param['cropName']
    CropType=crop_param['Type']
    planting_date=crop_param['plantDate']
    harvest_date=crop_param['harvesDate']
    PlantMethod=crop_param['plantMethod']

    CropTypes={"叶菜类":1,"根/块茎":2,"果实/谷物":3}#作物类型（1 = 叶菜类，2 = 根/块茎，3 = 果实/谷物）
    PlantMethods={"移栽":0,"播种":1}#播种方法（0 = 移栽，1 = 播种）
    built_inCropTypes={'玉米':'Maize', '小麦':'Wheat','水稻':'Rice', '土豆':'Potato'}#the built-in crop types
  
    if crop_name not in built_inCropTypes:
      crop = Crop('custom', planting_date=planting_date,harvest_date=harvest_date,
                    CropType=CropTypes[CropType],
                    PlantMethod=PlantMethods[PlantMethod])
    else:     
      crop= Crop(built_inCropTypes[crop_name],planting_date=planting_date,harvest_date=harvest_date)
    return crop

def CustomGroundWater(waterTable):
  
    if  waterTable is not None and waterTable != []:
      Dates=[]
      Values=[]
      #'date':'','depth'
      for recor in waterTable:
        Dates=Dates + copy.deepcopy([recor['date']] ) 
        Values=Values + copy.deepcopy( [recor['depth']] ) 
        
      groundWater=GroundWater(water_table='Y',#是提供地下水位
                        dates=Dates,#日期字符串列表形式
                        values=Values)#地下水位深度 [m]
    else:
      groundWater=GroundWater(water_table='N')#否提供地下水位（是或否）

    return groundWater


@anvil.server.callable
def RunModel(current_user):
     
    data = app_tables.zhikaikouuser_data.get(User=current_user)  
    if data is None or current_user is None:
      return  '新用户或从没有提交过模型数据的就不要执行以下模块'
    
    sim_startDate = data['irrigationArea_infor'][-1]
    location = data['irrigationArea_infor'][1:3]
    crop_params =data['crop_infor']
    soilParam =data['soil_infor'][0:7]
    smt =data['soil_infor'][7:11]

    soil=CustomSoil(soilParam)
    groundWater=CustomGroundWater(data['water_table'])
    # 定义北京时区
    beijing_tz = ZoneInfo('Asia/Shanghai')
    # 获取北京时间
    beijing_time = datetime.now(beijing_tz).replace(tzinfo=None)
    nowTime=beijing_time.strftime('%Y-%m-%d %H:%M:%S')
    N=7   #从现在开始向前运行 N 天，也即模拟结束时间为一周后结束,由于模型自身因素。只能计算到未来第6天
    sim_endDate =beijing_time+ timedelta(days=N-1)
    sim_endDate=sim_endDate.strftime('%Y/%m/%d')
    #SMT | list[float] | 每个生长阶段要维持的土壤水分目标（%TAW）
    irr_mngt=IrrigationManagement(irrigation_method=1,SMT=smt)

  
    for crop_param in crop_params:
      
      new_Row=(app_tables.irrigation_decisions.get(crop_name=crop_param['cropName'],User=current_user)
               or app_tables.irrigation_decisions.add_row(crop_name=crop_param['cropName'],is_firstRun=True,User=current_user))
      
      crop=CustomCrop(crop_param)
      area =data['irrigationArea_infor'][3]*(crop_param["areaRatio"]/100)

      if new_Row['is_firstRun'] is True:    #要区分是否为第一次模拟
        
        weather_df=Get_weather_data(sim_startDate,location)#维度和经度
        initialWater=InitialWaterContent(value = ['SAT'])
        model = AquaCropModel(sim_start_time=sim_startDate,
                          sim_end_time=sim_endDate,
                          weather_df=weather_df,
                          soil=soil,
                          crop=crop,
                          initial_water_content=initialWater,
                          irrigation_management=irr_mngt,
                          groundwater=groundWater) # create model
        model.run_model(till_termination=True)#Run
      
        water_flux=model._outputs.water_flux
        #water_flux=water_flux[ water_flux['season_counter'] ==0]#使用布尔表达式：根据条件过滤 DataFrame
        water_flux=water_flux.iloc[:-1]
        irrigation =list( water_flux['IrrDay'])
        for i in range(0, len(irrigation)):
          irrigation[i]=round(irrigation[i]*area*0.6666667, 2)      #亩的单位要换算
          
        water_storage=model._outputs.water_storage         
        lenth=water_storage.shape[0]
        water_storage=water_storage.iloc[lenth-7,3:15]#获取当日的土壤水分含量
        water_storage=list(water_storage)
        water_content =list(  water_flux['Wr'])#'Wr作物根区水分'
        actual_transpiration =list(  water_flux['Tr'])#作物蒸腾量（mm）。

        new_Row['actual_transpiration']=[round(x, 2) for x in actual_transpiration]
        new_Row['irrigation']=irrigation
        new_Row['water_content']=[round(x, 2) for x in water_content]
        new_Row['InitialWaterContent_Num']=water_storage
        # new_Row['submit_time']=nowTime
        new_Row['date_list']= [date.strftime('%Y-%m-%d') for date in pd.date_range(start=sim_startDate, periods=lenth-1, freq="D")]
        new_Row['is_firstRun'] = False
      else:
        
        sim_startDate = beijing_time- timedelta(days=1)
        sim_startDate= sim_startDate.strftime('%Y/%m/%d')
        weather_df=Get_weather_data(sim_startDate,location)#维度和经度
        Num= new_Row['InitialWaterContent_Num']
        initialWater=InitialWaterContent(wc_type = 'Prop',
                                        method = 'Layer',
                                        depth_layer= [1,2,3,4,5,6,7,8,9,10,11,12],
                                        value = Num )#要将土壤初始含水量设置到上次计算出来的结果，暂未修改
      
        model = AquaCropModel(sim_start_time=sim_startDate,
                          sim_end_time=sim_endDate,
                          weather_df=weather_df,
                          soil=soil,
                          crop=crop,
                          initial_water_content=initialWater,
                          irrigation_management=irr_mngt,
                          groundwater=groundWater) # create model
        model.run_model(till_termination=True)#Run
      
        water_flux=model._outputs.water_flux
        #water_flux=water_flux[ water_flux['season_counter'] ==0]#使用布尔表达式：根据条件过滤 DataFrame
        water_flux=water_flux.iloc[:-1]#删除最后一行0行
      
        irrigation =list( water_flux['IrrDay'])
        for i in range(0, len(irrigation)):
          irrigation[i]=round(irrigation[i]*area*0.6666667, 2)        #亩的单位要换算
          
        water_storage=model._outputs.water_storage         
        water_storage=water_storage.iloc[1,3:15]#获取当日的土壤水分含量,1：留下今天的Num
        water_storage=list(water_storage)
        
        water_content =list(  water_flux['Wr'])
        actual_transpiration =list(  water_flux['Tr'])
        datelist= [date.strftime('%Y-%m-%d') for date in pd.date_range(start=sim_startDate, periods=7 ,freq="D")]
        new_Row['irrigation']=new_Row['irrigation'][0:-6]+irrigation
        new_Row['water_content']= new_Row['water_content'][0:-6]+ [round(x, 2) for x in water_content]
        new_Row['actual_transpiration']=new_Row['actual_transpiration'][0:-6]+ [round(x, 2) for x in actual_transpiration]
        new_Row['InitialWaterContent_Num'] = water_storage
        new_Row['date_list']= new_Row['date_list'][0:-6] + datelist
        # new_Row['submit_time']=nowTime

    return '计算完成'

