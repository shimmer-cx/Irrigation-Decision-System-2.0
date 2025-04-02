from ._anvil_designer import cropBasicInfoTemplate
from anvil import *
import copy

class cropBasicInfo(cropBasicInfoTemplate):
  crop_row={'cropName':'玉米','Type':'默认','plantMethod':'默认','areaRatio':100,'plantDate':'缺失','harvesDate':'缺失'}
  num_rows=0#表的行数
  diffrentCrop=[]

  v=False
  def __init__(self, **properties):
    self.item={'cropName':['玉米','小麦','水稻','土豆','其他'],
      'crop_type':['叶菜类','根/块茎','果实/谷物'],
      'PlantMethod':['移栽','播种']}
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items=[]
    # Any code you write here will run before the form opens.

  def cropName_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.cropName_drop_down.selected_value=='其他':
      self.v=True
    else:
      self.crop_row['cropName']=self.cropName_drop_down.selected_value
      self.v=False
    self.refresh_data_bindings()

  def text_box_1_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.crop_row['cropName']=self.text_box_1.text

  def dropdown_menu_2_change(self, **event_args):
    """This method is called when an item is selected"""
    self.crop_row['Type']=self.dropdown_menu_2.selected_value

  def dropdown_menu_3_change(self, **event_args):
    """This method is called when an item is selected"""
    self.crop_row['plantMethod']=self.dropdown_menu_3.selected_value

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

    
    if self.crop_row['cropName'] not in self.diffrentCrop:
      """This method is called when the component is clicked."""
      self.num_rows=self.num_rows+1
      tempRow=[self.crop_row]

      self.repeating_panel_1.items= self.repeating_panel_1.items + copy.deepcopy( tempRow ) 
      #更新组件显示
      self.cropName_drop_down.selected_value='玉米'
      self.text_1.text=''
      self.text_box_2.text=''
      self.text_box_3.text=''
      
      self.v=False
      self.diffrentCrop=self.diffrentCrop+ [self.repeating_panel_1.items[-1]['cropName']]
      self.refresh_data_bindings()
    else:
      Notification('已经添加过该作物了！').show()

  def button_2_click(self, **event_args):
    """This method is called when the component is clicked."""
    self.repeating_panel_1.items=[]
    self.diffrentCrop=[]
    self.num_rows=0
    self.crop_row={'cropName':'玉米','Type':'默认','plantMethod':'默认','areaRatio':100,'plantDate':'缺失','harvesDate':'缺失'}
