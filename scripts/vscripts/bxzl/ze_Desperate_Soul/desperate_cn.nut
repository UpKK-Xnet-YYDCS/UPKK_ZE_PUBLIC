function NithhoggHP()
{
	EntFire("Hogg_Hp", "SetText", "绝望之龙-尼德霍格 : "+self.GetHealth().tostring(), 0.00, null);
	EntFire("Hogg_Hp", "Display", "", 0.05, null);
	EntFireByHandle(self, "RunScriptCode", " NithhoggHP(); ", 0.10, null, null);
}

function SetHP(amount)
{
	EntFireByHandle(self,"SetHealth",amount.tostring(),0.00,null,null);
}

function DiabloHPa()
{
	EntFire("S1_Diablo_Hp_Text", "SetText", "幻象 : "+self.GetHealth().tostring(), 0.00, null);
	EntFire("S1_Diablo_Hp_Text", "Display", "", 0.05, null);
	EntFireByHandle(self, "RunScriptCode", " DiabloHPa(); ", 0.10, null, null);
}

function DiabloHPb()
{
	EntFire("Diablo_Hp", "SetText", "暗黑破坏神 : "+self.GetHealth().tostring(), 0.00, null);
	EntFire("Diablo_Hp", "Display", "", 0.05, null);
	EntFireByHandle(self, "RunScriptCode", " DiabloHPb(); ", 0.10, null, null);
}

function Mapinfo()
{
	EntFire("Map_Text","SetText","绝望之灵:异闻录 \n地图作者: Tenshi \n模型帮助: uuz & Yasaka & Tianli & Dakotec \n脚本帮助: SakuraAyi\n翻译: 冰雪葬泪",0.00,null);
	EntFire("Map_Text", "Display", "", 0.05, null);
}

function KaledaHP()
{
	EntFire("Kaleda_Hp", "SetText", "Kalada Grotto : "+self.GetHealth().tostring(), 0.00, null);
	EntFire("Kaleda_Hp", "Display", "", 0.05, null);
	EntFireByHandle(self, "RunScriptCode", " KaledaHP(); ", 0.10, null, null);
}

function Earthlystar_info()
{
	EntFire("Item_Earthly_Star_Text", "SetText", "神器: 地星 \n描述: 切刀状态按E在地面上放置一个地星, 它将会在20秒后自动爆炸 \n你也可以在放置之后切刀状态再次按E提前引爆它 \n效果: 在0-10秒之间引爆时,将范围内人类回复到300血,同时对僵尸造成4000伤害 \n在0-10秒之间引爆时，将范围内人类回复到450血,同时对僵尸造成8000伤害 \n最大持续时间: 20秒 \n冷却: 60秒" , 0.00, null);
}

