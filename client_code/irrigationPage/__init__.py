from ._anvil_designer import irrigationPageTemplate
from anvil import *
import anvil.server
import anvil.users
from ..irrigationPage.irrigationHistory import irrigationHistory


class irrigationPage(irrigationPageTemplate):

  # irri_history=[]
  # date_history=[]
  n=1

  def __init__(self, **properties):
    self.item=anvil.server.call('get_irrigation_info')
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    

    # Any code you write here will run before the form opens.

  def interactive_card_1_click(self, **event_args):
    """This method is called when the component is clicked"""
    open_form('irrigationPage.irrigationHistory')

  def toIrriInfo(self,data):
    # data=self.item[0]  
    self.heading_2.text=data['crop_name']
    irrigationHistory.cropName=data['crop_name']#
    irrigation=data['irrigation']
    date_list=data['date_list']
    irrigation.reverse()#反向列表
    date_list.reverse()#反向列表
    irri_history=irrigation[8:]
    date_history=date_list[8:]
    irrigationHistory.irri_history=irri_history#
    irrigationHistory.date_history=date_history#
    irri_future= irrigation[0:8]
    date_future= date_list[0:8]
    irri_future.reverse()#再反回来列表
    date_future.reverse()#再反回来列表
    for irri,date in zip(irri_history,date_history):
      if irri>0:
        self.text_1.text='灌溉量：'+str(irri)+'m3'
        self.text_1_copy.text=date
        break
    for irri,date in zip(irri_future,date_future):
      if irri>0:
        self.text_2.text='灌溉量：'+str(irri)+'m3'
        self.text_3.text=date    
        break
    Tr=data['actual_transpiration']
    self.text_5.text=str(Tr[-7])+'mm(今日)'
    self.text_4.text=str(Tr[-6])+'mm(明日)'
    Wr=data['water_content']
    self.text_6.text=str(Wr[-7])+'mm(今日)'
    self.text_6_copy.text=str(Wr[-6])+'mm(明日)'

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    if len(self.item)==1:
      self.button_5.visible=False
      self.button_4.visible=False
      self.divider_1.visible=False
    else:
      self.button_5.visible=True
      self.button_4.visible=True
      self.divider_1.visible=True
    self.toIrriInfo(self.item[self.n-1])

  def button_5_click(self, **event_args):
    """This method is called when the component is clicked."""
    if  self.n>1:
      self.n=self.n-1
      self.toIrriInfo(self.item[self.n-1])

  def button_4_click(self, **event_args):
    """This method is called when the component is clicked."""
    if  self.n<len(self.item):
      self.n=self.n+1
      self.toIrriInfo(self.item[self.n-1])

    
    




 
