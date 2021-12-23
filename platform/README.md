# 必循遵循JSON规范 如果写错会导致全部失效!

目前可调整禁用地图

pwd.json = 国服
steam.json = 国际服
允许为每个服务器定义
ne_credits  = 基础预定地图积分
mce_exclude  = 地图CD循环张数

更新后version 必须+1 否则不同步
样本
```javascript
    {
      "version": 8,
      "data": {
        "ne_credits": 400,
        "mce_exclude": 10,
        "SERVER_TYPE_ZE": {
          "mce_exclude": 55,
          "DisableMaps": [
            "ze_doom3_v2",
            "ze_diddle_v3"
          ]
        },
        "SERVER_TYPE_PROPHUNT": {
          "mce_exclude": 30,
          "DisableMaps": [
            "cs_office",
            "bili27_pack"
          ]
        }
      }
    }
```


# data 下结构说明
字段名 | 类型 | 说明
:-: | :-: | :-:
SERVER_TYPE_XXX           | 对象 | 特定服务器 特定设置 如果没有指定 则以全局参数为准
Command_OnConfigsExecuted | 数组 | 地图加载后执行参数
AddCommandOverride_Flag   | 对象 | 变更命令权限flaghelper用户 Lv1 = r Lv2 = s
Store_FreeItem            | 数组 | Store系统中免费物品
mce_exclude               | 对象 | 地图循环次数池              



