from ._anvil_designer import irrigationPageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class irrigationPage(irrigationPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def interactive_card_1_click(self, **event_args):
    """This method is called when the component is clicked"""
    open_form('irrigationPage.irrigationHistory')




 
