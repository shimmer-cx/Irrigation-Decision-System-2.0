from ._anvil_designer import irrigationHistoryTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class irrigationHistory(irrigationHistoryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.grid_panel_1.get_components()
    # Any code you write here will run before the form opens.
