from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
import anvil.users


class HomePage(HomePageTemplate):
  
  def __init__(self, **properties):
    
    anvil.server.call('background_task_RunModel')
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user = anvil.users.get_user()
    if user is not None:
      self.icon_button_1.icon='mi:frame_person'
      self.text_4.text=user['email']
    else:
      self.icon_button_1.icon='mi:frame_person_off'
      self.text_4.text='请登录'
    # Any code you write here will run before the form opens.



  def image_2_mouse_up(self, x, y, button, **event_args):
    """This method is called when a mouse button is released on this component"""
    self.rich_text_2.content="AquaCrop用于处理粮食安全和评估环境和管理对作物生产的影响。 AquaCrop模拟草本作物对水的产量反应，特别是当水是作物生产中的关键限制因素时。 AquaCrop平衡精度，简单性和稳健性。为了确保其广泛的适用性，它仅使用可以用简单的方法来确定的少量的显式参数和大多数直观的输入变量。"

    
  def image_2_mouse_leave(self, x, y, **event_args):
    """This method is called when the mouse cursor leaves this component"""
    self.rich_text_2.content=""





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
      if anvil.server.call('get_zhiKaiKou_info') is None :
        Notification('你还未完成直开口相关信息输入！').show()
      elif anvil.server.call('get_irrigation_info') is None:
          Notification('系统今天可能还未完成首次计算！').show()
      else:
        open_form('irrigationPage')

        
        

  def navigation_link_4_click(self, **event_args):
    """This method is called when the component is clicked"""
    user = anvil.users.get_user()
    if user is None:
      Notification('请先登录再尝试！').show()
    else:
     if user['is_manager'] is True:
        open_form('Manage_map')
     else:
        Notification('当前账户非管理中心账户！').show()

  def navigation_link_5_click(self, **event_args):
    """This method is called when the component is clicked"""
    user = anvil.users.get_user()
    if user is None:
      Notification('请先登录再尝试！').show()
    else:
      if user['is_manager'] is True:
        open_form('Manage_central')
      else:
        Notification('当前账户非管理中心账户！').show()

  def navigation_link_1_click(self, **event_args):
    """This method is called when the component is clicked"""
    user = anvil.users.get_user()
    if user is None:
      Notification('请先登录再尝试！').show()
    else:
      if user['is_manager'] is True:
        open_form('moreParameter')
      else:
        Notification('当前账户非管理中心账户！').show()

  # def form_show(self, **event_args):
  #   """This method is called when the form is shown on the page"""
  #   self.user = anvil.users.get_user()



  def icon_button_1_click(self, **event_args):
    if anvil.users.get_user() is None:
      user=anvil.users.login_with_form()
      if user is not None:
        self.icon_button_1.icon='mi:frame_person'
        self.text_4.text=user['email']
        Notification('登录成功！').show()
    else:
      anvil.users.logout()
      self.icon_button_1.icon='mi:frame_person_off'
      self.text_4.text='请登录'
      Notification('已退出登录！').show()

 

    


 



      
