# 增加格式写法说明

| Key             | Value                          | Comment                                        |
|-----------------|--------------------------------|------------------------------------------------|
| workshop_id     | 3274462953                      | ID for the map workshop                       |
| enabled         | 1                              | 1 开启 0 禁用                                  |
| filename        | ze_p_v_z                        | 地图文件名                                     |
| RestrictedTimes | 08:00-12:00;14:00-23:00         | 禁用时间段 支持多个 (即不在这些时间段都可以玩) |
| MinPlayers      | 16                             | 最低需要玩家                                   |
| search          | "植物;pvz"                       | 预定搜索多关键词                               |


```plaintext
	"ze_p_v_z"
	{
		"workshop_id"		"3274462953"
		"enabled"		"1"
		"filename"		"ze_p_v_z"
		"updatedname"		"ze_p_v_z"
		"search"		"植物;pvz"
        "RestrictedTimes" "01:00-06:00;14:00-23:50"
	}
```
