# CS2-MapText
## 配置
``` 
{   
	"地图原始文本":{
		"translation": "翻译文本不翻译请留空"
	},
	"[NORMAL MODE]":{
		"translation": "**普通难度[NORMAL]**"
	},
	"** Defend untill the guards open the airport. **":{
		"translation": "**坚守至守卫将机场开放**",
		"Blocked": true
	}
}
```
## 可选参数
| 关键词 | 默认值|说明                                                                       |
|----------|-----|:----------------------------------------------------------------------------:|
| DoorCountDown  | 0 |手动设置倒计时 0 = 自动监听  -1 = 禁用自动监听  |
| Blocked  | false |设置成true则屏蔽该文本输出  |
| ClearTimer  | false |设置成true则在输出本文本时清空现有倒计时(可用于限时打死BOSS 打死BOSS后倒计时还在计时)  |
---

