| 客户端命令 | 描述 |
| --- | --- |
| `!ehud` | 允许玩家切换HUD（0 - 禁用，1 - 居中，2 - 警告，3 - 世界文本         默认为 0(不显示HUD) ） |
| `!ehud_pos` | 允许玩家更改HUD的位置 {X Y Z}（默认值: 50 50 50；最小值: -200.0；最大值: 200.0） |
| `!ehud_refresh` | 允许玩家更改滚动列表的时间间隔 {秒}（默认值: 3；最小值: 1；最大值: 10） |
| `!ehud_sheet` | 允许玩家更改列表中的项目数量 {个数}（默认值: 5；最小值: 1；最大值: 15） |
| `!eup` | 允许玩家启用 UsePriority {布尔值} |

`例如 !ehud 3`
`!ehud_pos 50 50 50`

## 神器显示配置
```
[
	{
		"Name": "",						//神器被拾起或丢弃时在左下角聊天栏显示的名称
		"ShortName": "",				//神器拾起后在hud显示的名称
		"Color": "{default}",					//聊天消息颜色 例如:{default},{darkred},{green},{white},{blue}
		"HammerID": 0,					//神器所对应weapon_实体的hammeruniqueid
		"GlowColor": [0,0,0,0],			//rgba,神器高亮颜色
		"Filter": "",            
		"BlockPickup": false,			//锁定拾起，无特殊情况填false
		"AllowTransfer": false,			//是否允许管理员传送该神器，皮肤神器和僵尸神器设置为false。
		"ForceDrop": false,				//允许神器落地，手枪神器填true，刀神器填false，这个参数服务器已经删除，实际不生效。
		"Chat": false,					//神器拾起或丢弃时聊天框提示
		"Hud": false,					//是否在hud显示
		"TriggerID": 0,					//设置一个被eban的玩家无法拾取神器的玩家触发的trigger，主要防止吞神器trigger导致正常玩家无法拾取。Trigger通常是绑定在神器的一个trigger_once或者trigger_multiple实体，该实体的io指向一个game_player_equip实体。
		"UsePriority": false,			//默认启用,可以禁用强制玩家按下特定神器上的按钮，如有bug请设置为false。
		"AbilityList": [				//神器属性配置
			{
				"Name": "",				//神器按钮的targetname
				"ButtonID": 0,			//神器按钮的hammeruniqueid
				"ButtonClass": "",		//神器按钮的classname，常见的有func_button，func_physbox，game_ui，注意game_ui由cs2fix插件扩展，Source 2不存在该实体
				"Chat_Uses": false,		//神器使用时聊天框提示(神器CD低于10秒请务必设置为false)
				"Mode": 0,				//神器冷却模式. 0 = 没有神器按钮, 1 = 神器有按钮，防E保护 2 = 冷却, 3 = 次数, 4 = 次数+冷却, 5 = 多次使用后进入冷却, 6 = max_counter - 达到最小值时停止, 7 = max_counter - 达到最大值时停止, 8 = 使用血量控制开/关的按钮
				"MaxUses": 0,			//最多使用次数，适用于mode 3,4,5
				"CoolDown": 0,			//冷却时间，适用于mode 2,4,5
				"Ignore": false,		//隐藏该神器属性
				"LockItem": false,		//锁定神器按钮
				"MathID": 0,			//math_counter的hammeruniqueid，适用于mode 6,7
				"MathNameFix": false	//修复 math_counter 的名称（使用标志：保留实体名称（不进行名称修复）->point_template/env_entity_maker），如果一关中生成多个相同的使用了math_counter控制CD的神器且hud显示不正确，比如狮子王的迷你机枪，那么请填true
			},
			{
				"Name": "",
				"ButtonID": 0,
				"ButtonClass": "game_ui::PressedAttack",	//神器按钮为game_ui的神器属性示例 ( game_ui实体用法请参考 https://github.com/Source2ZE/CS2Fixes/wiki/Custom-Mapping-Features#outputs 这里PressedAttack代表按下攻击键也就是鼠标左键来触发事件) 目前服务器缺少一个插件，神器按钮为game_ui的cd暂时无法显示。
				"Chat_Uses": false,
				"Mode": 0
				"MaxUses": 0,
				"CoolDown": 0,
				"Ignore": false,
				"LockItem": false,
				"MathID": 0,
				"MathNameFix": false
			}
		]
	}
]



[
	{
		"Name": "Quicksand",
		"ShortName": "Quicksand",
		"Color": "{blue}",
		"HammerID": 11145,
		"GlowColor": [0,0,255,255],
		"BlockPickup": false,
		"AllowTransfer": true,
		"ForceDrop": false,
		"Chat": true,
		"Hud": true,
		"TriggerID": 0,
		"UsePriority": true,
		"AbilityList": [
			{
				"Name": "Freeze",
				"ButtonID": 0,
				"ButtonClass": "func_button",
				"Filter": "$freeze_player",
				"Chat_Uses": true,
				"Mode": 2,
				"MaxUses": 0,
				"CoolDown": 60
			}
		]
	},
	{
		"Name": "Earth",
		"ShortName": "Earth",
		"Color": "{orange}",
		"HammerID": 11116,
		"GlowColor": [255,140,0,255],
		"BlockPickup": false,
		"AllowTransfer": true,
		"ForceDrop": false,
		"Chat": true,
		"Hud": true,
		"TriggerID": 0,
		"UsePriority": true,
		"AbilityList": [
			{
				"Name": "",
				"ButtonID": 0,
				"ButtonClass": "func_button",
				"Filter": "$item_fire",
				"Chat_Uses": true,
				"Mode": 2,
				"MaxUses": 0,
				"CoolDown": 60
			}
		]
	},
	{
		"Name": "Tornado",
		"ShortName": "Tornado",
		"Color": "{default}",
		"HammerID": 11162,
		"GlowColor": [255,255,255,255],
		"BlockPickup": false,
		"AllowTransfer": true,
		"ForceDrop": false,
		"Chat": true,
		"Hud": true,
		"TriggerID": 0,
		"UsePriority": true,
		"AbilityList": [
			{
				"Name": "",
				"ButtonID": 0,
				"ButtonClass": "func_button",
				"Filter": "$tornado_player",
				"Chat_Uses": true,
				"Mode": 2,
				"MaxUses": 0,
				"CoolDown": 60
			}
		]
	},
	{
		"Name": "Fire",
		"ShortName": "Fire",
		"Color": "{red}",
		"HammerID": 11184,
		"GlowColor": [255,30,30,255],
		"BlockPickup": false,
		"AllowTransfer": true,
		"ForceDrop": false,
		"Chat": true,
		"Hud": true,
		"TriggerID": 0,
		"UsePriority": true,
		"AbilityList": [
			{
				"Name": "",
				"ButtonID": 0,
				"ButtonClass": "func_button",
				"Filter": "$fire_player",
				"Chat_Uses": true,
				"Mode": 2,
				"MaxUses": 0,
				"CoolDown": 60
			}
		]
	},
	{
		"Name": "Heal",
		"ShortName": "Heal",
		"Color": "{default}",
		"HammerID": 11196,
		"GlowColor": [255,255,255,255],
		"BlockPickup": false,
		"AllowTransfer": true,
		"ForceDrop": false,
		"Chat": true,
		"Hud": true,
		"TriggerID": 0,
		"UsePriority": true,
		"AbilityList": [
			{
				"Name": "",
				"ButtonID": 0,
				"ButtonClass": "func_button",
				"Filter": "$heal_player",
				"Chat_Uses": true,
				"Mode": 2,
				"MaxUses": 0,
				"CoolDown": 60
			}
		]
	},
	{
		"Name": "SandStorm",
		"ShortName": "SandStorm",
		"Color": "{yellow}",
		"HammerID": 11127,
		"GlowColor": [199,223,7,255],
		"BlockPickup": false,
		"AllowTransfer": true,
		"ForceDrop": false,
		"Chat": true,
		"Hud": true,
		"TriggerID": 0,
		"UsePriority": true,
		"AbilityList": [
			{
				"Name": "Ultima",
				"ButtonID": 0,
				"ButtonClass": "func_button",
				"Filter": "$sandstorm_player",
				"Chat_Uses": true,
				"Mode": 4,
				"MaxUses": 1,
				"CoolDown": 1
			}
		]
	},
	{
		"Name": "Antlion",
		"ShortName": "Antlion",
		"Color": "{lime}",
		"HammerID": 11895,
		"GlowColor": [119,234,7,255],
		"BlockPickup": false,
		"AllowTransfer": false,
		"ForceDrop": true,
		"Chat": true,
		"Hud": true,
		"TriggerID": 0,
		"UsePriority": false,
		"AbilityList": [
			{
				"Name": "Attack",
				"ButtonID": 0,
				"ButtonClass": "game_ui::PressedAttack",
				"Filter": "$antlion_player",
				"Chat_Uses": false,
				"Mode": 2,
				"MaxUses": 0,
				"CoolDown": 2
			},
			{
				"Name": "Jump",
				"ButtonID": 0,
				"ButtonClass": "game_ui::PressedAttack2",
				"Filter": "$antlion_player",
				"Chat_Uses": true,
				"Mode": 2,
				"MaxUses": 0,
				"CoolDown": 40
			}
		]
	},
	{
		"Name": "[ZM]Dark",
		"ShortName": "[ZM]Dark",
		"Color": "{purple}",
		"HammerID": 11854,
		"GlowColor": [128,0,128,255],
		"BlockPickup": false,
		"AllowTransfer": false,
		"ForceDrop": true,
		"Chat": true,
		"Hud": true,
		"TriggerID": 0,
		"UsePriority": true,
		"AbilityList": [
			{
				"Name": "",
				"ButtonID": 0,
				"ButtonClass": "func_button",
				"Filter": "$zdark_zm_player",
				"Chat_Uses": true,
				"Mode": 2,
				"MaxUses": 0,
				"CoolDown": 60
			}
		]
	},
	{
		"Name": "[ZM]Fire",
		"ShortName": "[ZM]Fire",
		"Color": "{darkorange}",
		"HammerID": 11828,
		"GlowColor": [240,94,35,255],
		"BlockPickup": false,
		"AllowTransfer": false,
		"ForceDrop": true,
		"Chat": true,
		"Hud": true,
		"TriggerID": 0,
		"UsePriority": true,
		"AbilityList": [
			{
				"Name": "",
				"ButtonID": 0,
				"ButtonClass": "func_button",
				"Filter": "$zfirez_zm_player",
				"Chat_Uses": true,
				"Mode": 2,
				"MaxUses": 0,
				"CoolDown": 60
			}
		]
	}
]
```
