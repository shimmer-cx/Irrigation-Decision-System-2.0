from ._anvil_designer import userCropParameterTemplate
from anvil import *
import anvil.server
import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media


class userCropParameter(userCropParameterTemplate):

  cropName=''
  userName=''
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
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.heading_1.text='上传用户（'+self.userName+'）的'+self.cropName+'作物参数'
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    #下载参数表格文件:
    
    media=anvil.server.call('downLoadCropParamsExcel',self.built_inCrop[self.cropName],self.userName)
    anvil.media.download(media)

  def file_loader_2_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if self.file_loader_2.file is not None:
      anvil.server.call('upload_crop_parameter',self.file_loader_2.file,self.built_inCrop[self.cropName],self.userName)
      Notification('文件上传成功').show()

   
      

  
    
    
    
    
