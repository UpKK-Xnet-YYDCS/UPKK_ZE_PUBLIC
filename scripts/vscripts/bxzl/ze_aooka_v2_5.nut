bxzl_text <- null;
bxzl_firstline_time <- 0.0;
bxzl_secondline_time   <-  0.0;
bxzl_thirdline_time <- 0.0;
bxzl_fourthline_time <- 0.0;
bxzl_firstline_text  <-  "";
bxzl_secondline_text <-  "";
bxzl_thirdline_text <-  "";
bxzl_fourthline_text <-  "";
idx_time  <- 0.0;

Bxzl_Item_Water_Gametext <- null;
Bxzl_Item_Gold_Gametext <- null;
Bxzl_Item_Electro_Gametext <- null;
Bxzl_Item_Wind_Gametext <- null;
Bxzl_Item_Fire_Gametext <- null;
Bxzl_Item_Heal_Gametext <- null;
Bxzl_Item_Ice_Gametext <- null;
Bxzl_Item_Ammo_Gametext <- null;
Bxzl_Item_Help_Gametext <- null;

Bxzl_Item_Zshield_Gametext <- null;
Bxzl_Item_Zbgold_Gametext <- null;
Bxzl_Item_Zice_Gametext <- null;
Bxzl_Item_Zgravity_Gametext <- null;
Bxzl_Item_Zfire_Gametext <- null;
Bxzl_Item_Zwarp_Gametext <- null;
Bxzl_Item_Zgravity2_Gametext <- null;

bxzl_text_array <- [
    { 
        array_message="落星陨芒 - 开奶硬抗或者用金轮消除 - BOSS战开始和结束时释放"
        array_holdtime=5.0
    },//0

    {
        array_message="聚魂引 - 僵尸传送至BOSS正下方 - BOSS战开始后每隔90秒释放"
        array_holdtime=5.0
    },//1

    { 
        array_message="魂出电入 - 地面深色区域火焰伤害\n面对小地图箭头前后方向,去两边没有球状闪电的安全区"
        array_holdtime=5.0
    },//2

    { 
        array_message="锁星 - BOSS反伤(提前去BOSS正下方,下个技能必定解星)"
        array_holdtime=5.0
    },//3

    { 
        array_message="解星 - 全屏伤害,去BOSS正下方"
        array_holdtime=2.0
    },//4

    { 
        array_message="星夜问灵 - BOSS回血(提前蹲下,下个技能必定天罚非罪)"
        array_holdtime=3.0
    },//5

    { 
        array_message="天罚非罪 - 蹲下,上范围的伤害"
        array_holdtime=2.0
    },//6

    { 
        array_message="月离于毕 - 头顶九宫格天坠"
        array_holdtime=5.0
    },//7

    { 
        array_message="诸魂雁镇 - 场地三魂色伤害"
        array_holdtime=5.0
    },//8

    { 
        array_message="红 紫 绿 - 去白色区域"
        array_holdtime=4.0
    },//9

    { 
        array_message="白 紫 绿 - 去红色区域"
        array_holdtime=4.0
    },//10

    { 
        array_message="红 白 绿 - 去紫色区域"
        array_holdtime=4.0
    },//11

    { 
        array_message="红 紫 白 - 去绿色区域"
        array_holdtime=4.0
    },//12
    { 
        array_message="有玩家跳上了冰神器的平台，触发5秒后的僵尸传送,同时后面第二道门开启"
        array_holdtime=0.5
    },//13
    { 
        array_message="有玩家跳上了冰神器的平台，触发4秒后的僵尸传送,同时后面第二道门开启"
        array_holdtime=0.5
    },//14
    { 
        array_message="有玩家跳上了冰神器的平台，触发3秒后的僵尸传送,同时后面第二道门开启"
        array_holdtime=0.5
    },//15
    { 
        array_message="有玩家跳上了冰神器的平台，触发2秒后的僵尸传送,同时后面第二道门开启"
        array_holdtime=0.5
    },//16
    { 
        array_message="有玩家跳上了冰神器的平台，触发1秒后的僵尸传送,同时后面第二道门开启"
        array_holdtime=0.5
    },//17
    { 
        array_message="有玩家跳上了冰神器的平台，触发僵尸传送,同时后面第二道门开启"
        array_holdtime=0.5
    },//18
    { 
        array_message="script by bxzl on 2021.07.04"
        array_holdtime=5
    },//19
    { 
        array_message="改动一 增加神器拾取提示"
        array_holdtime=5
    },//20
    { 
        array_message="改动二 增加第三关BOSS技能详细提示"
        array_holdtime=5
    },//21
];

