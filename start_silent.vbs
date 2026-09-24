Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "c:\PROJECTS\English_Learning_Bot"
WshShell.Run "python run.py", 0, False
