import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


def CustomSoil(soilType, Sand, Clay,thWP,thFC,orgMat,ksat):
    from aquacrop import Soil
    built_inSoilTypes={'自定义':"custom", '黏土':"Clay", '黏壤土':"ClayLoam", '默认':'Default',
                      '壤土':"Loam", '壤砂土':"LoamySand", '砂土':"Sand", '砂黏土' :"SandyClay",
                      '砂质黏壤土':"SandyClayLoam", '砂壤土':"SandyLoam", '粉土':"Silt",
                      '粉砂黏壤土':"SiltClayLoam", '粉质壤土':"SiltLoam", '粉质黏土':"SiltClay"}
    # Clay:黏土
    # Loam:壤土
    # Sand:砂土
    # Silt：粉土
    if soilType != '自定义':
      custom = Soil(soil_type=built_inSoilTypes[soilType])
    else:
      #自定义土壤类别可以通过在创建 土壤 时传递 'custom' 作为土壤类型来创建。
      custom = Soil('custom',cn=46,rew=7)# 我们创建了一个具有曲线数（CN=46）和易蒸发水（REW=7）的自定义土壤。
      # custom.zSoil = float(soil_depth)#土壤剖面的总深度 [m]。
      #土壤水力特性随后使用 .add_layer() 指定。
      custom.add_layer(thickness=0.3,#此函数需要第一层土壤层厚度 [m]
                    thWP=thWP,#萎蔫点含水量 [m^3/m^3]
                    thFC=thFC,#田间持水量 [m^3/m^3]
                    thS=0.50,#饱和度 [m^3/m^3]
                    Ksat=ksat,#以及水力传导率 [mm/day]
                    penetrability=100)
      '''土壤水力特性也可以通过土壤质地组成来指定。这两种层创建方法可以组合在一起来创建多层土壤。
      注意：请注意，当您使用多层土壤剖面时，还必须指定多层初始含水量剖面，否则模型将所有层设置为默认的田间持水量'''
      custom.add_layer_from_texture(thickness=1.2,#第二层土壤厚度 [m]
                              Sand=Sand,#土壤中的砂含量 [%]
                              Clay=Clay,#土壤中的粘土含量 [%]
                              OrgMat=orgMat,
                              penetrability=100)#土壤中的有机物质含量 [%])
    return custom
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
