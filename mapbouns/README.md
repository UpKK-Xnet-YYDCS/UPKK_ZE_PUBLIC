
	"mapbouns"
	{
		"RequestClients"		"32" //基本需要玩家数量 (不能低于20以下)
		"Rounds_HumanWin" 
		//触发规则 回合结束 队伍CT胜利 (最多配置30个回合 不得越界)
		//执行逻辑 【首先必须是CT队伍 Win】 第一回合给30 第二回合给40 第三回合给 0 第4回合 延续第三回合....直到地图更换.
		//
		{
			"1"
			{
				"round_time_need" "120" //至少需要 120秒才能触发奖励 防止ezwin策略
				"point" "30" //点数
				 //zone_name 防ezwin方案 需要玩家到指定区域名称才会给奖励 使用命令 sm_zones 画区域并命名 前缀必须是 arrive_ 完整如 arrive_1 可靠性增加 但区域会占实体
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
	# 系统如何下移回合?
	同时满足3个条件 
	1.RequestClients (全局人数)
	2.round_time_need(局部配置 需要的回合时间)
	3.CT胜利


