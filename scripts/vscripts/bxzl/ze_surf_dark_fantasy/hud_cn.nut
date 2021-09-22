bDarkmode<-false;
sMessage<-"Spawn";
bTick<-false;
iTimerErrorGirl<-90;

function SetDarkMode(bDM)
{
	if(bDM==0)
	{
		bDarkmode=false;
	}else {
		bDarkmode=true;
	}
}

function Hud_set_current(iLevel)
{
	EntFire("stm_adminroom", "RunScriptCode", "IsDarkmode();", 0.00, null);
	EntFireByHandle(self, "RunScriptCode", "Hud_set_cl("+iLevel+");", 0.02, null, null);
}

function Hud_set_cl(iLevel)
{
	local msg = "message ";
	if(bDarkmode==true)
	{
		msg=msg+"[黑暗模式] ";
	}
	if(iLevel==1)
	{
		msg=msg+"出生点";
	}else if(iLevel==2)
	{
		msg=msg+"简单滑翔";
	}else if(iLevel==3)
	{
		msg=msg+"简单防守";
	}else if(iLevel==4)
	{
		msg=msg+"普通滑翔";
	}else if(iLevel==5)
	{
		msg=msg+"普通防守";
	}else if(iLevel==6)
	{
		msg=msg+"困难滑翔";
	}else if(iLevel==7)
	{
		msg=msg+"困难防守";
	}else if(iLevel==8)
	{
		msg=msg+"极限滑翔";
	}else if(iLevel==9)
	{
		msg=msg+"苦力怕娘";
	}else if(iLevel==10)
	{
		msg=msg+"秘密 - 城堡";
	}else if(iLevel==11)
	{
		msg=msg+"秘密 - 下水道";
	}else if(iLevel==12)
	{
		msg=msg+"秘密 - 地下墓窟";
	}else if(iLevel==13)
	{
		msg=msg+"秘密 - 恶魔地牢";
	}else if(iLevel==14)
	{
		msg=msg+"秘密 - 收集";
	}else if(iLevel==15)
	{
		msg=msg+"秘密 - 鬼魂";
	}else if(iLevel==16)
	{
		msg=msg+"秘密 - 真结局";
	}
	sMessage=msg;
	EntFire("system_gt_name_area","AddOutput",msg,0.00,null);
	EntFire("system_repiter_name_area","FireTimer","",0.02,null);
	EntFire("system_repiter_name_area","ResetTimer","",0.02,null);
}

function Hud_Show_False_Ending()
{
	EntFire("system_gt_name_area","AddOutput","color 255 0 0",0.00,null);
	EntFireByHandle(self, "RunScriptCode", "Set_AddHUDMessage(1);", 0.00, null, null);
	EntFireByHandle(self, "RunScriptCode", "Set_AddHUDMessage(2);", 2.00, null, null);
	EntFire("system_gt_name_area","AddOutput","color 65 150 255",4.00,null);
}

function Hud_Show_True_Ending()
{
	EntFire("system_gt_name_area","AddOutput","color 0 255 0",0.00,null);
	EntFireByHandle(self, "RunScriptCode", "Set_AddHUDMessage(3);", 0.00, null, null);
	EntFireByHandle(self, "RunScriptCode", "Set_AddHUDMessage(4);", 2.00, null, null);
	EntFireByHandle(self, "RunScriptCode", "Set_AddHUDMessage(5);", 4.00, null, null);
	EntFire("system_gt_name_area","AddOutput","color 65 150 255",6.00,null);
}

function Set_AddHUDMessage(iMsg)
{
	if(iMsg==1)
	{
		EntFire("system_gt_name_area","AddOutput",sMessage+"\n\nN上回合没有找到所有的命运齿轮",0.00,null);
	}else if(iMsg==2)
	{
		EntFire("system_gt_name_area","AddOutput",sMessage+"\n\n触发假结局",0.00,null);
	}else if(iMsg==3)
	{
		EntFire("system_gt_name_area","AddOutput",sMessage+"\n\n上回合找到了所有的命运齿轮",0.00,null);
	}else if(iMsg==4)
	{
		EntFire("system_gt_name_area","AddOutput",sMessage+"\n\n触发真结局",0.00,null);
	}else if(iMsg==5)
	{
		EntFire("system_gt_name_area","AddOutput",sMessage+"\n\n你们的故事现在开始",0.00,null);
	}
	EntFire("system_repiter_name_area","FireTimer","",0.02,null);
	EntFire("system_repiter_name_area","ResetTimer","",0.02,null);
	EntFire("system_gt_name_area","AddOutput",sMessage,0.50,null);
}

function BossArena_EG_Start()
{
	EntFire("system_repiter_name_area","Disable","",0.00,null);
	iTimerErrorGirl=90;
	bTick=true;
	EntFireByHandle(self, "RunScriptCode", "BossArena_ErrorGirl();", 1.00, null, null);
}

function BossArena_EG_Stop()
{
	bTick=false;
}

function BossArena_ErrorGirl()
{
	if(bTick==true)
	{
		if(iTimerErrorGirl>15)
		{
			EntFire("system_gt_name_area","AddOutput",sMessage+"\n\n你们有 "+iTimerErrorGirl+" 秒去杀死错误娘",0.00,null);		
		}else if(iTimerErrorGirl>5)
		{
			EntFire("system_gt_name_area","AddOutput",sMessage+"\n\n你们还剩 "+iTimerErrorGirl+" 秒, 快点！",0.00,null);	
		}else if(iTimerErrorGirl>0)
		{
			EntFire("system_gt_name_area","AddOutput",sMessage+"\n\n"+iTimerErrorGirl+" 秒后核爆",0.00,null);	
		}else
		{
			bTick=false;
			EntFire("lvls_true_bossarena_PT_init","RunScriptCode","ErrorGirl_Lose();",0.00,null);
		}
		if(iTimerErrorGirl==48)
		{
			EntFire("boss_errorgirl_pb2", "RunScriptCode", "EG_BlueScreen();", 0.00, null);
		}
		if((iTimerErrorGirl>=35) && (iTimerErrorGirl<=45))
		{
			EntFire("boss_errorgirl_pb2", "RunScriptCode", "EG_Fade();", 0.00, null);
		}
		EntFire("system_gt_name_area","Display","",0.05,null);
		iTimerErrorGirl--;
		EntFireByHandle(self, "RunScriptCode", "BossArena_ErrorGirl();", 1.00, null, null);
	}else
	{
		EntFire("system_gt_name_area","AddOutput",sMessage,0.00,null);
		EntFire("system_repiter_name_area","Enable","",0.02,null);
		EntFire("system_repiter_name_area","FireTimer","",0.04,null);
		EntFire("system_repiter_name_area","ResetTimer","",0.04,null);
	}
}