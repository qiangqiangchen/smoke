@echo off
echo "开始测试，请等待...."

taskkill /F /T /IM node.exe
ping -n 5 127.0.0.1>nul
cmd /c start node E:\Appium\node_modules\appium\bin\appium.js --no-reset
ping -n 10 127.0.0.1>nul

echo "测试完成，请查看结果报告。"
pause