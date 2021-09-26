# X社区 CSGO ZE地图参数/地图翻译/Stripper/Entwatch 仓库 【公开】 #
[私密仓库 如您有权限访问](https://github.com/MapTextLang/MapTextLang/)
---
非ZE服务器请前往以下地址:
[公开仓库](https://github.com/e54385991/GeneralMapcfg_Public) ||||
[私密仓库 如您有权限访问](https://github.com/e54385991/GeneralMapcfg)


#### 文件验证同步是否成功判断【限当前地图】


1. sm_findentitybytargetname 指令可以检查同步实体targetname情况 [权限等级:OP]
;例如 sm_findentitybytargetname 20191111 如果当前地图存在包含此实体的targetname 那么都会显示出来
;没有找到则不会输出任何东西

2. sm_gitsync_check_cureentmap_user 指令可以检查同步情况含文件MD5/CRC 修改时间等 [权限等级:任何玩家 间隔限制 300秒]
3. sm_gitsync_check_cureentmap 指令可以检查同步情况含文件MD5/CRC 修改时间等 [权限等级:OP 或 已认证Mapper用户]

## 参数修改规则

游戏平衡性由地图保证，若地图过于不平衡请通知OP进行下架或者调整。一般情况不得额外修改服务器参数；如果出现极度严重不平衡，可以额外修改参数。所有参数修改必须通过PR提交，并且通过OP审核后方可合并到服务器。

包括通过修改stripper修改地图内置参数，神器配置以及地图实体等实现调整地图难度也需要提供修改理由

**所有参数修改必须说明原因 任何掺杂个人因素的修改全部驳回**

**不得应个人要求 个人喜欢,等个人因素 而设定参数**

修改必须填写Commit信息的标题和修改内容，否则系统不同步（除地图翻译除外）。如果需要附加额外信息，请在Pull request 请求里面说明。

## Stripper 修改说明

保证Stripper修改的稳定性以及避免引起服务器崩溃，需先测试Stripper再部署到正式服务器。

在 Commit 标题附加内容 test 或 alpha 或 beta 任一关键词 用于同步到测试服上。确认测试完毕工作正常后 不包含之前关键词 后再 Commit 一次 可同步到正式服.

## 使用说明

| 对应目录 | 说明                                                                       |
|----------|----------------------------------------------------------------------------|
| mapcfg   | [地图参数](https://github.com/e54385991/UPKK_ZE_PUBLIC/blob/master/参数说明.md)       |
| mappool  | [地图池控制系统](https://github.com/e54385991/UPKK_ZE_PUBLIC/blob/master/其他修改说明.md) |
| entwatch | [神器显示配置](https://github.com/e54385991/UPKK_ZE_PUBLIC/blob/master/其他修改说明.md)   |
| maptext  | [ZE地图翻译](https://github.com/e54385991/UPKK_ZE_PUBLIC/blob/master/其他修改说明.md)     |
| 翻译原文下载  | [ZE地图翻译 原文下载 请使用右键另存为保存文件](http://demo.wc38.com/ze-maptext-id-2539/)     |
| bosshit  | [BOSS攻击奖励](https://github.com/e54385991/UPKK_ZE_PUBLIC/blob/master/其他修改说明.md)   |
| scripts  | [vscript脚本提交](https://github.com/e54385991/UPKK_ZE_PUBLIC/blob/master/scripts/vscripts/README.md)   |
| private_stripper_uploader.json  | [根据论坛UID允许上传私有Stripper](https://bbs.upkk.com/plugin.php?id=xnet_mappost:p_stripper_post)    |


---

## 游戏中自动同步说明

### 如果这里文件和服务器文件大小写不匹配 将无法同步成功 请务必通过[论坛查询地图](https://bbs.upkk.com/plugin.php?id=xnet_mappost:xnet_map_query)文件名!

1. 更新/添加修改/你想要的 通过创建 [Pull requests](https://github.com/MapTextLang/MapTextLang/pull/new/master)。就是通过编辑文件后创建PR

2. 当您提交Pull Request后 在管理通过后 在论坛会 [显示事件](https://bbs.upkk.com/plugin.php?id=xnet_events:xnet_events). 应该会显示事件 如果没有显示 可能没有成功 请加上一些无用注释 如`//`再提交一次 和原不同即可)

3. 游戏服务器会每隔地图更换 自动检测修改并同步 op / mapper可以输入 !git_update 强行同步 【同步后仍需要换一次该地图方可生效】
**请不要在修改后的 10分钟内强制同步，因为数据尚未缓存而造成无法更新**

1. 系统会在每日凌晨 3 点自动更新前一天数据

2. 只要对应服务器具备相应地图就会同步本仓库数据

### 仓库维护 一般每月一次

编辑 README.md 在尾部 添加任何无用注释内容
编辑原因填写为 "triggercleanup" 即可清理同步缓存
如果因为文件名错误  或者 小大写错误 则必须执行清理同步缓存

#trigger update11
test for web hook triggercleanup
#push trigger update p 3
triggercleanup  最后维护
    2021年09月26日
#push
