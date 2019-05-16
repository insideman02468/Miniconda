#!/bin/#!/bin/sh

git config --global user.name "insideman02468"
git config --global user.email "insideman02468@gmail.com"
git remote add origin https://github.com/insideman02468/Miniconda.git
git status
git checkout master
git add --all
git commit -m "粒子の位置をランダムにリセットを公式通りにしたが、エラー時ランダムポップのほうが良い結果が出る。"
git push origin master