function S2_BGM()
{
	EntFire("S2_Bgm_1_Lrc","SetText","Long ago, far away",0.64,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Lonely world",8.92,null);
	EntFire("S2_Bgm_1_Lrc","SetText","A silent gray",12.74,null);
	EntFire("S2_Bgm_1_Lrc","SetText","I walked alone",16.73,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Never knowing what lies ahead",19.58,null);
	EntFire("S2_Bgm_1_Lrc","SetText","And you",24.42,null);
	EntFire("S2_Bgm_1_Lrc","SetText","You gave me a light",27.27,null);
	EntFire("S2_Bgm_1_Lrc","SetText","So obscure",31.93,null);
	EntFire("S2_Bgm_1_Lrc","SetText","So naive",35.74,null);
	EntFire("S2_Bgm_1_Lrc","SetText","I was blind",39.58,null);
	EntFire("S2_Bgm_1_Lrc","SetText","And then you reached for me",43.41,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Broken heart",47.63,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Beating soundlessly",51.09,null);
	EntFire("S2_Bgm_1_Lrc","SetText","To life",55.39,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Once again",59.00,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Take my hand",63.03,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Take my soul",66.82,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Share with me",70.54,null);
	EntFire("S2_Bgm_1_Lrc","SetText","the fears in your mind",74.42,null);
	EntFire("S2_Bgm_1_Lrc","SetText","When you are facing a darkened night",79.41,null);
	EntFire("S2_Bgm_1_Lrc","SetText","And I",86.34,null);
	EntFire("S2_Bgm_1_Lrc","SetText","I'll be by your side",89.21,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Close your eyes",94.11,null);
	EntFire("S2_Bgm_1_Lrc","SetText","And hold your breath with me",97.83,null);
	EntFire("S2_Bgm_1_Lrc","SetText","We will dive",101.60,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Into a distant dream",105.49,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Beneath the waves",109.34,null);
	EntFire("S2_Bgm_1_Lrc","SetText","You have set me free",113.23,null);
	EntFire("S2_Bgm_1_Lrc","SetText","And now I see so differently",117.15,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Beyond a world of gray",124.90,null);
	EntFire("S2_Bgm_1_Lrc","SetText","But if time should tear us apart",136.55,null);
	EntFire("S2_Bgm_1_Lrc","SetText","and destiny falls into the deep azure",143.36,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Dry your tears and rest beside me now",151.98,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Like a prayer, our story goes on",159.74,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Don't let go",166.75,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Don't ever forget",170.40,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Forever you will be the light inside of me",174.21,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Dry your tears and rest beside me now",182.95,null);
	EntFire("S2_Bgm_1_Lrc","SetText","Like a prayer, the memory of you",190.72,null);
	EntFire("S2_Bgm_1_Lrc","SetText","will gently refrain again",197.45,null);
	EntFire("S2_Bgm_1_Lrc","Display","",0.66,null);
	EntFire("S2_Bgm_1_Lrc","Display","",8.94,null);
	EntFire("S2_Bgm_1_Lrc","Display","",12.76,null);
	EntFire("S2_Bgm_1_Lrc","Display","",16.75,null);
	EntFire("S2_Bgm_1_Lrc","Display","",19.60,null);
	EntFire("S2_Bgm_1_Lrc","Display","",24.44,null);
	EntFire("S2_Bgm_1_Lrc","Display","",27.29,null);
	EntFire("S2_Bgm_1_Lrc","Display","",31.95,null);
	EntFire("S2_Bgm_1_Lrc","Display","",35.76,null);
	EntFire("S2_Bgm_1_Lrc","Display","",39.60,null);
	EntFire("S2_Bgm_1_Lrc","Display","",43.43,null);
	EntFire("S2_Bgm_1_Lrc","Display","",47.65,null);
	EntFire("S2_Bgm_1_Lrc","Display","",51.11,null);
	EntFire("S2_Bgm_1_Lrc","Display","",55.41,null);
	EntFire("S2_Bgm_1_Lrc","Display","",59.02,null);
	EntFire("S2_Bgm_1_Lrc","Display","",63.05,null);
	EntFire("S2_Bgm_1_Lrc","Display","",66.84,null);
	EntFire("S2_Bgm_1_Lrc","Display","",70.56,null);
	EntFire("S2_Bgm_1_Lrc","Display","",74.44,null);
	EntFire("S2_Bgm_1_Lrc","Display","",79.43,null);
	EntFire("S2_Bgm_1_Lrc","Display","",86.36,null);
	EntFire("S2_Bgm_1_Lrc","Display","",89.23,null);
	EntFire("S2_Bgm_1_Lrc","Display","",94.13,null);
	EntFire("S2_Bgm_1_Lrc","Display","",97.85,null);
	EntFire("S2_Bgm_1_Lrc","Display","",101.62,null);
	EntFire("S2_Bgm_1_Lrc","Display","",105.51,null);
	EntFire("S2_Bgm_1_Lrc","Display","",109.36,null);
	EntFire("S2_Bgm_1_Lrc","Display","",113.25,null);
	EntFire("S2_Bgm_1_Lrc","Display","",117.17,null);
	EntFire("S2_Bgm_1_Lrc","Display","",124.92,null);
	EntFire("S2_Bgm_1_Lrc","Display","",136.57,null);
	EntFire("S2_Bgm_1_Lrc","Display","",143.38,null);
	EntFire("S2_Bgm_1_Lrc","Display","",152.00,null);
	EntFire("S2_Bgm_1_Lrc","Display","",159.76,null);
	EntFire("S2_Bgm_1_Lrc","Display","",166.77,null);
	EntFire("S2_Bgm_1_Lrc","Display","",170.42,null);
	EntFire("S2_Bgm_1_Lrc","Display","",174.23,null);
	EntFire("S2_Bgm_1_Lrc","Display","",182.97,null);
	EntFire("S2_Bgm_1_Lrc","Display","",190.74,null);
	EntFire("S2_Bgm_1_Lrc","Display","",197.47,null);
}
