from ._anvil_designer import RowTemplate1Template
from .. import cropBasicInfo

from anvil import *


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called clicked"""
    # crop_table= cropBasicInfo.repeating_panel_1.items
    # crop_table=crop_table.remove(self.item)
    # cropBasicInfo.repeating_panel_1.items=crop_table
    self.remove_from_parent()

