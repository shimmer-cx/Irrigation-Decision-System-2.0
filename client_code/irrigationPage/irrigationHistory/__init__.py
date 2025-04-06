from ._anvil_designer import irrigationHistoryTemplate
from anvil import *
import anvil.server
import anvil.users
import copy


class irrigationHistory(irrigationHistoryTemplate):
  irri_history=[]
  date_history=[]
  cropName=''
  def __init__(self, **properties):
    self.item=[]
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # self.grid_panel_1.get_components()
    # Any code you write here will run before the form opens.

  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    self.heading_1.text=self.cropName+'的灌溉历史'
    for irri,date in zip(self.irri_history,self.date_history):
      tempRow=[{'irri_history':irri,'date_history':date}]
      self.item=self.item+copy.deepcopy( tempRow ) 
    self.repeating_panel_1.items=self.item
    # self.item['irri_history'].reverse()#原列表是倒序的，所以再反回来
    # self.item['date_future'].reverse()

