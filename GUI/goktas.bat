@echo off
title Goktas AGV

REM Flutter SDK path (change this if necessary)
set flutter_sdk=C:\src\flutter

REM App path (change this if necessary)
set app_path=C:\GoktasAGV\GUI\GUI

cd %app_path%

REM Add Flutter to the system path
set path=%flutter_sdk%\bin;%path%

REM Run the app
flutter run -d chrome --web-renderer html
