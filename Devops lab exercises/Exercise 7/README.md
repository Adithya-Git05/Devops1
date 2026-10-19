# Exercise 7 — Jenkins Installation and CI/CD Introduction

## Requirements

- Docker Desktop running with the Linux container engine.
- Host ports 8080 and 50000 available.

## Start Jenkins

From this folder, run:

```powershell
docker compose up -d
docker compose ps
```

Open <http://localhost:8080>. On first startup, retrieve the one-time unlock
password with:

```powershell
docker compose exec jenkins `
  cat /var/jenkins_home/secrets/initialAdminPassword
```

Complete the Jenkins setup wizard and install the suggested plugins. Keep the
password private; do not put it in source control or screenshots.

Stop the container with `docker compose down`. The named `jenkins-home` volume
keeps the Jenkins configuration for the next run.
