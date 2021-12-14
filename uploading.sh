#!/bin/bash
cd /home/agentk/gitprojects/gibot/voc
git init
git add .
git commit -m 'first commit'
git branch -M main
git remote add origin https://FGamer112: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@github.com/FGamer112/voc.git
git push https://FGamer112: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@github.com/FGamer112/voc.git main
