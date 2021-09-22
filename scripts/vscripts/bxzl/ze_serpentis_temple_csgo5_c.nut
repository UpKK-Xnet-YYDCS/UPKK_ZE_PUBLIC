bxzltext <- null;
bxzl_bosshp  <- 0;
casetime <- 0;

function show_reset()
{
		bxzl_bosshp=0;
		casetime=0;
}

function Say_ScriptDate()
{
		bxzltext = Entities.FindByName(null,"bxzl_text");
		EntFire("Server","Command","say script by bxzl on 2020.12.02",0.00,null);
}

function text_change_1()
{
		if( (bxzltext != null) && (bxzltext.GetClassname() == "game_text") )
		{
			if (BossHpBar == 1)
			{
				EntFire("map_brush","RunScriptCode","bxzl_bosshp= BossHealth",0.00,null);
				bxzltext.__KeyValueFromString("message", "球(共用血量)"+" "+":"+" "+bxzl_bosshp.tostring());
			}
			else if(BossHpBar<=0)
			{
				EntFire("hud_timer","Disable","",0.00,null);
				bxzltext.__KeyValueFromString("message", "球(共用血量)"+" "+":"+" "+"0");
				local temp = bxzltext.GetName();
				EntFire(temp,"Display","",0.05,null);
			}
		}
}
function text_change_2()
{
		if( (bxzltext != null) && (bxzltext.GetClassname() == "game_text") )
		{
			if (BossHpBar >= 1)
			{
				EntFire("map_brush","RunScriptCode","bxzl_bosshp= ChangeHealth*(BossHpBar-1)+BossHealth",0.00,null);
				bxzltext.__KeyValueFromString("message", "美杜莎"+" "+":"+" "+bxzl_bosshp.tostring());
			}
			else if(BossHpBar<=0)
			{
				EntFire("hud_timer","Disable","",0.00,null);
				bxzltext.__KeyValueFromString("message", "美杜莎"+" "+":"+" "+"0");
				local temp = bxzltext.GetName();
				EntFire(temp,"Display","",0.05,null);
			}
		}
}

function text_show()
{		
	if ( (bxzltext != null) && (bxzltext.GetClassname() == "game_text") && (BossHealth != 0) )
	{
				if(casetime == 0)
				{
					return;
				}
				if (casetime == 1)
				{
					text_change_1();
				}
				if (casetime == 2)
				{
					text_change_2();
				}
				local temp1 = bxzltext.GetName();
				EntFire(temp1,"Display","",0.05,null);
	}
}
