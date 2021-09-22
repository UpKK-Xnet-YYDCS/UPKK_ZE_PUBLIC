bxzl_text <- null;
bxzl_timer_1 <- null;
bxzl_timer_2 <- null;
bxzl_timer_3 <- null;
bxzl_door_time <- 0;
bxzl_holy_time   <-  0;
bxzl_elevator_time <- 0;
bxzl_first_line  <-  "";
bxzl_second_line <-  "";
bxzl_third_line <-  "";

function Say_ScriptDate()
{
	bxzl_text = Entities.FindByName(null,"bxzl_text");
	bxzl_timer_1 = Entities.FindByName(null,"bxzl_timer_1");
	bxzl_timer_2 = Entities.FindByName(null,"bxzl_timer_2");
	bxzl_timer_3 = Entities.FindByName(null,"bxzl_timer_3");
	EntFire("consola","Command","say script by bxzl on 2021.06.05",0.00,null);
}

function bxzl_check_text_1()
{
	if(bxzl_door_time==0)
	{
		bxzl_first_line = "";
		EntFire("bxzl_timer_1","Disable","",0.00,null);
	}
	if(bxzl_door_time>0)
	{
		bxzl_first_line = "大门将在"+bxzl_door_time.tostring()+"秒后打开";
		EntFireByHandle(self,"RunScriptCode","bxzl_door_time-=1;",1.00,null,null);
	}
	bxzl_text.__KeyValueFromString("message", bxzl_first_line.tostring()+"\n"+bxzl_second_line.tostring()+"\n"+bxzl_third_line.tostring());
}

function bxzl_check_text_2()
{
	if(bxzl_holy_time==0)
	{
		bxzl_second_line = "";
		EntFire("bxzl_timer_2","Disable","",0.00,null);
	}
	if(bxzl_holy_time>0)
	{
		bxzl_second_line = "终极将在"+bxzl_holy_time.tostring()+"秒后生效";
		EntFireByHandle(self,"RunScriptCode","bxzl_holy_time-=1;",1.00,null,null);
	}
	bxzl_text.__KeyValueFromString("message", bxzl_first_line.tostring()+"\n"+bxzl_second_line.tostring()+"\n"+bxzl_third_line.tostring());
}

function bxzl_check_text_3()
{
	if(bxzl_elevator_time==0)
	{
		bxzl_third_line = "";
		EntFire("bxzl_timer_3","Disable","",0.00,null);
	}
	if(bxzl_elevator_time>0)
	{
		bxzl_third_line = "电梯将在"+bxzl_elevator_time.tostring()+"秒后离开";
		EntFireByHandle(self,"RunScriptCode","bxzl_elevator_time-=1;",1.00,null,null);
	}
	bxzl_text.__KeyValueFromString("message", bxzl_first_line.tostring()+"\n"+bxzl_second_line.tostring()+"\n"+bxzl_third_line.tostring());
}
