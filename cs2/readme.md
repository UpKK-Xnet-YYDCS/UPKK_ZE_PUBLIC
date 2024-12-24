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


| 指令            | 说明                                                                                             |
|-----------------|--------------------------------------------------------------------------------------------------|
| `!vl 名字`      | 投票某人成为指挥或使用 `!lv @me` 投票自己成为指挥。                                              |
| `!glow @me`     | 给自己添加光效。                                                                                 |
| `!defend`       | 放置一个防守图标。                                                                               |
| `!tracer`       | 开关激光。                                                                                       |
| `!beacon`       | 启用光环效果。                                                                                   |
| `!leaders`      | 显示所有指挥。                                                                                   |
| `!leaderhelp`   | 显示帮助指令。                                                                                   |
| `!def b <参数>` | 放置指定类型的图标，参数可以是玩家ID或玩家名（例如 BCDE）。                                        |
| `!defauto`      | 自动放置标记，按照顺序ABCED自动放置。绑定游戏 `player_ping`，因此鼠标中键有效。                   |
| `!def_usepingpos` | 切换是否使用游戏自带的 `player_ping` 位置，默认为启用，仅在自动模式下有效。（Cookie储存） 这种情况下自动放置忽略 range距离和高度height设置        |
| `!def_range`    | 设置放置标记的距离，范围为50-2000。（Cookie储存）                                                 |
| `!def_height`   | 设置放置标记的高度，范围为20-500。（Cookie储存）                                                 |
| `!defl`         | 同 `!def`，但图标会跟随头顶。                                                                     |
