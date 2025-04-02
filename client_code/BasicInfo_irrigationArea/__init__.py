from ._anvil_designer import BasicInfo_irrigationAreaTemplate
from anvil import *
import anvil.server
import anvil.users



class BasicInfo_irrigationArea(BasicInfo_irrigationAreaTemplate):
  def __init__(self, **properties):
    self.item=['1',38.236,106.296,0,'']
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def text_box_1_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.item[0]=self.text_box_1.text

  def text_box_2_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.item[1]=self.text_box_2.text

  def text_box_3_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.item[2]=self.text_box_3.text

  def text_box_4_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.item[3]=self.text_box_4.text

  def text_box_5_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self.item[4]=self.text_box_5.text

  def navigation_link_2_click(self, **event_args):
    """This method is called when the component is clicked"""

  def form_hide(self, **event_args):
    """This method is called when the form is removed from the page"""
    anvil.server.call('launch_save_irrigationArea',self.item)




    