function Say_ScriptDate()
{
    bxzl_text = Entities.FindByName(null,"bxzl_text");
    Bxzl_Item_Water_Gametext = Entities.FindByName(null,"Bxzl_Item_Water_Gametext");
    Bxzl_Item_Gold_Gametext = Entities.FindByName(null,"Bxzl_Item_Gold_Gametext");
    Bxzl_Item_Electro_Gametext = Entities.FindByName(null,"Bxzl_Item_Electro_Gametext");
    Bxzl_Item_Wind_Gametext = Entities.FindByName(null,"Bxzl_Item_Wind_Gametext");
    Bxzl_Item_Fire_Gametext = Entities.FindByName(null,"Bxzl_Item_Fire_Gametext");
    Bxzl_Item_Heal_Gametext = Entities.FindByName(null,"Bxzl_Item_Heal_Gametext");
    Bxzl_Item_Ice_Gametext = Entities.FindByName(null,"Bxzl_Item_Ice_Gametext");
    Bxzl_Item_Ammo_Gametext = Entities.FindByName(null,"Bxzl_Item_Ammo_Gametext");
    Bxzl_Item_Help_Gametext = Entities.FindByName(null,"Bxzl_Item_Help_Gametext");
    Bxzl_Item_Zshield_Gametext = Entities.FindByName(null,"Bxzl_Item_Zshield_Gametext");
    Bxzl_Item_Zbgold_Gametext = Entities.FindByName(null,"Bxzl_Item_Zbgold_Gametext");
    Bxzl_Item_Zice_Gametext = Entities.FindByName(null,"Bxzl_Item_Zice_Gametext");
    Bxzl_Item_Zgravity_Gametext = Entities.FindByName(null,"Bxzl_Item_Zgravity_Gametext");
    Bxzl_Item_Zfire_Gametext = Entities.FindByName(null,"Bxzl_Item_Zfire_Gametext");
    Bxzl_Item_Zwarp_Gametext = Entities.FindByName(null,"Bxzl_Item_Zwarp_Gametext");
    Bxzl_Item_Zgravity2_Gametext = Entities.FindByName(null,"Bxzl_Item_Zgravity2_Gametext");
    EntFire("cmd","Command","say script by bxzl on 2021.07.04",0.00,null);
    EntFire("cmd","Command","改动一 增加神器拾取时候提示",1.00,null);
}

