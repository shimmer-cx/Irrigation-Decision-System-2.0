from ._anvil_designer import irrigationPageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class irrigationPage(irrigationPageTemplate):
  def __init__(self, **properties):
    self.item=anvil.server.call('get_irrigation_info')
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if len(self.item)==1:
      self.button_5.visible=False
      self.button_4.visible=False
      # data=self.item[0]
      # for irri in data['irrigation'].reverse():
      #   if irri>0
          
        
    else:
      self.button_5.visible=True
      self.button_4.visible=True

    # Any code you write here will run before the form opens.

  def interactive_card_1_click(self, **event_args):
    """This method is called when the component is clicked"""
    open_form('irrigationPage.irrigationHistory')

  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    user=anvil.users.get_user()
    infor=anvil.server.call('RunModel',user)
    Notification(infor).show()

    
    




 
