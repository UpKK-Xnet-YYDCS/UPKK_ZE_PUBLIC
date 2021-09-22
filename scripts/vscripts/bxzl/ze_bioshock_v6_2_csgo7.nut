insect1 <- null;
insect2 <- null;
insect3 <- null;

electro1 <- null;
electro2 <- null;
electro3 <- null;

incinerate1 <- null;
incinerate2 <- null;
incinerate3 <- null;

cyclone1 <- null;
cyclone2 <- null;
cyclone3 <- null;

little_sister <- null;
tonic_unstable <- null;
tonic_static <- null;

gravity1 <- null;
gravity2 <- null;
gravity3 <- null;

frost1 <- null;
frost2 <- null;
frost3 <- null;

big_daddy <- null;

spawnhudhint <- null;

function Text_Change_1()
{
		insect1 = Entities.FindByName(null,"plasmid_insect_text1");
		insect2 = Entities.FindByName(null,"plasmid_insect_text2");
		insect3 = Entities.FindByName(null,"plasmid_insect_text3");
		electro1 = Entities.FindByName(null,"plasmid_electro_text1");
		electro2 = Entities.FindByName(null,"plasmid_electro_text2");
		electro3 = Entities.FindByName(null,"plasmid_electro_text3");
		incinerate1 = Entities.FindByName(null,"plasmid_incinerate_text1");
		incinerate2 = Entities.FindByName(null,"plasmid_incinerate_text2");
		incinerate3 = Entities.FindByName(null,"plasmid_incinerate_text3");
		cyclone1 = Entities.FindByName(null,"plasmid_cyclone_text1");
		cyclone2 = Entities.FindByName(null,"plasmid_cyclone_text2");
		cyclone3 = Entities.FindByName(null,"plasmid_cyclone_text3");
		little_sister = Entities.FindByName(null,"little_sister_pickup_text");
		tonic_unstable = Entities.FindByName(null,"tonic_unstable_text");
		tonic_static = Entities.FindByName(null,"tonic_static_text");
		gravity1 = Entities.FindByName(null,"plasmid_gravity_text1");
		gravity2 = Entities.FindByName(null,"plasmid_gravity_text2");
		gravity3 = Entities.FindByName(null,"plasmid_gravity_text3");
		frost1 = Entities.FindByName(null,"plasmid_frost_text1");
		frost2 = Entities.FindByName(null,"plasmid_frost_text2");
		frost3 = Entities.FindByName(null,"plasmid_frost_text3");
		big_daddy = Entities.FindByName(null,"big_daddy_pickup_text");	
		if( (insect1 != null) && (insect1.GetClassname() == "game_text") )
		{
			insect1.__KeyValueFromString("message", "质粒: 虫群1级\n效果：以一大群蜜蜂对前进碰到的目标造成少量伤害\n次数：5次（简单难度）/3次（困难难度）\n冷却时间：10秒 ");
		}
		if( (insect2 != null) && (insect2.GetClassname() == "game_text") )
		{
			insect2.__KeyValueFromString("message", "质粒: 虫群2级\n效果：以一大群蜜蜂对前进碰到的目标造成中量伤害\n次数：5次（简单难度）/3次（困难难度）\n冷却时间：10秒 ");
		}
		if( (insect3 != null) && (insect3.GetClassname() == "game_text") )
		{
			insect3.__KeyValueFromString("message", "质粒: 虫群3级\n效果：以一大群蜜蜂对前进碰到的目标造成大量伤害\n次数：5次（简单难度）/3次（困难难度）\n冷却时间：10秒 ");
		}
		if( (electro1 != null) && (electro1.GetClassname() == "game_text") )
		{
			electro1.__KeyValueFromString("message", "质粒: 闪电1级\n效果：以一道闪电对目标造成眩晕\n持续：4秒\n次数：6次（简单难度）/4次（困难难度）\n冷却时间：11秒 ");
		}
		if( (electro2 != null) && (electro2.GetClassname() == "game_text") )
		{
			electro2.__KeyValueFromString("message", "质粒: 闪电2级\n效果：以数道闪电对目标造成眩晕\n持续：4秒\n次数：6次（简单难度）/4次（困难难度）\n冷却时间：11秒 ");
		}
		if( (electro3 != null) && (electro3.GetClassname() == "game_text") )
		{
			electro3.__KeyValueFromString("message", "质粒: 闪电3级\n效果：召唤闪电云释放闪电目标造成眩晕\n持续：7秒\n次数：6次（简单难度）/4次（困难难度）\n冷却时间：11秒 ");
		}
		if( (incinerate1 != null) && (incinerate1.GetClassname() == "game_text") )
		{
			incinerate1.__KeyValueFromString("message", "质粒: 焚化1级\n效果：释放火球将目标点燃\n持续：7秒\n次数：8次（简单难度）/5次（困难难度）\n冷却时间：5秒 ");
		}
		if( (incinerate2 != null) && (incinerate2.GetClassname() == "game_text") )
		{
			incinerate2.__KeyValueFromString("message", "质粒: 焚化2级\n效果：释放火球将目标点燃\n持续：7秒\n次数：8次（简单难度）/5次（困难难度）\n冷却时间：5秒 ");
		}
		if( (incinerate3 != null) && (incinerate3.GetClassname() == "game_text") )
		{
			incinerate3.__KeyValueFromString("message", "质粒: 焚化3级\n效果：释放一堵火墙\n持续：7秒\n次数：8次（简单难度）/5次（困难难度）\n冷却时间：5秒 ");
		}
		if( (cyclone1 != null) && (cyclone1.GetClassname() == "game_text") )
		{
			cyclone1.__KeyValueFromString("message", "质粒: 音爆1级\n效果：用声波将目标击远\n持续：2秒\n次数：8次（简单难度）/5次（困难难度）\n冷却时间：10秒 ");
		}
		if( (cyclone2 != null) && (cyclone2.GetClassname() == "game_text") )
		{
			cyclone2.__KeyValueFromString("message", "质粒: 音爆2级\n效果：用一股剧烈的声波将目标击远\n持续：2秒\n次数：8次（简单难度）/5次（困难难度）\n冷却时间：10秒 ");
		}
		if( (cyclone3 != null) && (cyclone3.GetClassname() == "game_text") )
		{
			cyclone3.__KeyValueFromString("message", "质粒: 音爆3级\n效果：用龙卷风将目标击远\n持续：2秒\n次数：8次（简单难度）/5次（困难难度）\n冷却时间：10秒 ");
		}
		if( (little_sister != null) && (little_sister.GetClassname() == "game_text") )
		{
			little_sister.__KeyValueFromString("message", "小妹妹\n拥有通过从尸体中收集Adam来给予自身及周围的队友速度增益的Buff\n站在发紫光的尸体上以获得Adam\n收集的尸体越多，速度增益效果越强\n呆在大老爹旁边，不然你会变得很脆弱");
		}
		if( (tonic_unstable != null) && (tonic_unstable.GetClassname() == "game_text") )
		{
			tonic_unstable.__KeyValueFromString("message", "闪光弹\n你的身体充满了光！当你死亡时致盲敌人\n激活方式：触碰到变异体（僵尸）");
		}
		if( (tonic_static != null) && (tonic_static.GetClassname() == "game_text") )
		{
			tonic_static.__KeyValueFromString("message", "静电罩\n你的身体充满了电！当你死亡时电击眩晕敌人\n激活方式：触碰到变异体（僵尸）");
		}
		if( (gravity1 != null) && (gravity1.GetClassname() == "game_text") )
		{
			gravity1.__KeyValueFromString("message", "质粒: 重力井1级\n效果：用敌人吸入洞中\n持续：5秒\n次数：5次（简单难度）/3次（困难难度）\n1999模式下为地图自带默认次数4次\n冷却时间：18秒 ");
		}
		if( (gravity2 != null) && (gravity2.GetClassname() == "game_text") )
		{
			gravity2.__KeyValueFromString("message", "质粒: 重力井2级\n效果：用敌人吸入湮灭中\n持续：6秒\n次数：5次（简单难度）/3次（困难难度）\n1999模式下为地图自带默认次数4次\n冷却时间：18秒 ");
		}
		if( (gravity3 != null) && (gravity3.GetClassname() == "game_text") )
		{
			gravity3.__KeyValueFromString("message", "质粒: 重力井3级\n效果：用敌人吸入移动的黑洞中\n持续：7秒\n次数：5次（简单难度）/3次（困难难度）\n1999模式下为地图自带默认次数4次\n冷却时间：18秒 ");
		}
		if( (frost1 != null) && (frost1.GetClassname() == "game_text") )
		{
			frost1.__KeyValueFromString("message", "质粒: 冰霜1级\n效果：冰住敌人\n持续：3秒\n次数：5次（简单难度）/3次（困难难度）\n冷却时间：13秒 ");
		}
		if( (frost2 != null) && (frost2.GetClassname() == "game_text") )
		{
			frost2.__KeyValueFromString("message", "质粒: 冰霜2级\n效果：冻结敌人\n持续：3秒\n次数：5次（简单难度）/3次（困难难度）\n冷却时间：13秒 ");
		}
		if( (frost3 != null) && (frost3.GetClassname() == "game_text") )
		{
			frost3.__KeyValueFromString("message", "质粒: 冰霜3级\n效果：冰住并粉碎敌人\n持续：3秒\n次数：5次（简单难度）/3次（困难难度）\n冷却时间：18秒 ");
		}
		if( (big_daddy != null) && (big_daddy.GetClassname() == "game_text") )
		{
			big_daddy.__KeyValueFromString("message", "大老爹\n你的任务就是呆在小妹妹旁边\n你在小妹妹旁边的话，她将会是不死的");
		}
}

function Text_Change_2()
{
		spawnhudhint = Entities.FindByName(null,"spawn_hudhint");	
		if( (spawnhudhint != null) && (spawnhudhint.GetClassname() == "game_text") )
		{
			spawnhudhint.__KeyValueFromString("message", "1999模式\n恭喜你们已通关地图主要部分\n1999模式关卡是一个挑战关卡，它包含的前四关的大部分路线\n因此它将会是比较难的一关，并且大约需要20分钟通关\n那么预祝玩的开心，好运！");
		}
}
