from ._anvil_designer import moreParameterTemplate
from .userCropParameter import userCropParameter
from anvil import *
import anvil.server
import anvil.users
import copy
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

class moreParameter(moreParameterTemplate):
  

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items=[]
    rows=anvil.server.call('get_allZhiKaiKou_info')
    for row in rows:
      for crop in row['crop_infor']:
        tempRow=[{'user':row['User']['email'],'cropName':crop['cropName']}]
        self.repeating_panel_1.items= self.repeating_panel_1.items + copy.deepcopy( tempRow ) 
     
    # Any code you write here will run before the form opens.
