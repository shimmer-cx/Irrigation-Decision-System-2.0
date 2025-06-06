from ._anvil_designer import userCropParameterTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from aquacrop import Crop
class userCropParameter(userCropParameterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    #下载参数表格文件:
    parameterFile=app_tables.files.get(path='allCropParameter.csv')['file']
    
    
