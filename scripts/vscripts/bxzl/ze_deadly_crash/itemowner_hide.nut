older_owner <- null;
ticking <- false;
pistol <- null;

function SetOwner()
{
	pistol = caller;
	if( (older_owner != null) && (older_owner.IsValid()) )
	{
		if(older_owner == activator)
		{
			older_owner = activator;
			EntFireByHandle(older_owner,"AddOutput","rendermode 1",0.1,older_owner,null);
			EntFireByHandle(older_owner,"Alpha","10",0.2,older_owner,null);	
		}
		else
		{
			EntFireByHandle(older_owner,"AddOutput","rendermode 0",0,older_owner,null);
			older_owner = activator;
			EntFireByHandle(older_owner,"AddOutput","rendermode 1",0.1,older_owner,null);
			EntFireByHandle(older_owner,"Alpha","10",0.2,older_owner,null);
		}
	}
	else
	{
			older_owner = activator;
			EntFireByHandle(older_owner,"AddOutput","rendermode 1",0.1,older_owner,null);
			EntFireByHandle(older_owner,"Alpha","10",0.2,older_owner,null);
	}
	if(!ticking)
	{
		ticking = true;
		Tick();
	}
}

function Tick()
{
	if(!ticking)
	{
		return;
	}
	if(pistol!=null && pistol.IsValid())
	{
		if( (pistol.GetOwner() == null) || (!pistol.GetOwner().IsValid()) )
		{
			EntFireByHandle(older_owner,"AddOutput","rendermode 0",0,older_owner,null);
			ticking = false;
		}
	}
	if(ticking)
	{
		EntFireByHandle(self,"RunScriptCode"," Tick(); ",0.03,null,null);
	}
}
