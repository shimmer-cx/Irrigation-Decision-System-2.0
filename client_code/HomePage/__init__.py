from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
import anvil.users



class HomePage(HomePageTemplate):
  
  def __init__(self, **properties):
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


  def image_2_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    self.rich_text_2.content="AquaCrop用于处理粮食安全和评估环境和管理对作物生产的影响。 AquaCrop模拟草本作物对水的产量反应，特别是当水是作物生产中的关键限制因素时。 AquaCrop平衡精度，简单性和稳健性。为了确保其广泛的适用性，它仅使用可以用简单的方法来确定的少量的显式参数和大多数直观的输入变量。"

    
  def image_2_mouse_leave(self, x, y, **event_args):
    """This method is called when the mouse cursor leaves this component"""
    self.rich_text_2.content=""

  def icon_button_1_click(self, **event_args):
    anvil.users.login_with_form()

  def icon_button_2_click(self, **event_args):
    anvil.users.logout()
    Notification('退出登录成功！').show()



  def link_1_click(self, **event_args):
    """This method is called clicked"""
    user = anvil.users.get_user()
    if user is None:
      Notification('请先登录再尝试！').show()
    else:
      open_form('BasicInfo_irrigationArea')

  def link_2_click(self, **event_args):
    """This method is called clicked"""
    user = anvil.users.get_user()
    if user is None:
      Notification('请先登录再尝试！').show()
    else:
      open_form()
    


 



      