function Set_ItemText()
{
    if (Bxzl_Item_Water_Gametext != null)
    {
        Bxzl_Item_Water_Gametext.__KeyValueFromString("message", "水神器\n按E使用时在持有者正面生成一个跟随直线推力水\n推开僵尸\n若此时使用电神器,水将附带减速效果\n持续时间: 7秒\n用水神器的时候会将人类火神器的效果清除\n能对第二、三、四关BOSS造成300点伤害");
    }
    if (Bxzl_Item_Gold_Gametext != null)
    {
        Bxzl_Item_Gold_Gametext.__KeyValueFromString("message", "金轮神器\n按E使用时在正面生成一个固定隐形圆柱形墙\n持续时间: 7秒或者墙被僵尸挠碎\n第三关BOSS战时使用能消除落星陨芒的效果");
    }
    if (Bxzl_Item_Electro_Gametext != null)
    {
        Bxzl_Item_Electro_Gametext.__KeyValueFromString("message", "电神器\n按E使用时在持有者正面生成一个跟随直线电光\n减速僵尸\n在使用水或者火神器时使用电神器能增加对应神器效果\n持续时间: 3秒\n能对第二、三、四关BOSS造成75点伤害");
    }
    if (Bxzl_Item_Wind_Gametext != null)
    {
        Bxzl_Item_Wind_Gametext.__KeyValueFromString("message", "风神器\n按E使用时在持有者周围形成跟随环形风\n推开僵尸\n持续时间: 7秒");
    }
    if (Bxzl_Item_Fire_Gametext != null)
    {
        Bxzl_Item_Fire_Gametext.__KeyValueFromString("message", "火神器\n按E使用时在正前方生成固定圆形火圈\n燃烧并伤害僵尸\n若此时使用电神器,火将附带电效果\n持续时间: 7秒\n用火神器的时候会将人类冰神器的效果清除\n能对第二、三、四关BOSS造成300点伤害");
    }
    if (Bxzl_Item_Heal_Gametext != null)
    {
        Bxzl_Item_Heal_Gametext.__KeyValueFromString("message", "奶神器\n按E使用时在持有者周围形成跟随治疗圈\n将人类恢复到250血和给与在奶里人类的防抓效果\n持续时间: 5秒");
    }
    if (Bxzl_Item_Ice_Gametext != null)
    {
        Bxzl_Item_Ice_Gametext.__KeyValueFromString("message", "冰神器\n按E使用时在持有者周围生成固定冰圈,冻住僵尸\n持续时间: 7秒\n能对第二、三、四关BOSS造成300点伤害");
    }
    if (Bxzl_Item_Ammo_Gametext != null)
    {
        Bxzl_Item_Ammo_Gametext.__KeyValueFromString("message", "弹药神器\n按E使用时在持有者周围形成跟随弹药补给圈\n持续时间: 10秒");
    }
    if (Bxzl_Item_Help_Gametext != null)
    {
        Bxzl_Item_Help_Gametext.__KeyValueFromString("message", "求救神器\n按E使用时持有者单人1.5倍加速和免疫僵尸\n持续时间: 4秒");
    }

    if (Bxzl_Item_Zshield_Gametext != null)
    {
        Bxzl_Item_Zshield_Gametext.__KeyValueFromString("message", "僵尸护盾神器\n按E使用时在持有者周围跟随圆柱形护盾\n无视人类的子弹高爆伤害,同时反伤射击的人类\n持续时间: 5秒");
    }
    if (Bxzl_Item_Zbgold_Gametext != null)
    {
        Bxzl_Item_Zbgold_Gametext.__KeyValueFromString("message", "僵尸破坏金轮神器\n按E使用时将人类正在生效的金轮神器破坏\n同时给与持有者2.5倍的加速效果\n右键在原地生成一个加速带\n持续时间: 破坏效果瞬间,按E加速效果5秒");
    }
    if (Bxzl_Item_Zice_Gametext != null)
    {
        Bxzl_Item_Zice_Gametext.__KeyValueFromString("message", "僵尸冰神器\n按E使用时冻住持有者正前方的人类3秒\n右键使用时发射出一个移动的冰球,冻住触碰的人类\n持续时间: 按E技能0.5秒");
    }
    if (Bxzl_Item_Zgravity_Gametext != null)
    {
        Bxzl_Item_Zgravity_Gametext.__KeyValueFromString("message", "僵尸黑洞神器\n按E使用时吸引住持有者正前方的人类\n持续时间: 5秒");
    }
    if (Bxzl_Item_Zfire_Gametext != null)
    {
        Bxzl_Item_Zfire_Gametext.__KeyValueFromString("message", "僵尸火神器\n按E使用时燃烧持有者正前方的人类6秒\n右键使用时发射出一个移动的火球,燃烧触碰的人类\n持续时间: 按E技能0.5秒");
    }
    if (Bxzl_Item_Zwarp_Gametext != null)
    {
        Bxzl_Item_Zwarp_Gametext.__KeyValueFromString("message", "僵尸秒杀神器\n按E使用时秒杀持有者正前方的人类\n持续时间: 0.5秒");
    }
    if (Bxzl_Item_Zgravity2_Gametext != null)
    {
        Bxzl_Item_Zgravity2_Gametext.__KeyValueFromString("message", "僵尸黑洞球\n按E使用时直线发出一个黑洞球,吸住周围的人类\n并一段时间后返回初始点");
    }
}

