iFloor<-0;
iSpecialEvent<-120;
bSpecialEvent<-false;
bSE_Disabled<-false;
sNameZone<-"秘密 - 恶魔地牢";

bDarkmode<-false;

iTRM<-31;

bTick<-false;

function SetDarkMode(bDM)
{
	if(bDM==0)
	{
		bDarkmode=false;
		sNameZone<-"message 秘密 - 恶魔地牢";
	}else {
		bDarkmode=true;
		sNameZone<-"message [黑暗模式]] 秘密 - 恶魔地牢";
	}
}

function init_DD()
{
	iFloor=0;
	iTRM=31;
	iSpecialEvent=120;
	bSpecialEvent=false;
	bSE_Disabled=false;
	
	EntFire("stm_adminroom", "RunScriptCode", "IsDarkmode();", 0.00, null);
	EntFire("stm_hud_script", "RunScriptCode", "Hud_set_current(13);", 0.00, null);
	
	EntFire("system_repiter_name_area", "Disable", "", 0.00, null);
	
	EntFire("lvls_dd_chtex_room", "SetTextureIndex", "0", 1.00, null);
	EntFire("lvls_dd_chtex_cp", "SetTextureIndex", "0", 1.00, null);
	EntFire("lvls_dd_chtex_base", "SetTextureIndex", "0", 1.00, null);
	
	EntFire("lvls_dd_PT", "ForceSpawn", "", 0.50, null);
	
	EntFire("stm_script", "RunScriptCode", "music_stop_all();", 0.00, null);
	EntFire("lvls_dd_sfx_start", "Volume", "10", 0.50, null);
	EntFire("lvls_dd_sfx_start", "PlaySound", "", 0.50, null);
	EntFire("lvls_dd_sfx_start", "Kill", "", 35.50, null);
	
	EntFire("lvls_dd_light1", "TurnOn", "", 15.00, null);
	EntFire("lvls_dd_light2", "TurnOn", "", 16.00, null);
	EntFire("lvls_dd_light3", "TurnOn", "", 17.00, null);
	
	EntFire("lvls_dd_particle_start", "Kill", "", 30.50, null);
	EntFire("lvls_dd_trig_multi_fade", "Enable", "", 30.50, null);
	EntFire("lvls_dd_trig_multi_fade", "Disable", "", 32.00, null);
	
	EntFire("server", "Command", "say ***You ended up in the dungeon of demons***", 0.00, null);
	EntFire("server", "Command", "say ***This dungeon contains 4 levels of difficulty***", 5.00, null);
	EntFire("server", "Command", "say ***To exit the dungeon you need to complete all tasks***", 10.00, null);
	EntFire("server", "Command", "say ***On the first level it is necessary to destroy the bloodstone***", 15.00, null);
	
	EntFireByHandle(self, "RunScriptCode", "init_Floor_1();", 35.00, null, null);
	
	bTick=true;
	EntFireByHandle(self, "RunScriptCode", "UpdateDD();", 1.00, null, null);
}

function UpdateDD()
{
	if(bTick)
	{
		if(iTRM>0)
		{
			iTRM--;
		}else
		{
			iTRM=290;
			EntFire("stm_script", "RunScriptCode", "music_stop_all();", 0.00, null);
			EntFire("lvls_dd_music_blacksea", "Volume", "8", 0.10, null);
			EntFire("lvls_dd_music_blacksea", "PlaySound", "", 0.10, null);
		}
		if(bSE_Disabled==false)
		{
			if(iSpecialEvent>1)
			{
				iSpecialEvent--;
			}else
			{
				if(bSpecialEvent==false)
				{
					bSpecialEvent=true;
					iSpecialEvent=55;
					init_SpecialEvent();
				}else
				{
					bSpecialEvent=false;
					iSpecialEvent=120;
					close_SpecialEvent();
				}
			}
		}
		UpdateFloor();
		EntFire("system_gt_name_area", "Display", "", 0.10, null);
		EntFireByHandle(self, "RunScriptCode", "UpdateDD();", 1.00, null, null);
	}
}

function init_SpecialEvent()
{
	EntFire("lvl3_trig_once", "Kill", "", 0.00, null);
	local rLocation=RandomInt(1,3);
	if(rLocation==1)
	{
		EntFire("lvls_dd_tp_human", "AddOutput", "target info_tp_def_lvl3_1", 0.00, null);
		EntFire("lvls_dd_tp_zombie", "AddOutput", "target info_tp_def_lvl3_1", 0.00, null);
	}else if(rLocation==2)
	{
		EntFire("lvls_dd_tp_human", "AddOutput", "target info_tp_def_lvl3_2", 0.00, null);
		EntFire("lvls_dd_tp_zombie", "AddOutput", "target info_tp_def_lvl3_2", 0.00, null);
	}else if(rLocation==3)
	{
		EntFire("lvls_dd_tp_human", "AddOutput", "target info_tp_def_lvl3_3", 0.00, null);
		EntFire("lvls_dd_tp_zombie", "AddOutput", "target info_tp_def_lvl3_3", 0.00, null);
	}
	EntFire("lvls_dd_tp_human", "Enable", "", 0.10, null);
	EntFire("lvls_dd_tp_zombie", "Enable", "", 10.00, null);
}

