from ._anvil_designer import Manage_mapTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Manage_map(Manage_mapTemplate):
  lat_lon=[38.236,106.296]
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.google_map_1.center= GoogleMap.LatLng(self.lat_lon[0],self.lat_lon[1])
    self.google_map_1.zoom = 13
    # Any code you write here will run before the form opens.
