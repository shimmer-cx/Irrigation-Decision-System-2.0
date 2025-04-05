import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from zoneinfo import ZoneInfo


@anvil.server.background_task
def save_Zhikaikou_data(current_user,whatData,data):
   # Get the logged in user
    # current_user = anvil.users.get_user()#在后台任务中无法获得当前登录！！！！
    # Check that someone is logged in
    if current_user is not None:
      # 定义北京时区
      beijing_tz = ZoneInfo('Asia/Shanghai')
      # 获取北京时间
      now_time = datetime.now(beijing_tz).replace(tzinfo=None)
      
      user_row = (app_tables.zhikaikouuser_data.get(User=current_user)
               or app_tables.zhikaikouuser_data.add_row(User=current_user))
      user_row['submit_time']=now_time.strftime('%Y-%m-%d %H:%M:%S')
      user_row[whatData]=data

@anvil.server.callable
def launch_save_Zhikaikou_data(whatData,data):
    current_user = anvil.users.get_user()
    anvil.server.launch_background_task('save_Zhikaikou_data',current_user,whatData,data)



  
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