function close_SpecialEvent()
{
	EntFire("lvls_dd_tp_human", "Disable", "", 0.00, null);
	EntFire("lvls_dd_tp_zombie", "Disable", "", 0.00, null);
	EntFire("lvl3_def_trig_tp_next_surf_human", "AddOutput", "target info_tp_dd_human", 0.00, null);
	EntFire("lvl3_def_trig_tp_next_surf_zombie", "AddOutput", "target info_tp_dd_zombie", 0.00, null);
	EntFire("lvl3_def_trig_tp_next_surf_human", "Enable", "", 0.10, null);
	EntFire("lvl3_def_trig_tp_next_surf_zombie", "Enable", "", 0.10, null);
	EntFire("lvls_dd_tp_human", "AddOutput", "target info_tp_secret_collector", 1.00, null);
	EntFire("lvls_dd_tp_zombie", "AddOutput", "target info_tp_secret_collector", 1.00, null);
	EntFire("lvl3_def_trig_tp_next_surf_human", "Disable", "", 2.00, null);
	EntFire("lvl3_def_trig_tp_next_surf_zombie", "Disable", "", 2.00, null);
}

function Disable_SpecialEvent()
{
	bSE_Disabled=true;
	close_SpecialEvent();
}

function init_Floor_1()
{
	iFloor=1;
	EntFire("lvls_dd_bloodstone_PT", "ForceSpawn", "", 0.00, null);
}

function init_Floor_2()
{
	iFloor=2;
	
	EntFire("lvls_dd_trig_multi_fade", "Enable", "", 5.00, null);
	EntFire("lvls_dd_trig_multi_fade", "Disable", "", 6.00, null);
	EntFire("lvls_dd_chtex_room", "SetTextureIndex", "1", 10.00, null);
	EntFire("lvls_dd_chtex_cp", "SetTextureIndex", "1", 10.00, null);
	EntFire("lvls_dd_chtex_base", "SetTextureIndex", "1", 10.00, null);

	EntFire("server", "Command", "say ***On the second level you need to defeat all the demons***", 10.00, null);
	
	if(bDarkmode==false)
	{
		EntFire("lvls_dd_script_floor2", "RunScriptCode", "init_Boss(0);", 0.0, null);
		
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 13312 3504 -1984", 14.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 14.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 14.75, null);
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 12784 4096 -1984", 15.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 15.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 15.75, null);
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 13312 4688 -1984", 16.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 16.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 16.75, null);
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 13840 4096 -1984", 17.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 17.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 17.75, null);
	}else
	{
		EntFire("lvls_dd_script_floor2", "RunScriptCode", "init_Boss(1);", 0.0, null);
		
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 13312 3504 -1984", 14.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 14.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 14.75, null);
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 12784 4096 -1984", 15.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 15.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 15.75, null);
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 13312 4688 -1984", 16.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 16.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 16.75, null);
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 13840 4096 -1984", 17.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 17.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 17.75, null);
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 13632 4096 -1984", 18.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 18.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 18.75, null);
		EntFire("boss_miniboss_death_PT", "AddOutput", "origin 13312 4416 -1984", 19.00, null);
		EntFire("boss_miniboss_death_PT", "ForceSpawn", "", 19.50, null);
		EntFire("boss_mb_death_phbox_s*", "FireUser3", "", 19.75, null);
	}
}

function init_Floor_3()
{
	iFloor=3;
	
	EntFire("lvls_dd_trig_multi_fade", "Enable", "", 5.00, null);
	EntFire("lvls_dd_trig_multi_fade", "Disable", "", 6.00, null);
	
	EntFire("lvls_dd_chtex_room", "SetTextureIndex", "2", 10.00, null);
	EntFire("lvls_dd_chtex_cp", "SetTextureIndex", "2", 10.00, null);
	EntFire("lvls_dd_chtex_base", "SetTextureIndex", "2", 10.00, null);
	
	EntFire("lvls_dd_floor_3_PT", "ForceSpawn", "", 9.00, null);
	
	EntFire("server", "Command", "say ***At the third level you need to knock out the seal***", 5.00, null);
	
	EntFire("lvls_dd_script_floor3", "RunScriptCode", "init_Boss();", 13.00, null);
	
	EntFire("boss_miniboss_taros_PT", "AddOutput", "origin 13312 3504 -1984", 14.00, null);
	EntFire("boss_miniboss_taros_PT", "ForceSpawn", "", 14.50, null);
	EntFire("boss_mb_taros_phbox_s*", "FireUser3", "", 14.75, null);
	
	EntFire("boss_miniboss_taros_PT", "AddOutput", "origin 13312 4688 -1984", 15.00, null);
	EntFire("boss_miniboss_taros_PT", "ForceSpawn", "", 15.50, null);
	EntFire("boss_mb_taros_phbox_s*", "FireUser3", "", 15.75, null);	
}

