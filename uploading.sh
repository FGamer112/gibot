#!/bin/bash
cd /home/fgamer112/gitprojects/gibot
git init
git add .
git commit -m 'first commit'
git branch -M main
git remote add origin https://123:123@github.com/123/gibot.git
git push https://123:123@github.com/123/gibot.git main
