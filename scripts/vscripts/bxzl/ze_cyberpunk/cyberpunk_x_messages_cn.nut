White           <- " \x01 "; 
DarkRed         <- " \x02 ";
Purple          <- " \x03 ";
Green           <- " \x04 "; 
BrightGreen     <- " \x05 ";
Lime            <- " \x06 "; 
Red             <- " \x07 "; 
Silver          <- " \x08 ";
BrightYellow    <- " \x09 "; 
Yellow          <- " \x10 "; 
BrightSilver    <- " \x0A "; 
Blue            <- " \x0B "; 
DarkBlue        <- " \x0C "; 
DarkSilver      <- " \x0D "; 
PurplePinkish   <- " \x0E ";
BrightRed       <- " \x0F "; 

/*
function Example()
{
	ScriptPrintMessageChatAll(DarkSilver + "A" + Red + "Torch" + DarkSilver + "has been lit.");
}
*/


//***************General messages
function AIXTrappedPlayer()
{
	ScriptPrintMessageChatAll(DarkRed+"[人工智能X]"+DarkSilver+"击毙了"+Blue+"一位人类.(不要乱贴门)");
}
function PlayerTouchedWater()
{
	ScriptPrintMessageChatAll(DarkRed+"一位玩家"+DarkSilver+"失去了自己的"+Blue+"生命"+DarkSilver+"(由于掉进水里).");
}
function TeleportAdvance(value)
{
	if(value == null)
		return;
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"传送即将在"+Red+value.tostring()+" 秒后激活.");
}
function FailMessage()
{
	ScriptPrintMessageChatAll(Red+"损坏的人类(僵尸)触发了开关,回合失败....");
}
function StageMessage(currentStage)
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkBlue+"当前关卡--"+currentStage.tostring());
}
//***************


//-----------
function StartMessage()
{
	ScriptPrintMessageChatAll(DarkSilver + "地图作者:" + PurplePinkish + "๖ۣۜDemon" + DarkSilver + "和" + PurplePinkish + "iXi");
	ScriptPrintMessageChatAll(DarkSilver + "翻译:" + PurplePinkish + "冰雪葬泪");
}
//-----------
function Lvl1SlideDoorMessage()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"城市滑动门将于"+Blue+"30 秒后打开.");
}

function Lvl1Tip1Message()
{
	ScriptPrintMessageChatAll(DarkRed+"[提示]:"+DarkSilver+"躲避 人工智能X 的"+Blue+"监视眼.");
}
//-----------
function Lvl1Trigger1Message()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"路障似乎已经充满了电...去周围寻找它的"+Blue+"电源电池"+DarkSilver+"并将电池摧毁");
}

function Lvl1Trigger1Message2()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"电源电池"+DarkSilver+"正在放电(释放电能）.");
}
//-----------
function Lvl1Trigger2Message()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"面前这个操作面板好像坏了..但是似乎"+Blue+"门后面的那个操作面板是"+DarkSilver+"好的.");
}
//-----------
function Lvl1Trigger3Message()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"这个"+Blue+"电源电池"+DarkSilver+"是给"+Blue+"这两扇门供电的."+DarkSilver+" 但它似乎超载了."+Red+"射击"+DarkSilver+"它,以使得电池放电.");
}
//-----------
function Lvl1Trigger4_1Message()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"给这些路障供电的"+Blue+"电源电池"+DarkSilver+"似乎不在这外面..."+Blue+"它很有可能在"+PurplePinkish+"地下.."+PurplePinkish+"寻找能去往底下的方法.");
}
function Lvl1Trigger4_1Message2()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"这些路障即将解锁..");
}

//-----------
function Lvl1Trigger4MessageFirst()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"可恶...又是一扇关闭的门.., 旁边"+Blue+"右侧的管道"+DarkSilver+"似乎可以攀爬.");
}
function Lvl1Trigger4Message()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"看起来我们需要一个人去破坏"+Blue+"位于另一边的电源电池.");
}
//-----------
function Lvl1TriggerFinal1()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"城市已经完全封锁了.唯一能够逃出的方式就是 "+Blue+"车"+DarkSilver+"但是我们怎样能找到一辆车呢?.");
}

