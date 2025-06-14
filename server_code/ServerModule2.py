
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

'''说明：此类服务器模块中为AquaCrop模型运行相关的方法函数
'''

def GetForecastWeather(location,days):#获取预报气象数据
   
    #使用缓存设置Open-Meteo API客户端，并在出现错误时重试
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": location[0],
	    "longitude": location[1],
	    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "et0_fao_evapotranspiration"],
	    "wind_speed_unit": "ms",
	    "timezone": "Asia/Shanghai",
      "past_days": days,#如果在模拟当天获取数据，days=0,否则days=1
      "forecast_days": 14,
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



def Get_weather_data(simStartDate, location, current_user, crop):
    new_Row=(app_tables.weatherdata.get(User=current_user,crop=crop)
             or app_tables.weatherdata.add_row(User=current_user,crop=crop,Date=[-1]))
    Start_Date=datetime.strptime(simStartDate, "%Y/%m/%d")
   
    # 定义北京时区
    beijing_tz = ZoneInfo('Asia/Shanghai')
    # 获取北京时间
    beijing_time = datetime.now(beijing_tz).replace(tzinfo=None,hour=0, minute=0, second=0, microsecond=0)
 
    #获取预测气象数据(#如果在模拟当天获取数据，days=0)
    if beijing_time-Start_Date==timedelta(days=0):#模拟当天
  
      forecast_weather=GetForecastWeather(location,0)
      forecast_weather=forecast_weather.iloc[:-6]#取预报8天
      new_Row['MinTemp']=list(forecast_weather['MinTemp'])
      new_Row['MaxTemp']=list(forecast_weather['MaxTemp'])
      new_Row['Precipitation']=list(forecast_weather['Precipitation'])
      new_Row['ReferenceET']=list(forecast_weather['ReferenceET'])
      new_Row['Date']= [date.strftime('%Y-%m-%d') for date in list(forecast_weather['Date'])]
      return forecast_weather#取预报8天
    elif beijing_time-Start_Date==timedelta(days=1):#第二天
      if new_Row['Date'][0] !=-1 and datetime.strptime(new_Row['Date'][-8],'%Y-%m-%d')==beijing_time:#数据库中已经有气象预报数据了
        weatherData={'MinTemp':new_Row['MinTemp'],'MaxTemp':new_Row['MaxTemp'],'Precipitation':new_Row['Precipitation'],
                     'ReferenceET':new_Row['ReferenceET'],'Date':[datetime.strptime(date,'%Y-%m-%d') for date in new_Row['Date']]}
        return pd.DataFrame(weatherData)
      else:
        forecast_weather=GetForecastWeather(location,1)
        forecast_weather=forecast_weather.iloc[:-6]#取历史1天和预报8天
     
        new_Row['MinTemp']=list(forecast_weather['MinTemp'])
        new_Row['MaxTemp']=list(forecast_weather['MaxTemp'])
        new_Row['Precipitation']=list(forecast_weather['Precipitation'])
        new_Row['ReferenceET']=list(forecast_weather['ReferenceET'])
        new_Row['Date']= [date.strftime('%Y-%m-%d') for date in list(forecast_weather['Date'])]
        return forecast_weather
    elif beijing_time-Start_Date>timedelta(days=1):#以后

      if new_Row['Date'][0] !=-1 and datetime.strptime(new_Row['Date'][-8],'%Y-%m-%d')==beijing_time:#数据库中已经有气象预报数据了
        weatherData={'MinTemp':new_Row['MinTemp'],'MaxTemp':new_Row['MaxTemp'],'Precipitation':new_Row['Precipitation'],
                     'ReferenceET':new_Row['ReferenceET'],'Date':[datetime.strptime(date,'%Y-%m-%d') for date in new_Row['Date']]}
        return pd.DataFrame(weatherData)
      else:
        days=(beijing_time-datetime.strptime(new_Row['Date'][-8],'%Y-%m-%d'))/timedelta(days=1)
        forecast_weather=GetForecastWeather(location,int(days))
        forecast_weather=forecast_weather.iloc[:-6]#取历史days和预报8天
     
        list_1=new_Row['MinTemp'][:-8]+list(forecast_weather['MinTemp'])
        list_2=new_Row['MaxTemp'][:-8]+list(forecast_weather['MaxTemp'])
        list_3=new_Row['Precipitation'][:-8]+list(forecast_weather['Precipitation'])
        list_4=new_Row['ReferenceET'][:-8]+list(forecast_weather['ReferenceET'])
        Date=[datetime.strptime(date,'%Y-%m-%d') for date in new_Row['Date'][:-8]]
        list_5=Date+list(forecast_weather['Date'])
      
        weatherData={'MinTemp':list_1,'MaxTemp':list_2,'Precipitation':list_3,'ReferenceET':list_4,'Date':list_5}
        new_Row['MinTemp']=list_1
        new_Row['MaxTemp']=list_2
        new_Row['Precipitation']=list_3
        new_Row['ReferenceET']=list_4
        new_Row['Date']=[date.strftime('%Y-%m-%d') for date in list_5]
      
        return pd.DataFrame(weatherData)
    
     

      
