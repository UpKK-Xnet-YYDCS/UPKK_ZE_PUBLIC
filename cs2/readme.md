# 基础同步命令操作 
| **命令**                           | **权限**       | **描述**                                                                                      |
|-----------------------------------|---------------|---------------------------------------------------------------------------------------------|
| `css_git_update`                  | `@css/root`   | 触发Git同步操作，并将服务器类型输出到控制台并通知所有玩家。(通常无需手动操作 换图会自动触发(自动不会频繁触发 比如2次换图低于10分钟 则需要手动指令操作))        |
| `css_gitsync_check_cureentmap`    | `@css/root`   | 检查当前地图的配置文件信息，包括Stripper、EntWatch和map-cfg文件，输出文件修改日期、MD5哈希值和大小。   |


# 目录
|  目录说明 |   |
| ------------ | ------------ |
|  StripperCS2 |  地图Stripper热修复文件  |
|  counterstrikesharp |  绝大多数插件配置,以及地图禁用等 |
|  cs2fixes |  ZR模式的僵尸配置 cf2f管理等 |

# 地图配置 [MapChooser](https://github.com/UpKK-Xnet-YYDCS/UPKK_ZE_PUBLIC/blob/master/cs2/counterstrikesharp/configs/plugins/MapChooser)


| Key             | Value                          | Comment                                        |
|-----------------|--------------------------------|------------------------------------------------|
| workshop_id     | 3274462953                      | ID for the map workshop host_workshop_map     |
| enabled         | 1                              | 1 开启 0 禁用                                   |
| filename        | ze_p_v_z                        | 地图文件名                                     |
| updatedname     | 地图准确名称                     | 调用需要 如 ds_workshop_changelevel 地图名      |
| RestrictedTimes | 08:00-12:00;14:00-23:00         | 禁用时间段 支持多个 (即不在这些时间段都可以玩)  24:00是不合法的时间会导致无法解析(如果先前已被预定 则不起限制作用)      | 
| MinPlayers      | 16                             | 最低需要玩家(如果先前已被预定 则不起限制作用)                                   |
| search          | "植物;pvz"                       | 预定搜索多关键词                               |

# 配置样本
```plaintext
	"ze_p_v_z"
	{
		"workshop_id"		"3274462953"
		"enabled"		"1"
		"filename"		"ze_p_v_z"
		"updatedname"		"ze_p_v_z"
		"search"		"植物;pvz"
        	"RestrictedTimes" 	"01:00-06:00;14:00-23:50"
	}
```


# 地图预定
- !yd 地图名已支持


# CS2 ZE指挥系统
- !vl 名字可以投票成为指挥  或者 !lv @me
- !glow @me 
- !defend 放一个防守图标
- !tracer 开关激光
- !beacon 光环
- !leaders 显示所有指挥
- !leaderhelp 显示帮助指令
- !def b <#玩家id或者玩家名> 放置b图标 也可以是BCDE (备注:输入一次后系统将记住您的图标 再次输入 !def 则会是相同的类型 例如 b)
- !defl 效果同上,区别就是图标会follow跟随头顶
- 可以给别人上效果 例如#userid 或者 名字 以及 @me
