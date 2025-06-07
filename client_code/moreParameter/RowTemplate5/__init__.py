from ._anvil_designer import RowTemplate5Template
from ..userCropParameter import userCropParameter
from anvil import *
# import anvil.server
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    userCropParameter.cropName=self.item['cropName']
    userCropParameter.userName=self.item['user']
    open_form('moreParameter.userCropParameter')
