# Exercise 8 — Hello World Jenkins Job

## Requirements

- Jenkins running and accessible at <http://localhost:8080>.
- Jenkins Git plugin.
- A GitHub repository containing `hello-world.sh`.

## Publish the script

Create a repository in your own GitHub account, then from this folder run:

```sh
git init
git config user.name "Your Name"
git config user.email "you@example.com"
git add hello-world.sh
git commit -m "Add hello-world.sh"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repository>.git
git push -u origin main
```

Use a GitHub credential in Jenkins if the repository is private. Never commit
or paste a personal access token into the repository or the job configuration.

## Configure and verify the Jenkins job

Create a **Freestyle project**, select Git under **Source Code Management**, and
enter the repository URL. Add **Execute shell** with:

```sh
sh hello-world.sh
```

Run **Build Now**. The Console Output should contain `Hello, Jenkins!` and
finish with `Finished: SUCCESS`.
