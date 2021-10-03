my_time <- 0.0;
speed_rate <- 0.0;
v1 <- Vector(0,0,0);
time_finish <- false;

function timer()
{
	if(time_finish)
	{
		return;
	}
	if(my_time > 1.4)
	{
		speed_rate = 0.3;
	}
	else if(my_time > 0.9)
	{
		speed_rate = 0.5;
	}
	else if(my_time > 0.4)
	{
		speed_rate = 0.8;
	}
	else if(my_time > 0)
	{
		speed_rate = 1;
	}
	EntFireByHandle(self,"RunScriptCode","timer();",0.1,null,null);
	my_time = my_time + 0.1;
	//printl("time="+my_time.tostring());
} 

function stop()
{
	time_finish = true;
}

function start()
{
	my_time = -1;
	speed_rate = 1.0;
	time_finish = false;
	EntFireByHandle(self,"RunScriptCode","timer();",0.1,null,null);
	v1 = self.GetOrigin();
	//printl(v1.tostring());
} 

function end()
{
	DoEntFire("speedmod","ModifySpeed","1",1,activator,null);
	DoEntFire("client","Command","r_screenoverlay off",1,activator,null);
	EntFireByHandle(self,"RunScriptCode","activator.SetVelocity(activator.GetVelocity()*0.3)",1,activator,null);
}

function qwq()
{
	
	local v = activator.GetOrigin() - v1;
	local v_len = sqrt(v.x*v.x+v.y*v.y);
	local act_speed_rate = (v_len / 400 - 0.1);
	if(act_speed_rate>1)
		act_speed_rate = 1;
	if(act_speed_rate<0)
		act_speed_rate = 0;	
    
	act_speed_rate = speed_rate * act_speed_rate;
  
	DoEntFire("speedmod","ModifySpeed",act_speed_rate.tostring(),0,activator,null);
  
	if(act_speed_rate>0.6)
	{
		DoEntFire("client","Command","r_screenoverlay fong/ice1.vmt",0,activator,null);
	}
	else if(act_speed_rate>0.2)
	{
		DoEntFire("client","Command","r_screenoverlay fong/ice2.vmt",0,activator,null);
	}
	else
	{
		DoEntFire("client","Command","r_screenoverlay fong/ice3.vmt",0,activator,null);
	}
	
if(time_finish)
	{
		DoEntFire("speedmod","ModifySpeed","1",2,activator,null);
		DoEntFire("client","Command","r_screenoverlay off",2,activator,null);
		EntFireByHandle(self,"RunScriptCode","activator.SetVelocity(activator.GetVelocity()*0.3)",2,activator,null);
	}
		
}
