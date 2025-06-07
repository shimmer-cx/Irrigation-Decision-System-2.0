from ._anvil_designer import cropBasicInfoTemplate
from anvil import *
import anvil.server
import anvil.users

import copy

class cropBasicInfo(cropBasicInfoTemplate):
  crop_row={'cropName':None,'areaRatio':100,'plantDate':'缺失','harvesDate':'缺失'}
  num_rows=0#表的行数
  diffrentCrop=[]

  def __init__(self, **properties):
    self.item=[ "土豆",  "土豆GDD", "本地土豆GDD", "大豆", "大豆GDD", "大麦", "大麦GDD",   "小麦",   "小麦GDD",  "冬小麦GDD", "水培麦GDD", "番茄",  "番茄GDD",   "甘蔗",   "高粱",
                           "高粱GDD",    "玉米",   "玉米GDD",   "冠军玉米GDD",  "棉花",   "棉花GDD",   "水稻",  "水稻GDD",   "乡稻",
                            "甜菜",   "甜菜GDD",  "向日葵",    "向日葵GDD",  "长丰麦GDD",    "干安豆/旱地豆",  "干安豆GDD",    "默认",  "木薯",   "苜蓿GDD","藜麦"]

    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items=[]
    # Any code you write here will run before the form opens.

  def cropName_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    self.crop_row['cropName']=self.cropName_drop_down.selected_value


  def text_box_2_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.crop_row['plantDate']=self.text_box_2.text

  def text_box_3_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.crop_row['harvesDate']=self.text_box_3.text

  def slider_1_change_end(self, **event_args):
    """This method is called when the Slider is no longer being dragged"""
    self.crop_row['areaRatio']=self.slider_1.value

  def button_1_click(self, **event_args):
    if self.crop_row['cropName'] is not None :
      if  self.crop_row['cropName'] not in self.diffrentCrop:
        """This method is called when the component is clicked."""
        self.num_rows=self.num_rows+1
        tempRow=[self.crop_row]

        self.repeating_panel_1.items= self.repeating_panel_1.items + copy.deepcopy( tempRow ) 
        #更新组件显示
        self.cropName_drop_down.selected_value=None
        self.text_box_2.text=''
        self.text_box_3.text=''
        self.crop_row['plantDate']='缺失'
        self.crop_row['harvesDate']='缺失'
        self.diffrentCrop=self.diffrentCrop+ [self.repeating_panel_1.items[-1]['cropName']]
        self.refresh_data_bindings()
      else:
        Notification('已经添加过该作物了！').show()
    else:
      Notification('请选择作物后再试！').show()

  def button_2_click(self, **event_args):
    """This method is called when the component is clicked."""
    self.repeating_panel_1.items=[]
    self.diffrentCrop=[]
    self.num_rows=0
    self.cropName_drop_down.selected_value=None
    self.crop_row={'cropName':None,'areaRatio':100,'plantDate':'缺失','harvesDate':'缺失'}

  def form_hide(self, **event_args):
    """This method is called when the form is removed from the page"""
    if self.repeating_panel_1.items is not None and self.repeating_panel_1.items !=[]:
      anvil.server.call('launch_save_Zhikaikou_data','crop_infor',self.repeating_panel_1.items)

  def slider_1_change(self, **event_args):
    """This method is called when the value of the component is changed"""
    self.text_2.text=str(self.slider_1.value)+'%'


 
