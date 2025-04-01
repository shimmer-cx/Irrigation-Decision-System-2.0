from ._anvil_designer import soilEnvironmentTemplate
from anvil import *


class soilEnvironment(soilEnvironmentTemplate):
  v=True
  def __init__(self, **properties):
    self.item={'soilType':['自定义','粘土','粘壤土','壤土','壤砂土','砂土','砂粘土','砂质粘壤土','砂壤土','粉土','粉质粘壤土','粉质壤土','粉质粘土']}
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def dropdown_menu_1_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.dropdown_menu_1.selected_value=='自定义':
      self.v=True
    else:
      self.v=False
    self.refresh_data_bindings()
