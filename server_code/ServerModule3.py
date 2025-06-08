
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import requests
import datetime

'''此服务器模块用于获取历史和预报气象数据并储存在数据库中'''

#获取历史数据
def GetHistoryWeather(lat,lon,start_date,end_dat):#获取历史气象数据
 
    # 配置参数
    api_key = "YOUR_API_KEY"  # 替换为你的和风天气API密钥[1,9](@ref)
    location = "101010100"    # 城市ID（北京示例，其他城市ID需自行查询）
    days = 10                 # 获取最近10天数据

    # 计算日期范围（结束日期=昨天，开始日期=10天前）
    end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y%m%d")

    # 构造请求URL（商业版API）
    url = f"https://api.qweather.com/v7/historical/air?location={location}&date={start_date}&end_date={end_date}&key={api_key}"

    # 发送请求并处理响应
    try:
     response = requests.get(url)
     response.raise_for_status()  # 检查HTTP错误
     data = response.json()

     if data["code"] == "200":
       # 解析空气质量数据
       for daily_data in data["daily"]:
          date = daily_data["fxDate"]
          aqi = daily_data["aqi"]
          pm25 = daily_data["pm2p5"]
          print(f"日期: {date}, AQI: {aqi}, PM2.5: {pm25}μg/m³")
     else:
        print(f"API返回错误: {data['code']}, 消息: {data.get('message', '未知错误')}")

    except requests.exceptions.RequestException as e:
      print(f"请求失败: {e}")
    except KeyError:
      print("响应数据格式异常，请检查API文档更新")

   