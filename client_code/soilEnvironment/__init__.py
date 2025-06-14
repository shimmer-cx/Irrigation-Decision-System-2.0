from ._anvil_designer import soilEnvironmentTemplate
from anvil import *
import anvil.server
import anvil.users
import copy



class soilEnvironment(soilEnvironmentTemplate):
  
  w_e=False
  soil_infor=['默认',60,70,80,50] # soilType, SMT[]
  
  waterTable_row={'date':'','depth':0}
  num_rows=0#表的行数
  diffrentDate=[]
  
  def __init__(self, **properties):
    self.item={'soilType':[ '黏土', '黏壤土', '壤土', '壤砂土', '砂土', '砂黏土' ,
                          '砂质黏壤土', '砂壤土', '粉土', '粉砂黏壤土', '粉质壤土', '粉质黏土', '默认']}
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items=[]
    # Any code you write here will run before the form opens.

  def dropdown_menu_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.soil_infor[0]=self.dropdown_menu_1.selected_value
  

  def checkbox_1_change(self, **event_args):
    """This method is called when the component is checked or unchecked"""
    if self.checkbox_1.checked is True:
      self.w_e=True
      if self.dropdown_menu_1.selected_value is not None:
        anvil.server.call('launch_save_Zhikaikou_data','soil_infor',self.soil_infor)
    else:
      self.w_e=False
    self.refresh_data_bindings()

 

  def form_hide(self, **event_args):
    """This method is called when the form is removed from the page"""
    if (self.checkbox_1.checked is False and self.dropdown_menu_1.selected_value is not None
       and self.text_box_9.text is not None and self.text_box_10.text is not None
       and self.text_box_11.text is not None and self.text_box_12.text is not None):
      anvil.server.call('launch_save_Zhikaikou_data','soil_infor',self.soil_infor)
      # anvil.server.call('launch_save_Zhikaikou_data','water_table',[])
    elif self.checkbox_1.checked is True and self.repeating_panel_1.items is not None:
      anvil.server.call('launch_save_Zhikaikou_data','water_table',self.repeating_panel_1.items)

  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    if self.waterTable_row['date'] not in self.diffrentDate:
      self.num_rows=self.num_rows+1
      tempRow=[self.waterTable_row]
      
      self.repeating_panel_1.items= self.repeating_panel_1.items + copy.deepcopy( tempRow ) 
      #更新组件显示
      self.text_box_5.text=''
      self.text_box_6.text=''
      
      self.diffrentDate=self.diffrentDate+ [self.repeating_panel_1.items[-1]['date']]
      self.refresh_data_bindings()
    else:
      Notification('未填写或已经添加过该日期的数据了！').show()

  def text_box_5_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.waterTable_row['date']=self.text_box_5.text

  def text_box_6_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.waterTable_row['depth']=self.text_box_6.text

  def text_box_9_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.soil_infor[-4]=self.text_box_9.text

  def text_box_10_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.soil_infor[-3]=self.text_box_10.text

  def text_box_11_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.soil_infor[-2]=self.text_box_11.text

  def text_box_12_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.soil_infor[-1]=self.text_box_12.text

  def button_2_click(self, **event_args):
    """This method is called when the component is clicked."""
    self.repeating_panel_1.items=[]
    self.diffrentDate=[]
    self.num_rows=0
    self.waterTable_row ={'date':'','depth':0}


    
      