function Bxzl_DisplayText(bxzl_displaytime) 
{    
    local bxzl_message = "";
	if (bxzl_text == null)
    {
        return;
    }
    if (bxzl_displaytime>0.0)
    {
        if (bxzl_firstline_text=="" && bxzl_secondline_text=="" && bxzl_thirdline_text=="" && bxzl_fourthline_text=="" )
        {
            EntFire("cmd","Command","say 1215",0.00,null);
            return;
        }
        bxzl_message = bxzl_firstline_text.tostring() + "\n" + bxzl_secondline_text.tostring() + "\n" + bxzl_thirdline_text.tostring() + "\n" + bxzl_fourthline_text.tostring();
        bxzl_text.__KeyValueFromString("message", bxzl_message);
        EntFireByHandle(bxzl_text, "Display", "", 0, bxzl_text, bxzl_text);
        bxzl_displaytime = bxzl_displaytime - 0.1;
        EntFireByHandle(self,"RunScriptCode","Bxzl_DisplayText(" + bxzl_displaytime + ")",0.1,null,null);
    }
}

function Bxzl_SetText(bxzl_idx)
{
    if (bxzl_firstline_text == "")
    {
        bxzl_firstline_text = bxzl_text_array[bxzl_idx].array_message;
        idx_time = bxzl_text_array[bxzl_idx].array_holdtime;
        EntFireByHandle(self, "RunScriptCode", "Bxzl_DisplayText(idx_time);", 0.00, null, null);
        EntFireByHandle(self,"RunScriptCode","bxzl_firstline_text="+"\""+"\"",idx_time+0.4,null,null);
    }
    else if (bxzl_secondline_text == "")
    {
        bxzl_secondline_text = bxzl_text_array[bxzl_idx].array_message;
        idx_time = bxzl_text_array[bxzl_idx].array_holdtime;
        EntFireByHandle(self, "RunScriptCode", "Bxzl_DisplayText(idx_time);", 0.00, null, null);
        EntFireByHandle(self,"RunScriptCode","bxzl_secondline_text="+"\""+"\"",idx_time+0.4,null,null);
    }
    else if (bxzl_thirdline_text == "")
    {
        bxzl_thirdline_text = bxzl_text_array[bxzl_idx].array_message;
        idx_time = bxzl_text_array[bxzl_idx].array_holdtime;
        EntFireByHandle(self, "RunScriptCode", "Bxzl_DisplayText(idx_time);", 0.00, null, null);
        EntFireByHandle(self,"RunScriptCode","bxzl_thirdline_text="+"\""+"\"",idx_time+0.4,null,null);      
    }
    else if (bxzl_fourthline_text == "")
    {
        bxzl_fourthline_text = bxzl_text_array[bxzl_idx].array_message;
        idx_time = bxzl_text_array[bxzl_idx].array_holdtime;
        EntFireByHandle(self, "RunScriptCode", "Bxzl_DisplayText(idx_time);", 0.00, null, null);
        EntFireByHandle(self,"RunScriptCode","bxzl_fourthline_text="+"\""+"\"",idx_time+0.4,null,null);        
    }
}
