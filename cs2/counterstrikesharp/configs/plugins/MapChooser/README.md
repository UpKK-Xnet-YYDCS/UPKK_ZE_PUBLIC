
# 地图配置 [MapChooser](https://github.com/UpKK-Xnet-YYDCS/UPKK_ZE_PUBLIC/blob/master/cs2/counterstrikesharp/configs/plugins/MapChooser)


| Key             | Value                          | Comment                                        |
|-----------------|--------------------------------|------------------------------------------------|
| workshop_id     | 3274462953                      | ID for the map workshop                       |
| enabled         | 1                              | 1 开启 0 禁用                                  |
| filename        | ze_p_v_z                        | 地图文件名                                     |
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


## Console Command 列表与注释

| Console Command               | 用途说明                                      | 备注                                | 所需权限                    |
|-------------------------------|-----------------------------------------------|-------------------------------------|-----------------------------|
| `css_rtv`                     | 玩家发起 RTV 投票（换图投票）                  | 仅限客户端使用                      | 无权限要求                   |
| `css_unrtv`                   | 玩家取消 RTV 投票                              | 仅限客户端使用                      | 无权限要求                   |
| `css_nominate` / `css_yd`     | 玩家提名一个地图作为下次投票选项                | 仅限客户端使用                      | 无权限要求                   |
| `css_force_mapvote`           | 强制启动地图投票                              |                                    | 需要管理员权限 `@css/ban`     |
| `css_debug_votemaplist`       | 输出当前可用于投票的地图列表                    |                                    | 需要管理员权限 `@css/ban`     |
| `css_force_rtv`               | 强制启动 RTV 换图投票                          |                                    | 需要管理员权限 `@css/ban`     |
| `css_random_map`              | 随机切换地图                                  |                                    | 需要管理员权限 `@css/ban`     |
| `css_update_ws`               | 更新服务器 Workshop 地图                      |需要ID参数                          | 需要管理员权限 `@css/ban`     |
| `css_reload_maplist`          | 重新加载地图列表                               |                                    | 需要管理员权限 `@css/ban`     |
| `css_clean_crashmaprecover`   | 清空崩溃恢复文件（crash map recover 文件）      |                                    | 需要管理员权限 `@css/ban`     |
| `css_mapinfo`                 | 显示当前地图信息                               | 仅限客户端使用                      | 无权限要求                   |

### Console Command 详细说明

- **`css_rtv`**: 
  - 用途: 玩家发起 RTV (Rock the Vote) 换图投票。
  - 仅限客户端使用，如果玩家投票成功并达到要求票数，则会启动换图流程。
  - 权限要求: 无。

- **`css_unrtv`**: 
  - 用途: 玩家取消自己发起的 RTV 投票。
  - 仅限客户端使用。
  - 权限要求: 无。

- **`css_nominate` / `css_yd`**: 
  - 用途: 玩家提名一个地图加入下次地图投票选项中。
  - 仅限客户端使用。
  - 权限要求: 无。

- **`css_force_mapvote`**: 
  - 用途: 管理员强制启动地图投票。
  - 权限要求: 需要管理员权限 `@css/ban`。

- **`css_debug_votemaplist`**: 
  - 用途: 输出当前可用于投票的地图列表。
  - 权限要求: 需要管理员权限 `@css/ban`。

- **`css_force_rtv`**: 
  - 用途: 管理员强制启动 RTV 换图投票。
  - 权限要求: 需要管理员权限 `@css/ban`。

- **`css_random_map`**: 
  - 用途: 管理员随机切换地图。
  - 权限要求: 需要管理员权限 `@css/ban`。

- **`css_update_ws`**: 
  - 用途: 管理员更新工作坊订阅的地图。
  - 权限要求: 需要管理员权限 `@css/ban`。

- **`css_reload_maplist`**: 
  - 用途: 重新加载地图列表。
  - 权限要求: 需要管理员权限 `@css/ban`。

- **`css_clean_crashmaprecover`**: 
  - 用途: 清空崩溃恢复文件。
  - 权限要求: 需要管理员权限 `@css/ban`。

- **`css_mapinfo`**: 
  - 用途: 显示当前地图的信息。
  - 仅限客户端使用。
  - 权限要求: 无。
