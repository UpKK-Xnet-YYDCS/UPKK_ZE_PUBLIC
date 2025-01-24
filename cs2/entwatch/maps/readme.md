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
    "Name": "",						//出现在聊天框的神器名称
    "ShortName": "",					//出现在HUD的神器名称
    "Color": "{default}",						//神器提示在聊天框中的颜色 例如:{default},{darkred},{green},{white},{blue}
    "HammerID": 0,					//武器实体的hammerid
    "GlowColor": [0,0,0,0],					//神器高亮的颜色和透明度，R,G,B参数取值范围在0-255之间且为非负整数，第四个参数A为透明度，取值范围在0.0-1.0之间
    "BlockPickup": false,					//是否锁定神器拾取，默认填false
    "AllowTransfer": true,					//是否允许管理员传送该神器，刀神器填false
    "ForceDrop": true,					//允许神器落地，手枪神器填true，刀神器填false
    "Chat": true,					//神器使用时是否在聊天框中提示
    "Hud": true,					//神器是否在HUD显示
    "TriggerID": 0,					//与该神器相关的触发实体的hammerid
    "UsePriority": false,					//玩家按E时，插件会额外生成一个使用输入，防止在人群或其它场景中卡神器按钮，默认填true，机枪，燃料型神器填false
    "AbilityList": [				//神器属性配置
      {
        "Name": "",				//神器按钮的targetname
        "ButtonID": 0,			//神器按钮的hammerid
        "ButtonClass": "",		//神器按钮的classname
        "Filter": "",           //神器按钮使用筛选器的名字，filter_activator_attribute_int实体的值为'$filterattribute'；filter_activator_context实体的值为'responsecontext:数字'；filter_activator_name实体的值为'filtername'
        "Chat_Uses": false,		//该神器属性使用时是否在聊天框中提示(CD低于10秒填false，防止聊天框刷屏)
        "Mode": 0,				//神器冷却模式. 0 = 无按钮, 1 = 仅防E神器 2 = 冷却, 3 = 次数, 4 = 次数+冷却, 5 = 多次使用后进入冷却, 6 = math_counter达到或低于最小值时触发(OnHitMin), 7 = math_counter达到或超过最大值时触发(OnHitMax), 8 = 有血量的按钮
        "MaxUses": 0,			//最多使用次数，适用于mode 3,4,5
        "CoolDown": 0,			//冷却时间，适用于mode 2,4,5
        "Ignore": false,		//当插件自动识别神器按钮错误时，填入true以隐藏神器属性。例如，使用func_physbox作为神器模型且其父级为武器的实体会被插件错误识别
        "LockItem": false,		//锁定神器按钮，默认填false
        "MathID": 0,			//math_counter的hammerid，适用于mode 6,7
        "MathNameFix": false,	//math_counter名称修正（使用source2viewer查询该实体的targetname，如果名称的格式为'名字&0000'，则填true；否则填false）
        "MathFindSpawned": false,	//武器生成后在地图上搜索math_counter（math_counter不在point_template中填true；否则填false）
        "MathDontShowMax": false	//不显示math_counter的最大值（燃料型/动态/固定次数型神器填true，机枪填false）
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
    "GlowColor": [0,255,0,1],
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
    "GlowColor": [0,255,0,1],
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
    "GlowColor": [0,255,0,1],
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
    "GlowColor": [0,255,0,1],
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
    "GlowColor": [0,255,0,1],
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