function Lvl1TriggerFinal2()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"似乎这个建筑物就是我们要找的地方! 我们应该能找到一辆 "+Blue+" 车"+DarkSilver+",在这里的顶层");
}

function Lvl1TriggerFinalElevator(value)
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"这个"+Blue+"电梯"+DarkSilver+"即将前往"+Blue+"第"+value.tostring()+"层.");
}

function Lvl1TriggerFinal3()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"然而, 这里的"+Blue+"安全系统按钮"+DarkSilver+"是在"+Blue+"上面一层."+DarkSilver+"或许我们能穿过"+Blue+"餐厅"+DarkSilver+"到达那里");
}
function Lvl1TriggerFinal4()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"我们得给"+Blue+"这个车充电.");
}
function Lvl1TriggerFinal5()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"车"+DarkSilver+"正在"+Blue+"充电中.");
}
function Lvl1TriggerFinal6()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"车电"+DarkSilver+"几乎要充满了"+Blue+"快上车!");
}
//---------- previus trigger messages above this, just to keep it in order.

function Lvl1SuccessfullyEnteredCodeMsg()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"密码已"+Green+"成功"+DarkSilver+"输入.....大门即将打开...");
}

function Lvl1WrongCodeMessage()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Red+"错误的密码");
}

function Lvl1BoatTrigger1Message()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"情报告诉我们"+Blue+"检查点"+DarkSilver+"需要一个"+Blue+"密码"+DarkSilver+"来打开"+Blue+"大门."+DarkSilver+"我们可以在"+Blue+"右边建筑物里"+DarkSilver+"找到那个密码.");
}
function Lvl1BoatTrigger1_1Message()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"或许我们能让人搭乘"+Blue+"这个小船"+DarkSilver+"去对岸进入"+Blue+"那个建筑物里寻找密码."+DarkSilver+"其他人从陆路前进"+PurplePinkish+"去输入"+DarkSilver+"密码开门.");
}
function Lvl1BoatTrigger2Message()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"小船"+DarkSilver+"似乎"+Blue+"没有燃料..."+DarkSilver+"我们能用"+Blue+"燃料桶"+DarkSilver+"给船加油,燃料在左边.");
}
boatFuel <- 0;

SuccessfullyFueledTheBoat <- false;

function Lvl1BoatFill(amountToAdd)
{
	boatFuel += amountToAdd;
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"船燃料已达"+Blue+boatFuel.tostring()+"%");
	if(boatFuel >= 100)
	{
		SuccessfullyFueledTheBoat = true;
	}
}
function CheckBoatFuel()
{
	if(!SuccessfullyFueledTheBoat)
	{
		EntFireByHandle(caller,"FireUser1","",0.00,null,null);
	}
}
function Lvl1BoatFilled()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"船即将在"+Blue+"5 秒后离开");
}

//---------------------------Level 2 Messages---------------------------

