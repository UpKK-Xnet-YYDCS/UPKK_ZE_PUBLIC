function Display(amount, i)
{
    local x = amount;
    local y = i;
    local mes = "";
//    EntFire("seconds_left","SetText","      seconds left",0);
//    EntFire("hold_zomb","SetText","  HOLD ZOMBIES",0);
    for(i=1;i<=amount;i++)
    {
        if(x>y)
        {
            mes = "守 住 僵 尸" + "\n" + " " + "剩余" + x.tostring()+ "秒";
            EntFire("text_sec","SetText",mes.tostring(),i-1);
            EntFire("text_sec","Display","",i-1);
//            EntFire("seconds_left","Display","",i-1);
//            EntFire("hold_zomb","Display","",i-1);
            x=x-1;
        }
    }
}


function DisplayRTV(amount, i)
{
    local x = amount;
    local y = i;
    local mes = "";
//    EntFire("seconds_left","SetText","       seconds",0);
//    EntFire("hold_zomb","SetText","SURVIVE",0);
    for(i=1;i<=amount;i++)
    {
        if(x>y)
        {
            mes = "生 存 关 卡" + "\n" + " " +"剩余" + x.tostring()+ "秒";
            EntFire("text_sec","SetText",mes.tostring(),i-1);
            EntFire("text_sec","Display","",i-1);
//            EntFire("seconds_left","Display","",i-1);
//            EntFire("hold_zomb","Display","",i-1);
            x=x-1;
        }
    }
}
