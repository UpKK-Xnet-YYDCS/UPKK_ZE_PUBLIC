
MapHudHint	<-	null;
DevGunHud	<-	null;

function Say_ScriptDate()
{
		EntFire("Cmd","Command","say script by bxzl on 2021.09.02",0.00,null);
		MapHudHint = Entities.FindByName(null,"Map_HudHint");
		DevGunHud = Entities.FindByName(null,"Dev_Gun_Hud");
}

function Map_HudHint_Change()
{
		if( (MapHudHint != null) && (MapHudHint.GetClassname() == "game_text") )
		{
			MapHudHint.__KeyValueFromString("message", "神庙奇袭\n---------------------------\n地图作者:Slayerdragon & h4sArD/Noctali\n翻译:bxzl\n改动:----------------------\n100秒模式触发NPC由原本20%概率出现改为通关正常关卡后必刷\n以及取消原本的100秒模式在通关一次后不再刷新的设定");
		}
}

function Dev_Gun_Hud_Change(index)
{
		if( (DevGunHud != null) && (DevGunHud.GetClassname() == "game_text") )
		{
			switch(index)
			{
				case 1:
				{
					DevGunHud.__KeyValueFromString("message", ">设定人类血量<\n>设定值:200<");
          break;
				}
				case 2:
				{
					DevGunHud.__KeyValueFromString("message", ">设定人类血量<\n>设定值:10000<");
          break;
				}
				case 3:
				{
					DevGunHud.__KeyValueFromString("message", ">设定人类无敌<\n>持续:10秒<");
          break;
				}
				case 4:
				{
					DevGunHud.__KeyValueFromString("message", ">定住僵尸<\n>持续:10秒<");
          break;
				}
				case 5:
				{
					DevGunHud.__KeyValueFromString("message", ">BOSS 龙 血量<\n>增加:50点<");
          break;
				}
				case 6:
				{
					DevGunHud.__KeyValueFromString("message", ">BOSS 龙 血量<\n>减少:9999点<");
          break;
				}
				case 7:
				{
					DevGunHud.__KeyValueFromString("message", ">BOSS 飞船 血量<\n>增加:50点<");
          break;
				}
				case 8:
				{
					DevGunHud.__KeyValueFromString("message", ">BOSS 飞船 血量<\n>减少:9999点<");
          break;
				}
				case 9:
				{
					DevGunHud.__KeyValueFromString("message", ">调整尸变比<\n>设定值:10<");
          break;
				}
				case 10:
				{
					DevGunHud.__KeyValueFromString("message", ">设定僵尸复活延迟<\n>设定值:15秒<");
          break;
				}
				case 11:
				{
					DevGunHud.__KeyValueFromString("message", ">更改僵尸设定<\n>禁止自动复活<");
          break;
				}
				case 12:
				{
					DevGunHud.__KeyValueFromString("message", ">更改僵尸设定<\n>启用自动复活<");
          break;
				}
				case 13:
				{
					DevGunHud.__KeyValueFromString("message", ">更改僵尸设定<\n>禁止复活<");
          break;
				}
				case 14:
				{
					DevGunHud.__KeyValueFromString("message", ">更改僵尸设定<\n>启用复活<");
          break;
				}
			}
		}
}
