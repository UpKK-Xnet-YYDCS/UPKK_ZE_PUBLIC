# X社区 CS2 ZE地图参数/地图翻译/Stripper/Entwatch 仓库【公开】 #
[CS2ZE配置](https://github.com/UpKK-Xnet-YYDCS/UPKK_ZE_PUBLIC/tree/master/cs2)




- [私有仓库(通常用于Stripper) 
- 如您有权限访问](https://github.com/UpKK-Xnet-YYDCS/ZE_Stripper_Vscript)

# 非ZE服务器请前往以下地址:
- [公开仓库](https://github.com/UpKK-Xnet-YYDCS/GeneralMapcfg_Public)  
- [私有仓库 如您有权限访问](https://github.com/UpKK-Xnet-YYDCS/GeneralMapcfg)


# Actions 脚本说明
| YML 文件名                                 | 用途/说明                                     |
|-------------------------------------------|--------------------------------------------|
| DownloadMapPreviewImagesMapPingJSON.yml   | 用于自动下载地图预览图片,并将其上传UPKK服务器 以实现完全自动化 https://servers.upkk.com 地图预览图   |
| check_workshop_collection_not_in_file.yml | 检查创意工坊合集订阅存在,但是maps.txt已经移除的情况         |
| check_workshop_ids.yml                    | 用于检查地图创意工坊中是否还有效例如是否被下架地图等。            |
| check_workshop_in_collection.yml         | 检查地图是否已被加入创意工坊集合中。               |
| deleteWorkflowRun.yml                     | 用于自动清理工作流的运行记录。                   |
| valid_json.yml                           | 注释文件，包含 JSON 数据验证规则    |
| ollama-automatic-translate.yml           | 使用upkk自拓管github runner运行器,在upkk的自拓管AI服务器使用特定模型自动化翻译地图语言并自动提交PR 注:依赖Upkk 部署AI的服务器在线状态  |



