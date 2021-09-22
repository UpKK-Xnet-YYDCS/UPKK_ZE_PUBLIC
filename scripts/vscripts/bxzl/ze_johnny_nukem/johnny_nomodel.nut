STAGE <- 1;
NO_BALLS <- false;
UFO_ULT <- false;

function MapStart()
{
    if(UFO_ULT && STAGE == 2)
    {
        EntFire("UFO_Quest_Relay", "Enable", "", 0.00, null);
    }
    SendToConsoleServer("sv_disable_radar 1");
    if(STAGE == 1)
    {
        EntFireByHandle(self, "FireUser1", "", 0.00, null, null);
    }
    else if(STAGE == 2)
    {
        EntFireByHandle(self, "FireUser2", "", 0.00, null, null);
    }
    else if(STAGE == 3)
    {
        EntFireByHandle(self, "FireUser3", "", 0.00, null, null);
    }
    if(NO_BALLS)
    {
        EntFireByHandle(self, "FireUser4", "", 0.00, null, null);
    }
}

function LevelWon()
{
    if(STAGE == 3)
    {
        NO_BALLS = true;
        return STAGE=1;
    }
    STAGE++;
}

function SetPlayerSkin()
{
        local p = null;
        while(null != (p = Entities.FindByClassname(p, "player")))
        {
            if(p.GetTeam() == 3 && p.GetHealth() > 0 && p.GetModelName() != "models/player/johnnynukem.mdl")
            {
                p.SetModel("models/player/johnnynukem.mdl");
            }
        }
}

function NO_Balls_Text()
{
    ScriptPrintMessageChatAll(" \x02 **NO BALLS MODE ACTIVATED**");
    ScriptPrintMessageChatAll(" \x02 **NOW BABIES THE REAL GAME HAS STARTED**");
}
