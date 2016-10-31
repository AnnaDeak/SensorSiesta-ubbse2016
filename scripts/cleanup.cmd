@echo off

rem Clean up repository

pushd %~dp0..

rem make sure temp dir is clean
rmdir /s /q .git

rem initialize empty repository, add empty readme file and commit
git init
echo. 2>README.md
git add .
git commit -m "init"

rem set main remote as parameter
git remote add origin https://github.com/csabasulyok/SensorSiesta-ubbse2016
git remote add origin2 https://github.com/csabasulyok/IronHedgehog-ubbse2016
git remote add origin3 https://github.com/csabasulyok/KaPi-ubbse2016
git remote add origin4 https://github.com/csabasulyok/PiPi-ubbse2016

rem force push new DAG into repository
git push -u --force origin master
git push -u --force origin2 master
git push -u --force origin3 master
git push -u --force origin4 master

popd

rem remove temp folder
rm -rf temp