function Lvl2Start()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"我们得坐"+Blue+"火车"+DarkSilver+"前往那座塔."+DarkRed+"人工智能X"+DarkSilver+"就在里面.");
}
function Lvl2Trigger1_1()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"可恶...似乎我们无法乘坐地铁.");
}
function Lvl2Trigger1_2()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"情报告诉我们"+Blue+"可以乘坐墙对面的货运火车."+DarkSilver+"如果我们能够翻过"+Blue+"这个墙壁..."+DarkSilver+"然我们去"+Blue+"顶部的控制室看看"+DarkSilver+".");
}
function Lvl2Trigger2()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"似乎他们正在修复"+Blue+"路障的电路"+DarkSilver+","+Red+"破坏这个保险丝"+DarkSilver+"应该能有效果.");
}
function Lvl2Trigger2_1()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"路障"+DarkSilver+"即将打开.");
}
function Lvl2Trigger3()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"在发电室里有一个"+Blue+"控制板"+DarkSilver+", 或者它能够控制"+Blue+"顶楼的路障"+DarkSilver+".");
}
function Lvl2Trigger3_1()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"路障"+DarkSilver+"即将打开.");
}
function Lvl2Trigger4()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"控制室的大门似乎被"+Red+"封死了..."+DarkSilver+"我们需要一个人穿过"+Blue+"那个打开的排气口"+DarkSilver+", 这样我们或许能够从"+Blue+"另一边"+DarkSilver+"打开.");
}
function Lvl2Trigger5()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"一个"+Blue+"货运火车"+DarkSilver+"即将经过这里...我们必须加快脚步.");
}
function Lvl2Trigger5_1()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"我们应该能够关闭"+Blue+"安全系统"+DarkSilver+"以防在后面的路上出现什么东西.");
}
function Lvl2Trigger5_2()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"安全系统"+DarkSilver+"正在"+Red+"关闭"+DarkSilver+"但它完全关闭需要一些"+Blue+"时间"+DarkSilver+", 让我们进入"+Blue+"下水道"+DarkSilver+",在这个墙边上的洞里.");
}
function Lvl2Trigger5_3()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"安全系统"+DarkSilver+"正在"+Red+"关闭"+DarkSilver+", 坚守这里直至"+Blue+"滑动门"+DarkSilver+"打开.");
}
function Lvl2Trigger5_4()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"滑动门正在打开"+DarkSilver+", 让我们继续前往"+Blue+"顶楼."+DarkSilver+"通过"+Blue+"梯子"+DarkSilver+",它在右边.");
}
function Lvl2Trigger5_5()
{
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+Blue+"火车"+DarkSilver+"马上要到了,准备往下跳.");
}

function Lvl2IncomingTunnel() {
	ScriptPrintMessageChatAll(Red+"[警告]:"+DarkSilver+"出现 "+Red+"通道凸起部分"+DarkSilver+"! 保持蹲下!");
}

function Lvl2IncomingZombieBikeA() {
	ScriptPrintMessageChatAll(Red+"[警告]:"+DarkSilver+"出现 "+Red+"僵尸自行车"+DarkSilver+"! 快防守!");
}

function Lvl2IncomingZombieHelicopter() {
	ScriptPrintMessageChatAll(Red+"[警告]:"+DarkSilver+"出现 "+Red+"僵尸飞机"+DarkSilver+"! 快防守!");
}

function Lvl2IncomingHelicopter() {
	ScriptPrintMessageChatAll(Red+"[警告]:"+DarkSilver+"出现 "+Red+"飞机"+DarkSilver+"! 快到中间去!");
}

function overallDefendMsg() {
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]:"+DarkSilver+"防守住火车! 4节火车都必须守住!");
}

function stageFailedTrain() {
	ScriptPrintMessageChatAll(Red+"[地图信息] 你们没能防守住火车,GG!!!");
}

function stageFailedTrain1() {
	ScriptPrintMessageChatAll(Red+"[地图信息] 人工智能X 发现了火车,GG....");
}

function AIXSummonHeliBoss()
{
	ScriptPrintMessageChatAll(DarkRed+"[人工智能X]"+DarkSilver+"召唤了"+Blue+"一个攻击机.");
}

function killBossPls() {
	ScriptPrintMessageChatAll(PurplePinkish+"[地图信息]"+DarkSilver+"快击毁攻击机,否则这个门将会关闭!!");
}

function AIXSummonBackupHeli()
{
	ScriptPrintMessageChatAll(DarkRed+"[人工智能X]"+DarkSilver+"召唤了"+Blue+"一个支援机");
}

function shootTheMissiles() 
{
	ScriptPrintMessageChatAll(Red+"[警告]:"+DarkSilver+"出现 "+Red+"导弹"+DarkSilver+"! 快把它们击毁!!");
}
