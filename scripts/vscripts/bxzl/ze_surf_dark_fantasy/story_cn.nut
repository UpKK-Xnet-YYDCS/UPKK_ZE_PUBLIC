iNumLang<-0;
//Only story Translate. I apologize if there are inaccuracies somewhere
function SetLang(iNum)
{
	if(iNum==0)
	{
		//English
		iNumLang=0;
	}else if(iNum==1)
	{
		//Russian
		iNumLang=1;
	}else if(iNum==2)
	{
		//Chinese
		iNumLang=2;
	}else
	{
		//default
		iNumLang=0;
	}
}

function StoryText(iText)
{
	if(iNumLang==0)
	{
		Translate_English(iText);
	}else if(iNumLang==1)
	{
		Translate_Russian(iText);
	}else if(iNumLang==2)
	{
		Translate_Chinese(iText);
	}else
	{
		Translate_English(iText);
	}
}

function Translate_English(iTE)
{
	if(iTE==1)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 A group of heroes was called to another world");
	}else if(iTE==2)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 In this difficult time the empire was almost destroyed");
	}else if(iTE==3)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Gathering the remnants of power people settled in the last undefeated city");
	}else if(iTE==4)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 But trouble got to the last stronghold of humanity ...");
	}else if(iTE==5)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 To explain all the reasons for the heroes called to the castle");
	}else if(iTE==6)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 The heroes were supposed to meet the queen but ...");
	}else if(iTE==7)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Before that they had to demonstrate their strength and intelligence");
	}else if(iTE==8)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Heroes have proven their strength and are now ready to meet with the queen");
	}else if(iTE==9)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 When the heroes arrived at the top floor of the tower ...");
	}else if(iTE==10)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 They saw the queen on the edge of the balcony");
	}else if(iTE==11)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 And then the queen jumped down");
	}else if(iTE==12)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 The death of the queen was blamed on the heroes who arrived ...");
	}else if(iTE==13)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 There was a guard everywhere");
	}else if(iTE==14)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 To avoid execution innocent people had to leave the city as soon as possible");
	}else if(iTE==15)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 To go unnoticed could only be through the sewer");
	}else if(iTE==16)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 The only passage was overwhelmed");
	}else if(iTE==17)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Something caused the destruction of the wall");
	}else if(iTE==18)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Very suspicious portal but people had no choice");
	}else if(iTE==19)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Everyone looked around");
	}else if(iTE==20)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 No one could understand where the portal led them");
	}else if(iTE==21)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Perhaps this passage has remained from the ancient civilization");
	}else if(iTE==22)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Suddenly everyone noticed the ghost away");
	}else if(iTE==23)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Everyone wondered: what was it now");
	}else if(iTE==24)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Heroes have moved further along the catacombs full of danger");
	}else if(iTE==25)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 One of the people lifted into the air and twice hit the wall");
	}else if(iTE==26)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 These catacombs not only contain traps and mobs but also something more sinister");
	}else if(iTE==27)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Moving on the heroes came closer to solving unusual events");
	}else if(iTE==28)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Whats happening");
	}else if(iTE==29)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 This ghost is so much like a queen");
	}else if(iTE==30)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 These events happened many years ago");
	}else if(iTE==31)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 The ghost sprained limbs and then chopped with an ax");
	}else if(iTE==32)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 This ghost has suffered torture");
	}else if(iTE==33)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 She crushed her limbs and then gouged out her eyes");
	}else if(iTE==34)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 And she was burned at the stake");
	}else if(iTE==35)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Heroes learned the truth about the cause of all disasters");
	}else if(iTE==36)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 They must end this");
	}else if(iTE==37)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Heroes heard a mysterious voice: it was all I");
	}else if(iTE==38)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04Story\x0B] \x01 Now enjoy your torment");
	}
}

function Translate_Russian(iTR)
{
	if(iTR==1)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Группа героев была призвана в другой мир");
	}else if(iTR==2)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01В это нелёгкое время империя была почти разрушена");
	}else if(iTR==3)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Собрав остатки сил люди обосновались в последнем неразрушенном городе");
	}else if(iTR==4)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Но беда добралась и до последнего оплота человечества...");
	}else if(iTR==5)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Для объяснения всех причин героев позвали в замок");
	}else if(iTR==6)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Герои должны были встретится с королевой но...");
	}else if(iTR==7)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01До этого они должны были продемонстрировать свою силу и интеллект");
	}else if(iTR==8)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Герои доказали свою силу и теперь готовы встретится с королевой");
	}else if(iTR==9)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Когда герои прибыли на верхний этаж башни...");
	}else if(iTR==10)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Они увидели королеву на краю балкона");
	}else if(iTR==11)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01А затем королева прыгнула вниз");
	}else if(iTR==12)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01В смерти королевы обвинили прибывших героев...");
	}else if(iTR==13)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Всюду была стража");
	}else if(iTR==14)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Чтобы избежать казни невиновные должны были покинуть город как можно скорее");
	}else if(iTR==15)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Пройти незамеченными можно были лишь через канализацию");
	}else if(iTR==16)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Единственный проход завалило");
	}else if(iTR==17)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Что-то вызвало разрушение стены");
	}else if(iTR==18)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Очень подозрительный портал но у людей не было выбора");
	}else if(iTR==19)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Все оглядывались по сторонам");
	}else if(iTR==20)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Никто не мог понять куда их привёл портал");
	}else if(iTR==21)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Возможно этот проход остался от древней цивилизации");
	}else if(iTR==22)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Вдруг все заметили вдали призрака");
	}else if(iTR==23)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Все задались вопросом: что это сейчас такое было");
	}else if(iTR==24)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Герои продвинулись дальше по катакомбам полных опасности");
	}else if(iTR==25)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Одного из людей подняло в воздух и дважды ударило об стену");
	}else if(iTR==26)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Эти катакомбы не только содержат ловушки и мобов но и ещё что-то зловещее");
	}else if(iTR==27)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Продвигаясь дальше герои подходили всё ближе к разгадке необычных событий");
	}else if(iTR==28)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Что происходит");
	}else if(iTR==29)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Этот призрак так похож на королеву");
	}else if(iTR==30)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Эти события произошли много лет назад");
	}else if(iTR==31)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01У призрака растянули конечности а затем её разрубило топором");
	}else if(iTR==32)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Этот призрак подвергся мучительным пыткам");
	}else if(iTR==33)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Ей раздробили конечности а затем выкололи глаза");
	}else if(iTR==34)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01А она была сожжена на костре");
	}else if(iTR==35)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Герои узнали правду о причине всех бедствий");
	}else if(iTR==36)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Они должны положить конец этому");
	}else if(iTR==37)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01Герои услышали загадочный голос: это всё был я");
	}else if(iTR==38)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04История\x0B] \x01А теперь наслаждайтесь своими мучениями");
	}
}