def CustomSoil(soilType ):

    built_inSoilTypes={'黏土':"Clay", '黏壤土':"ClayLoam", '默认':'Default',
                      '壤土':"Loam", '壤砂土':"LoamySand", '砂土':"Sand", '砂黏土' :"SandyClay",
                      '砂质黏壤土':"SandyClayLoam", '砂壤土':"SandyLoam", '粉土':"Silt",
                      '粉砂黏壤土':"SiltClayLoam", '粉质壤土':"SiltLoam", '粉质黏土':"SiltClay"}
    # Clay:黏土    # Loam:壤土    # Sand:砂土    # Silt：粉土
    
    custom = Soil(soil_type=built_inSoilTypes[soilType])

    return custom

def CustomCrop(crop_param,user):

    crop_name=crop_param['cropName']
    planting_date=crop_param['plantDate']
    harvest_date=crop_param['harvesDate']
    # PlantMethod=crop_param['plantMethod']
    built_inCrop={ "土豆":"Potato",
                "土豆GDD":"PotatoGDD",
                "本地土豆GDD":"PotatoLocalGDD",
                "大豆":"Soybean",
                "大豆GDD":"SoybeanGDD",
                "大麦":"Barley",
                "大麦GDD":"BarleyGDD",
                "冬小麦GDD":"WheatGDD_1dec",
                "番茄":"Tomato",
                "番茄GDD":"TomatoGDD",
                "甘蔗":"SugarCane",
                "高粱":"Sorghum",
                "高粱GDD":"SorghumGDD",
                "冠军玉米GDD":"MaizeChampionGDD",
                "棉花":"Cotton",
                "棉花GDD":"CottonGDD",
                "水培麦GDD":"HydWheatGDD",
                "水润稻":"PaddyRice",
                "水润稻GDD":"PaddyRiceGDD",
                "甜菜":"SugarBeet",
                "甜菜GDD":"SugarBeetGDD",
                "乡稻":"localpaddy",
                "向日葵":"Sunflower",
                "向日葵GDD":"SunflowerGDD",
                "小麦":"Wheat",
                "小麦GDD":"WheatGDD",
                "玉米":"Maize",
                "玉米GDD":"MaizeGDD",
                "长丰麦GDD":"WheatLongGDD",
                "干安豆/旱地豆":"DryBean",
                "干安豆GDD":"DryBeanGDD",
                "默认":"Default",
                "木薯":"Cassava",
                "苜蓿GDD":"AlfalfaGDD",
                "藜麦":"Quinoa"}
  
    crop= Crop(built_inCrop[crop_name],planting_date=planting_date,harvest_date=harvest_date)
    crop_param_row=app_tables.usercropparameter.get(User=user['email'])
    if crop_param_row is not None:
      crop.__dict__.update(
        (k, v) for k, v in crop_param_row['parameter_value'].items()#如果管理中心为用户设定了作物参数，将更新到模型中
      )
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


