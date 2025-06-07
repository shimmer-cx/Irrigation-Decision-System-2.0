import anvil.files
from anvil.files import data_files

import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as 
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
from . import crop_params_code
import anvil.media
'''说明：此类文件中为数据库处理相关函数方法
'''

@anvil.server.background_task
def save_Zhikaikou_data(current_user,whatData,data): #在后台任务中无法获得当前登录！
    # Check that someone is logged in
    if current_user is not None:
      # 定义北京时区
      beijing_tz = ZoneInfo('Asia/Shanghai')
      # 获取北京时间
      now_time = datetime.now(beijing_tz).replace(tzinfo=None)
      
      user_row = (app_tables.zhikaikouuser_data.get(User=current_user)
               or app_tables.zhikaikouuser_data.add_row(User=current_user))
      user_row['submit_time']=now_time.strftime('%Y-%m-%d %H:%M:%S')
      user_row[whatData]=data

@anvil.server.callable
@anvil.tables.in_transaction
def launch_save_Zhikaikou_data(whatData,data):
    current_user = anvil.users.get_user()
    anvil.server.launch_background_task('save_Zhikaikou_data',current_user,whatData,data)

@anvil.server.callable
@anvil.tables.in_transaction
def get_irrigation_info():
    current_user = anvil.users.get_user()
    if current_user is not None:
      return app_tables.irrigation_decisions.search(User=current_user)
      
@anvil.server.callable
@anvil.tables.in_transaction
def getAllUsersIrriInfo():
    return app_tables.irrigation_decisions.search()

@anvil.server.callable
@anvil.tables.in_transaction
def get_zhiKaiKou_info():
  current_user = anvil.users.get_user()
  if current_user is not None:
    return app_tables.zhikaikouuser_data.get(User=current_user)

@anvil.server.callable
@anvil.tables.in_transaction
def downLoadCropParamsExcel(cropName,userName):
    parameterDescription=["Vol (%) below saturation at which stress begins to occur due to deficient aeration",
                        "最大冠层覆盖度（土壤覆盖比例）",    "冠层下降系数（每GDD/日历日的分数）",        "",
                        "冠层生长系数（每GDD的分数）",      "",        "日历类型(1 =日历天数，2=生长度日）",
                        "作物类型",   "作物确定性(0 =不定型，1=确定型）",    "Adjustment to water stress thresholds depending on daily ET0 (0 No, 1 Yes)",
                        "从播种到出苗或移栽恢复的生长度/日历天数",      "",   "开花持续时间（以生长度/日历日计算，非果粮作物为-999）",
                        "",      "作物蒸腾作用不发生时的生长度日（℃/天）",      "作物完全蒸腾潜力所需的最低生长度日（℃/天）",
                        "生长度日计算方法",    "参考收获指数",       "从播种到开始形成产量的生长度/日历天数",      "",
                        "当冠层生长完成但尚未进入衰老阶段时的作物系数",     "从播种到成熟期的生长度/日历天数",
                        "",    "从播种到最大生根期的生长度/日历天数",          "",        "作物名称",     "种植方式",      "每公顷CCx的植物数量",  
                        "受冷应激影响的授粉(0 =否，1=是）",     "热应激对授粉的影响(0 =否，1=是）",   "植物Pop中，单株幼苗在90%出苗时所覆盖的土壤表面积（cm2）",
                        "从播种到衰老的生长度/日历天数",      "",    "是否将日历转换为GDD模式(0 =否；1=是）",      "根区底部的最大根系水分提取量(m3/ m3/天）",
                        "根区顶部的最大根水提取量（m3/m3/天）",     "基础温度（℃），低于此温度生长不会继续，",       "完全无法完成授粉的最高空气温度（℃）",
                        "开始发生授粉失败的最大空气温度（℃）",   "完全无法完成授粉的最低空气温度（℃）",     "最低气温（℃），低于此温度时授粉开始失败",
                        "冷温度应激对蒸腾作用的影响(0 =否，1=是）",  "作物生长不再增加的温度上限（℃）",   "以ET0和C02为基准的水生产力（g/m2）",
                        "产量形成阶段水分生产率调整（%WP）",     "方法中产量形成持续时间",    "",       "",
                        "最大有效生根深度(m)",        "最小有效生根深度(m)",    "描述在产量形成期间对受限营养生长的收获指数产生积极影响的系数",
                        "描述在产量形成过程中气孔闭合对收获指数产生负面影响的系数",       "高于参考值的收获指数最大允许增幅系数",
                        "开花前因水分压力导致的收获指数可能增加（%）",     "潜在果实超额量",    "因老化导致的作物系数下降（%/天）",
                        "描述根扩展的形状因子",       "描述水胁迫对树冠扩展影响的形状因子",       "描述水分胁迫对气孔调控影响的形状因子",
                        "描述水分胁迫对树冠衰老影响的形状因子",       "描述水胁迫对授粉影响的形状因子",   "在大气二氧化碳浓度升高条件下作物的生长表现（%/100）",
                        "降低土壤水分枯竭阈值，以减轻水胁迫对树冠扩展的影响",   "降低土壤水分枯竭阈值，以减轻水胁迫对冠层气孔控制的影响",
                        "降低土壤水分枯竭阈值，以减轻水胁迫对树冠衰老的影响",     "降低土壤水分枯竭阈值，以减轻水胁迫对树冠授粉的影响",
                        "土壤水分枯竭阈值的提高，有助于缓解水胁迫对树冠扩展的影响",   "水胁迫对树冠气孔控制的影响下，土壤水分枯竭的上限阈值",
                        "水胁迫对树冠衰老影响的土壤水分枯竭上限",   "土壤水分枯竭阈值的提高，以应对水胁迫对树冠授粉的影响"  ]

    CropParameters={'参数名':list(crop_params_code.crop_params[cropName].keys()),
                     '设定值':list(crop_params_code.crop_params[cropName].values()),
                      '参数描述':parameterDescription}
    CropParams_df=pd.DataFrame(CropParameters)
    file_contents = CropParams_df.to_csv(index=False).encode()      # String as bytes
    my_media = anvil.BlobMedia(content_type="csv", content=file_contents, name=userName[:-4]+'_CropParameters.csv')
    return my_media

  
@anvil.server.callable
@anvil.tables.in_transaction
def upload_crop_parameter(my_media,cropName,userName):
    CropParams_df=pd.read_csv(my_media)
    userRow=(app_tables.usercropparameter.get(User=userName,cropName=cropName)
         or app_tables.usercropparameter.add_row(User=userName,cropName=cropName))
    userRow['parameter_file']=my_media
    userRow['parameter_value']=dict.fromkeys(list(crop_params_code.crop_params[cropName].keys()), list(CropParams_df['设定值']))
  