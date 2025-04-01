from ._anvil_designer import cropBasicInfoTemplate
from anvil import *


class cropBasicInfo(cropBasicInfoTemplate):

  v=False
  def __init__(self, **properties):
    self.item={'cropName':['玉米','小麦','水稻','土豆','其他'],
      'crop_type':['叶菜类','根/块茎','果实/谷物'],
      'PlantMethod':['移栽','播种']}
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def cropName_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.cropName_drop_down.selected_value=='其他':
      self.v=True
    else:
      self.v=False
    self.refresh_data_bindings()