@anvil.server.background_task
def RunModel(current_user):
    # 定义北京时区
    beijing_tz = ZoneInfo('Asia/Shanghai')
    # 获取北京时间
    beijing_time = datetime.now(beijing_tz).replace(tzinfo=None)    
    if beijing_time.hour<datetime.strptime("08:00:00","%H:%M:%S").hour :
      return  "早上八点之后再运行"
    data = app_tables.zhikaikouuser_data.get(User=current_user)  
    if data is None or current_user is None:# or current_user['is_manager'] is True:
      return  '新用户或从没有提交过模型数据的就不要执行以下模块/管理员账户也不用执行'
    irri_info=app_tables.irrigation_decisions.search(User=current_user)
    if irri_info is not None:
      for info in irri_info:
        if  beijing_time.strftime('%Y-%m-%d') in info['submit_time']:
          return  '当日已经运行过也不用执行'
      
    sim_startDate = data['irrigationArea_infor'][-1]
    location = data['irrigationArea_infor'][1:3]
    crop_params =data['crop_infor']
    smt =data['soil_infor'][1:]
    Zhikaikou_code=data['irrigationArea_infor'][0]
    soil=CustomSoil(data['soil_infor'][0])
    groundWater=CustomGroundWater(data['water_table'])

    nowTime=beijing_time.strftime('%Y-%m-%d %H:%M:%S')
    N=7   #从现在开始向前运行 N 天，也即模拟结束时间为一周后结束,由于模型自身因素。只能计算到未来第6天
    sim_endDate =beijing_time+ timedelta(days=N)
    sim_endDate=sim_endDate.strftime('%Y/%m/%d')
    #SMT | list[float] | 每个生长阶段要维持的土壤水分目标（%TAW）
    irr_mngt=IrrigationManagement(irrigation_method=1,SMT=smt)

    for crop_param in crop_params:
      
      new_Row=(app_tables.irrigation_decisions.get(crop_name=crop_param['cropName'],User=current_user)
               or app_tables.irrigation_decisions.add_row(crop_name=crop_param['cropName'],User=current_user))
      
      crop=CustomCrop(crop_param,current_user)
      area =data['irrigationArea_infor'][3]*(crop_param["areaRatio"]/100)
        
      weather_df=Get_weather_data(sim_startDate,location,current_user,crop_param['cropName'])#维度和经度
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
      water_flux=water_flux.iloc[:-1]#删除最后一行0行
      irrigation =list( water_flux['IrrDay'])
      for i in range(0, len(irrigation)):
        irrigation[i]=round(irrigation[i]*area*0.6666667,2)      #亩的单位要换算
     
      water_content =list(  water_flux['Wr'])#'Wr作物根区水分'
      # actual_transpiration =list(  water_flux['Tr'])#作物蒸腾量（mm）。
      # new_Row['actual_transpiration']=[round(x, 2) for x in actual_transpiration]
      new_Row['irrigation']=irrigation
      new_Row['water_content']=[round(x, 2) for x in water_content]
      # new_Row['InitialWaterContent_PlantNum']=water_storage
      new_Row['submit_time']=nowTime
      new_Row['Zhikaikou_code']=Zhikaikou_code
      new_Row['date_list']= [date.strftime('%Y-%m-%d') for date in pd.date_range(start=sim_startDate, periods=len(irrigation), freq="D")]
      
    return '计算完成'

@anvil.server.callable
@anvil.tables.in_transaction
def background_task_RunModel():
  user=anvil.users.get_user()
  infor_run=anvil.server.launch_background_task('RunModel',user)
  return infor_run