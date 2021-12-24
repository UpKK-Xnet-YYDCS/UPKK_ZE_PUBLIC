
# 地图区域说明

## 区域绘制要求

对于一般地图，需要画在回合结束时（僵尸处死后，弹出人类胜利图片）的人类可活动范围。
如果是僵尸触发会导致回合失败的地图，按照 `arrive_nozm_xxx` 的方式命名。



## 实例配置文件

	"mapbouns"
	{
		"RequestClients"		"32" //基本需要玩家数量 (不能低于20以下)
		"Rounds_HumanWin" 
		//触发规则 回合结束 队伍CT胜利 (最多配置30个回合 不得越界)
		//执行逻辑 【首先必须4项条件】 第一回合给30 第二回合给40 第三回合给 0 第4回合 延续第三回合....直到地图更换.
		//注意的是 回合顺序必须以位置为准 第一个位置代表第一回合 第二个位置代表第二回合 不是 123 key (key只是方便阅读)
		//如果不满足 下面4项条件 系统不会设置为第二回合
		{
			"1"
			{
				"round_time_need" "120" //至少需要 120秒才能触发奖励 防止ezwin策略
				"Rewared_Type" "" // 留空则没有 配置奖励 playerskin 随机公共人物皮肤 playerskin_advance !task 月抽奖可能得到的皮肤 [playerskin 公共人物皮肤 = 1~7天 playerskin_advance 高级人物皮肤 = 30天]
				"Rewared_Note" "注释说明"
				"point" "30" //积分点数 0 则不给积分
				 //zone_name 防ezwin方案 需要玩家到指定区域名称才会给奖励 使用命令 sm_zones 画区域并命名 前缀必须是 arrive_ 完整如 arrive_1 但区域会占实体.
				 //未实施:【僵尸触碰会取消i奖励】
				 //每个地图区域名称必须唯一  arrive_1,arrive_2,arrive_3,...etc
				"zone_name"  ""
			}
			"2"
			{
				"round_time_need" "120" //至少需要 120秒才能触发奖励 防止ezwin策略
				"point" "40"
				"zone_name"  ""
			}
			"3"
			{
				"point" "0" //置点数为0 
			}
		}
	}
`

# 系统下移回合条件

**需要满足以下全部条件**

1.RequestClients (全局人数)
2.round_time_need(局部配置 需要的回合时间)
3.CT胜利
4.如配置了 "zone_name" 则必须有任何一位CT玩家达到指定区域