function Translate_Chinese(iTC)
{
	if(iTC==1)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01一群英雄被召唤到另一个世界");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 一群英雄被召唤到另一个世界",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==2)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01在这个困难时期，帝国几乎被摧毁");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 在这个困难时期，帝国几乎被摧毁",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==3)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01聚集了残余势力的人们定居在最后一座不败之城");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 聚集了残余势力的人们定居在最后一座不败之城",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==4)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01但是麻烦也如期而至…");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 但是麻烦也如期而至…",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==5)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01为了解释发生的情况，英雄们被叫到城堡");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 为了解释发生的情况，英雄们被叫到城堡",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==6)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01英雄们本计划去见女王，但是……");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 英雄们本计划去见女王，但是……",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==7)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01在那之前，他们必须展示他们的力量和智慧");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 在那之前，他们必须展示他们的力量和智慧",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==8)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01英雄们已经证明了他们的力量，现在准备与女王会面");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 英雄们已经证明了他们的力量，现在准备与女王会面",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==9)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01当英雄们到达塔顶时……");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 当英雄们到达塔顶时……",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==10)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01他们看见王后站在阳台上");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 他们看见王后站在阳台上",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==11)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01然后他们目睹了王后跳了下来");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 然后他们目睹了王后跳了下来",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==12)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01女王的死被归咎于英雄们的到来。");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 女王的死被归咎于英雄们的到来。",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==13)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01到处都是警卫");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 到处都是警卫",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==14)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01为了避免招致无妄之灾，无辜的人们不得不尽快离开这座城市");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 为了避免招致无妄之灾，无辜的人们不得不尽快离开这座城市",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==15)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01为了掩人耳目只能从下水道逃走");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 为了掩人耳目只能从下水道逃走",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==16)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01唯一的通道被淹没了");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 唯一的通道被淹没了",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==17)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01有什么东西摧毁了墙");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 有什么东西摧毁了墙",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==18)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01非常可疑的门，但人们别无选择");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 非常可疑的门，但人们别无选择",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==19)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01人们面面相觑");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 人们面面相觑",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==20)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01没有人能知道那扇门能把他们带到哪里");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 没有人能知道那扇门能把他们带到哪里",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==21)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01也许这座地下建筑是在古时建造的");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 也许这座地下建筑是在古时建造的",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==22)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01突然，大家都注意到鬼魂不见了");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 突然，大家都注意到鬼魂不见了",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==23)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01每个人都很疑惑:现在还会发生什么？");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 每个人都很疑惑:现在还会发生什么？",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==24)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01英雄们已经沿着充满危险的地下墓穴走得更远了");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 英雄们已经沿着充满危险的地下墓穴走得更远了",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==25)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01有一个人被一股未知力量腾空，两次撞到墙上");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 有一个人被一股未知力量腾空，两次撞到墙上",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==26)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01这些地下墓穴不仅包含陷阱和怪物，而且还有一些更邪恶的东西");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 这些地下墓穴不仅包含陷阱和怪物，而且还有一些更邪恶的东西",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==27)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01英雄们离解决不寻常事件更近了一步");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 英雄们离解决不寻常事件更近了一步",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==28)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01发生了什么？");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 发生了什么？",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==29)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01这个鬼魂太像女王了");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 这个鬼魂太像女王了",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==30)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01这些事件发生在许多年前");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 这些事件发生在许多年前",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==31)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01鬼魂被扭断了四肢，之后被斧头腰斩");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 鬼魂被扭断了四肢，之后被斧头腰斩",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==32)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01这个鬼魂遭受了折磨");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 这个鬼魂遭受了折磨",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==33)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01她残废了四肢，然后被挖出了眼睛");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 她残废了四肢，然后被挖出了眼睛",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==34)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01她被烧死在火刑柱上");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 她被烧死在火刑柱上",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==35)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01英雄们知道了所有灾难发生的原因以及事情的真相");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 英雄们知道了所有灾难发生的原因以及事情的真相",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==36)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01他们必须结束这一切");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 他们必须结束这一切",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==37)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01英雄们听到一个神秘的声音:原来是我");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 英雄们听到一个神秘的声音:原来是我",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}else if(iTC==38)
	{
		ScriptPrintMessageChatAll(" \x0B[\x04故事\x0B] \x01现在享受你的痛苦吧");
		EntFire("Bxzl_Story_Gametext","Addoutput","message 现在享受你的痛苦吧",0.00,null);
		EntFire("Bxzl_Story_Gametext","Display","",0.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",1.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",2.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",3.01,null);
		//EntFire("Bxzl_Story_Gametext","Display","",4.01,null);
	}
}