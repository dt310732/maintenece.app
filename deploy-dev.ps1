# deploy-dev.ps1

git add .
git commit -m "dev update"
git push

ssh dev@192.168.101.2 "cd /opt/cmms && git pull --ff-only && docker compose up -d --build"