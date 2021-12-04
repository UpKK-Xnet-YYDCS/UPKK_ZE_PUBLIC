
	"mapbouns"
	{
		"RequestClients"		"32" //基本需要玩家数量 (不能低于20以下)
		"Rounds_HumanWin" 
		//触发规则 回合结束 队伍CT胜利 (最多配置30个回合 不得越界)   [如果 回合结束  当前玩家 < RequestClients 则 下回合仍然算未激活 不会从第一回合开始]
		//执行逻辑 第一回合给30 第二回合给40 第三回合给 0 第4回合 延续第三回合....直到地图更换.
		//
		{
			"1"
			{
				"round_time_need" "120" //至少需要 120秒才能触发奖励 防止ezwin策略
				"point" "30" //点数
				"console_output"  "" //检测say是否有输出文本才能激活 # 请务必确认在回合结束之前有输出 留空则不检测 *(暂不生效)
				"zone_name"  ""   //防ezwin方案 需要玩家到指定区域名称才会给奖励 sm_zones 画区域并命名 前缀 arrive_ 完整如 arrive_1 可靠性增加 但区域会占实体
			}
			"2"
			{
				"round_time_need" "120" //至少需要 120秒才能触发奖励 防止ezwin策略
				"point" "40"
				"console_output"  ""  //不需要检测控制台输出
				"zone_name"  ""
			}
			"3"
			{
				"point" "0" //置点数为0 
			}
		}
	}

`
