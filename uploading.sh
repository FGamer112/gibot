#!/bin/bash
cd /home/agentk/gitprojects/gibot
git init
git add .
git commit -m 'first commit'
git branch -M main
git remote add origin https://your username:api@github.com/your username/gibot.git
git push https://your username:api@github.com/your username/gibot.git main
