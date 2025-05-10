from ._anvil_designer import Manage_centralTemplate
from anvil import *
import anvil.server
import anvil.users
import copy


class Manage_central(Manage_centralTemplate):
  datas=[]
  
  def __init__(self, **properties):
    self.datas=anvil.server.call('getAllUsersIrriInfo')
    self.item=[]
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    if self.datas is not None:
      info_row={'Zhikaikou_code':'','crop_name':'','lastIrrigationDate':'','lastIrrigationVolume':0,'nextIrrigationDate':'','naxtIrrigationVolume':0,'totallVolum':0}
      for data in self.datas:
        info_row['Zhikaikou_code']=data['Zhikaikou_code']
        info_row['crop_name']=data['crop_name']
        irrigation=data['irrigation']
        date_list=data['date_list']
        #反向列表
        irrigation.reverse()
        date_list.reverse()#反向列表
        #历史灌溉记录
        irri_history=irrigation[6:]
        date_history=date_list[6:]
        for irri,date in zip(irri_history,date_history):
          if irri>0:
            info_row['lastIrrigationVolume']=irri
            info_row['lastIrrigationDate']=date
            break
        info_row['totallVolum']=round(sum(irri_history),2)
        irri_future= irrigation[0:6]
        date_future= date_list[0:6]
        irri_future.reverse()#再反回来列表
        date_future.reverse()#再反回来列表
        for irri,date in zip(irri_future,date_future):
          if irri>0:
            info_row['naxtIrrigationVolume']=irri
            info_row['nextIrrigationDate']=date    
            break
        self.item=self.item+copy.deepcopy([info_row]) 
      self.repeating_panel_1.items=self.item
