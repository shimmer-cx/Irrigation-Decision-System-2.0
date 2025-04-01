from ._anvil_designer import RowTemplate1Template
from .. import cropBasicInfo
import copy
from anvil import *


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called clicked"""


    # self.remove_from_parent()
    # cropBasicInfo.num_rows=cropBasicInfo.num_rows-1
    

    Notification("清空成功！").show()

