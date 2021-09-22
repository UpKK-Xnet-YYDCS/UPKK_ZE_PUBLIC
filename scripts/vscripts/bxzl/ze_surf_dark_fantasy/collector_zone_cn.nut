iCount<-0;
bDetect<-false;

bBowDoor<-false;
bSpearDoor<-false;
bSwordDoor<-false;
bShieldDoor<-false;

iSort<-[1,2,3,4];

function init_zone()
{
	iCount=0;
	bDetect=false;
	bBowDoor=false;
	bSpearDoor=false;
	bSwordDoor=false;
	bShieldDoor=false;
	Random_Combination();
	
	EntFire("lvls_collector_PT_triggers", "ForceSpawn", "", 0.00, null);
	EntFire("lvls_collector_PT_system", "ForceSpawn", "", 0.00, null);
	
	EntFire("lvls_collector_laser_timer_1", "Enable", "", 5.00, null);
	EntFire("lvls_collector_laser_timer_2", "Enable", "", 5.00, null);
	EntFire("lvls_collector_laser_timer_3", "Enable", "", 5.00, null);
}

function Lose_Detect()
{
	if(bDetect==false)
	{
		iCount=0;
		EntFire("lvls_collector_checker_sprite_bow", "Color", "255 255 255", 0.00, null);
		EntFire("lvls_collector_checker_sprite_spear", "Color", "255 255 255", 0.00, null);
		EntFire("lvls_collector_checker_sprite_sword", "Color", "255 255 255", 0.00, null);
		EntFire("lvls_collector_checker_sprite_shield", "Color", "255 255 255", 0.00, null);
		
		EntFire("lvls_collector_weapon_sprite*", "Kill", "", 0.00, null);
		EntFire("lvls_collector_weapon_pb*", "Kill", "", 0.00, null);
		EntFire("lvls_collector_weapon_elite*", "Kill", "", 0.50, null);
		
		EntFire("lvls_collector_PT_bow", "ForceSpawn", "", 2.00, null);
		EntFire("lvls_collector_PT_spear", "ForceSpawn", "", 2.00, null);
		EntFire("lvls_collector_PT_sword", "ForceSpawn", "", 2.00, null);
		EntFire("lvls_collector_PT_shield", "ForceSpawn", "", 2.00, null);
		
		EntFire("server", "Command", "say ***Respawn Items***", 2.00, null);
	}
}

function Random_Combination()
{
	for(local i=4;i>1;i-=1)
	{
		local rIndex=RandomInt(0,3);
		local temp = iSort[i-1];
		iSort[i-1] = iSort[rIndex];
		iSort[rIndex]=temp;
	}
}

function Show_Combination()
{
	local mes="say ***顺序 | ";
	local mes2="***放入物品的顺序 | ";
	for(local i=0;i<4;i+=1)
	{
		local sNum=i+1;
		if(iSort[i]==1)
		{
			mes=mes+sNum.tostring()+"-弓";
			mes2=mes2+sNum.tostring()+"-弓";
		}else if(iSort[i]==2)
		{
			mes=mes+sNum.tostring()+"-矛";
			mes2=mes2+sNum.tostring()+"-矛";
		}else if(iSort[i]==3)
		{
			mes=mes+sNum.tostring()+"-剑";
			mes2=mes2+sNum.tostring()+"-剑";
		}else if(iSort[i]==4)
		{
			mes=mes+sNum.tostring()+"-盾";
			mes2=mes2+sNum.tostring()+"-盾";
		}
		if(i<3)
		{
			mes=mes+" ";
			mes2=mes2+" ";
		}else
		{
			mes=mes+"***";
			mes2=mes2+"***";
		}
	}
	EntFire("server", "Command", mes.tostring(), 0.00, null);
	EntFire("system_gt_name_area","AddOutput","message "+"秘密 - 收集"+"\n" + mes2.tostring(),0.00,null);
}

function Detect_Item(iNum)//1-Bow, 2-Spear, 3-Sword, 4-Shield
{
	if(bDetect==false)
	{
		if(iSort[iCount]==iNum)
		{
			iCount++;
			EntFire("server", "Command", "say ***Item Accepted***", 0.00, null);
			if(iCount>=4)
			{
				bDetect=true;
				EntFire("lvls_collector_button", "Lock", "", 0.00, null);
				EntFire("lvls_collector_trig_final", "FireUser1", "", 11.00, null);
				
				EntFire("lvls_collector_laser_timer_1", "Disable", "", 0.00, null);
				EntFire("lvls_collector_laser_timer_2", "Disable", "", 0.00, null);
				EntFire("lvls_collector_laser_timer_3", "Disable", "", 0.00, null);
				
				EntFire("lvls_collector_earth_door_up", "Close", "", 0.00, null);
				EntFire("lvls_collector_earth_door_down", "Close", "", 0.00, null);
				EntFire("lvls_collector_water_door_up", "Close", "", 0.00, null);
				EntFire("lvls_collector_water_door_down", "Close", "", 0.00, null);
				EntFire("lvls_collector_fire_door_up", "Close", "", 0.00, null);
				EntFire("lvls_collector_fire_door_down", "Close", "", 0.00, null);
				EntFire("lvls_collector_wind_door_up", "Close", "", 0.00, null);
				EntFire("lvls_collector_wind_door_down", "Close", "", 0.00, null);
				
				EntFire("lvls_collector_afk_room_tp_trig", "Enable", "", 0.00, null);
				
				EntFire("lvls_collector_next_door", "Open", "", 16.00, null);
				EntFire("server", "Command", "say ***Door will open in 15 sec***", 1.00, null);
			}
		}else
		{
			iCount=0;
			Lose_Detect();
			EntFire("server", "Command", "say ***Wrong Combination***", 0.00, null);
		}
	}
}

function Open_Door(iDoor)
{
	if(iDoor==1)
	{
		if(bBowDoor==false)
		{
			bBowDoor=true;
			EntFire("lvls_collector_wind_door_up", "Open", "", 0.00, null);
		}
	}else if(iDoor==2)
	{
		if(bSpearDoor==false)
		{
			bSpearDoor=true;
			EntFire("lvls_collector_fire_door_up", "Open", "", 0.00, null);
		}
	}else if(iDoor==3)
	{
		if(bSwordDoor==false)
		{
			bSwordDoor=true;
			EntFire("lvls_collector_water_door_up", "Open", "", 0.00, null);
		}
	}else if(iDoor==4)
	{
		if(bShieldDoor==false)
		{
			bShieldDoor=true;
			EntFire("lvls_collector_earth_door_up", "Open", "", 0.00, null);
		}
	}
}