class cBoss{
	entity = null;
	name = null;
	timer_death = null;
	timer_show = null;
	type = null;
	hp = 0;
	hpbar = 0;
	constructor(_e,_n,_td,_ts,_tp){entity=_e;name=_n;timer_death=_td;timer_show=_ts;type=_tp;}
}

Bosses <- [];
iTShow <- 20;
iTShowDeath <- 7;
Tick <- false;
UpdateTime <- 0.5;
Bxzl_BossHP_Gametext <- null;

function Say_ScriptDate()
{
    Bxzl_BossHP_Gametext = Entities.FindByName(null,"Bxzl_BossHP_Gametext");
    EntFire("server","Command","say script by bxzl on 2021.06.27",0.00,null);
}

function AddBoss(iType)
{
	local nameboss = "Boss: ";
	local type_boss = 1; //1-counter, 2-breakable, 3-hpbar
	if(iType==1){ nameboss = "苦力怕娘: ";} else
	if(iType==2){ nameboss = "苦力怕娘: ";} else
	if(iType==3){ nameboss = "狗: "; type_boss = 2;} else
	if(iType==4){ nameboss = "恶魔骑士: "; type_boss = 2;} else
	if(iType==5){ nameboss = "恶魔剑士: "; type_boss = 2;} else
	if(iType==6){ nameboss = "血石: "; type_boss = 3;} else
	if(iType==7){ nameboss = "大狗: "; type_boss = 2;} else
	if(iType==8){ nameboss = "死神: ";} else
	if(iType==9){ nameboss = "错误娘: ";} else
	if(iType==10){ nameboss = "王后: ";} else
	if(iType==11){ nameboss = "猫女: ";} else
	if(iType==12){ nameboss = "水晶: "; type_boss = 2;} else
	if(iType==13){ nameboss = "真正的敌人: ";} else
	if(iType==14){ nameboss = "剩余: ";} else
	if(iType==15){ nameboss = "开关: ";}
	if(caller.IsValid())
	{
		local oBoss = cBoss(caller,nameboss,0,iTShow,type_boss);
		Bosses.push(oBoss);
		if(Tick==false)
		{
			Tick = true;
			ShowBossHP();
		}
	}
}

function ShowBossHP()
{
	if(Tick)
	{
		local bosshud = "BossHP:\n";
		local bShow = false;
		for(local i=0;i<Bosses.len();i+=1)
		{
			if(Bosses[i].timer_death==0)
			{
				if(Bosses[i].timer_show>0)
				{
					if(Bosses[i].entity.IsValid())
					{
						bShow = true;
						if(Bosses[i].type==1)
						{
							//script boss
							EntFireByHandle(Bosses[i].entity, "RunScriptCode", "GetBossHP();", 0.00, null, null);
							bosshud=bosshud+Bosses[i].name+Bosses[i].hp+"\n";
						} else if(Bosses[i].type==3)
						{
							EntFireByHandle(Bosses[i].entity, "RunScriptCode", "GetBossHP();", 0.00, null, null);
							bosshud=bosshud+Bosses[i].name+Bosses[i].hpbar+"x"+Bosses[i].hp+"\n";
						} else
						{
							bosshud=bosshud+Bosses[i].name+Bosses[i].entity.GetHealth()+"\n";
						}
						Bosses[i].timer_show--;
					} else
					{
						bShow = true;
						bosshud=bosshud+Bosses[i].name+"死掉了\n";
						RemoveBossID(i);
					}
				}
			} else if(Bosses[i].timer_death>1)
			{
				bShow = true;
				bosshud=bosshud+Bosses[i].name+"死掉了\n";
				Bosses[i].timer_death--;
			} else if (Bosses[i].timer_death==1)
			{
				Bosses.remove(i);
				bShow = true;
				EntFireByHandle(self, "RunScriptCode", "ShowBossHP();", UpdateTime, null, null);
				return;
			}
		}
		if(bShow)
		{
			//showbosshud message
			if (Bxzl_BossHP_Gametext!=null)
			{
				 Bxzl_BossHP_Gametext.__KeyValueFromString("message", bosshud);
				 EntFireByHandle(Bxzl_BossHP_Gametext, "Display", "", 0, Bxzl_BossHP_Gametext, Bxzl_BossHP_Gametext);
			}
			//ScriptPrintMessageCenterAll(bosshud);
		}
		Tick = bShow;
		EntFireByHandle(self, "RunScriptCode", "ShowBossHP();", UpdateTime, null, null);
	}
}

function RemoveBoss()
{
	for(local i=0;i<Bosses.len();i+=1)
	{
		if(Bosses[i].entity==caller)
		{
			Bosses[i].timer_death = iTShowDeath;
			break;
		}
	}
}

function RemoveBossID(idB)
{
	Bosses[idB].timer_death = iTShowDeath;
}

function UpdateTimer()
{
	for(local i=0;i<Bosses.len();i+=1)
	{
		if(Bosses[i].entity==caller)
		{
			Bosses[i].timer_show = iTShow;
			if(Tick==false)
			{
				Tick = true;
				ShowBossHP();
			}
			break;
		}
	}
}

function SetHP(iHP)
{
	for(local i=0;i<Bosses.len();i+=1)
	{
		if(Bosses[i].entity==caller)
		{
			Bosses[i].hp = iHP;
			break;
		}
	}
}

function SetHPBAR(iHP,iBAR)
{
	for(local i=0;i<Bosses.len();i+=1)
	{
		if(Bosses[i].entity==caller)
		{
			Bosses[i].hp = iHP;
			Bosses[i].hpbar = iBAR;
			break;
		}
	}
}
