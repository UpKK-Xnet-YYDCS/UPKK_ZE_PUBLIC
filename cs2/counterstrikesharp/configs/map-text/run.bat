
@echo off
chcp 65001 >nul
cd /d "%~dp0"

:: 设置虚拟环境文件夹名字
set VENV_DIR=venv

:: 如果虚拟环境不存在就创建
if not exist %VENV_DIR% (
    echo 正在创建虚拟环境...
    py -3 -m venv %VENV_DIR%
)

:: 激活虚拟环境
call %VENV_DIR%\Scripts\activate.bat

:: 升级 pip
python -m pip install --upgrade pip

:: 安装/更新所需包（在这里继续加你需要的包就行）
pip install tqdm requests
:: 如果还有别的包，继续往下一行加，比如：
:: pip install colorama pillow numpy ...

:: 运行你的脚本
echo.
echo 正在运行 ollama_translation_maptext.py ...
python ollama_translation_maptext.py  -r KR JP TW US

:: 运行完毕后暂停，方便你看输出结果
echo.
echo 任务执行完毕，按任意键退出...
pause