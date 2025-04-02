import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from pandas import DateOffset

@anvil.server.background_task
def save_BasicInfo_irrigationArea(data):
   # Get the logged in user
    current_user = anvil.users.get_user()
    # Check that someone is logged in
    if current_user is not None:
      # 获取北京时间
      now_time = datetime.now()+DateOffset(hours=8)
      
      user_row = (app_tables.zhikaikouuser_data.get(User=current_user)
               or app_tables.zhikaikouuser_data.add_row(User=current_user))
      user_row['submit_time']=now_time.strftime('%Y-%m-%d %H:%M:%S')
      user_row['irrigationArea_infor']=data

@anvil.server.callable
def launch_save_irrigationArea(data):
   anvil.server.launch_background_task('save_BasicInfo_irrigationArea',data)
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