function init_Floor_4()
{
	iFloor=4;
	
	EntFire("lvls_dd_floor_3_filter_seal", "Kill", "", 2.00, null);
	
	EntFire("lvls_dd_trig_multi_fade", "Enable", "", 5.00, null);
	EntFire("lvls_dd_trig_multi_fade", "Disable", "", 6.00, null);
	
	EntFire("lvls_dd_chtex_room", "SetTextureIndex", "3", 10.00, null);
	EntFire("lvls_dd_chtex_cp", "SetTextureIndex", "3", 10.00, null);
	EntFire("lvls_dd_chtex_base", "SetTextureIndex", "3", 10.00, null);
	
	EntFire("server", "Command", "say ***On the fourth level you have to defeat Charon***", 5.00, null);
	
	EntFire("server", "Command", "say ***BuyZone activated for 8 seconds***", 7.00, null);
	EntFire("lvls_dd_buyzone", "Enable", "", 7.00, null);
	EntFire("lvls_dd_buyzone", "Disable", "", 15.00, null);
	EntFire("lvls_dd_buyzone", "Kill", "", 16.00, null);
	
	EntFire("lvls_dd_sfx_no_one", "PlaySound", "", 15.00, null);
	EntFire("lvls_dd_sfx_no_one", "Kill", "", 25.00, null);
	
	EntFire("lvls_dd_floor_4_boss_attack_PT", "ForceSpawn", "", 17.00, null);
	EntFire("boss_PT_charon", "AddOutput", "origin 13826 4096 -1984", 19.00, null);
	EntFire("boss_PT_charon", "ForceSpawn", "", 20.00, null);
	EntFire("boss_charon_phb2", "RunScriptCode", "init_Boss();", 21.00, null);
}

function DD_win()
{
	bTick=false;
	EntFire("system_repiter_name_area", "Enable", "", 1.00, null);
	EntFire("lvls_collector_PT_system", "RunScriptCode", "init_zone();", 9.00, null);
	EntFire("stm_hud_script", "RunScriptCode", "Hud_set_current(14);", 15.00, null);
	EntFire("lvls_dd_tp_human", "Enable", "", 15.00, null);
	EntFire("lvls_dd_tp_zombie", "Enable", "", 25.00, null);
	
	EntFire("stm_script", "RunScriptCode", "music_stop_all();", 14.90, null);
	EntFire("system_music_collector", "Volume", "7", 15.00, null);
	EntFire("system_music_collector", "PlaySound", "", 15.00, null);
	
	EntFire("server", "Command", "say ***Humans will be teleported after 10 seconds***", 5.00, null);
	EntFire("server", "Command", "say ***Zombies will be teleported after 10 seconds***", 15.00, null);
	EntFire("server", "Command", "say ***To go further you must solve the riddle***", 17.00, null);
	
	EntFire("stm_script", "RunScriptCode", "DD_entity_cleaner();", 16.00, null);
}

function UpdateFloor()
{
	if(iFloor==0)
	{
		EntFire("system_gt_name_area", "AddOutput", sNameZone+"\n第一层 - 血石", 0.00, null);
	}else if(iFloor==1)
	{
		if(bSpecialEvent==false)
		{
			EntFire("system_gt_name_area", "AddOutput", sNameZone+"\n第一层 - 血石\n特殊事件将在 "+iSpecialEvent+" 秒后出现", 0.00, null);
		}else
		{
			EntFire("system_gt_name_area", "AddOutput", sNameZone+"\n第一层 - 血石\n特殊事件将持续 "+iSpecialEvent+" 秒", 0.00, null);
		}
	}else if(iFloor==2)
	{
		if(bSpecialEvent==false)
		{
			EntFire("system_gt_name_area", "AddOutput", sNameZone+"\n第二层 - 恶魔\n特殊事件将在 "+iSpecialEvent+" 秒后出现", 0.00, null);
		}else
		{
			EntFire("system_gt_name_area", "AddOutput", sNameZone+"\n第二层 - 恶魔\n特殊事件将持续 "+iSpecialEvent+" 秒", 0.00, null);
		}
	}else if(iFloor==3)
	{
		if(bSE_Disabled==false)
		{
			if(bSpecialEvent==false)
			{
				EntFire("system_gt_name_area", "AddOutput", sNameZone+"\n第三层 - 封印\n特殊事件将在 "+iSpecialEvent+" 秒后出现", 0.00, null);
			}else
			{
				EntFire("system_gt_name_area", "AddOutput", sNameZone+"\n第三层 - 封印\n特殊事件将持续 "+iSpecialEvent+" 秒", 0.00, null);
			}
		}else 
		{
			EntFire("system_gt_name_area", "AddOutput", sNameZone+"\n第三层 - 封印", 0.00, null);
		}
	}else if(iFloor==4)
	{
		EntFire("system_gt_name_area", "AddOutput", sNameZone+"\n第四层 - 死神", 0.00, null);
	}
}