# Git and GitHub

## What is Git?

**Git** is a version control system (VCS) that tracks changes to your files over time.

Think of it like a 'save game' feature for your code: You can save snapshots (called 'commits') and go back to any previous version if something breaks.

## What is GitHub?

**GitHub** is a website that stores your Git repositories (repos) online, making it easy to:
- **Back up** your code
- **Access** your code from different computers
- **Share** your code with others
- **Track** your project history

## Key Git Concepts

| Concept               | Definition                                                                                                              |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Repository (repo)** | A collection of files in a folder that Git is tracking. Contains a hidden `.git` folder that stores the version history |
| **Remote**            | The online version of your repository stored on GitHub. Usually called `origin`                                         |
| **Local**             | The version of your repository on your computer. This is the copy that you will work on as you develop your app                                      |
| **Main Branch**       | The primary version of your code, usually called `main`. Other branches can be created if needed                        |
| **Clone**             | Making a copy of a GitHub repository onto your computer for the first time                                              |
| **Commit**            | A snapshot of your files at a specific point in time. Each commit has a message describing what changed                 |
| **Push**              | Sending your local commits up to GitHub (uploading your changes) - You push from local to remote                        |
| **Pull**              | Getting the latest changes from GitHub down to your computer (downloading updates) - You pull from remote to local      |


## Typical Workflows

*Note: To keep things simple, instead of using the `git` command-line tool, we will use **GitHub Desktop**, an easy-to-use Git client with a GUI.*

### Working with a New Repo

1. Create a repo on [GitHub](https://github.com) → Name it, add a description, make it public

2. Open **GitHub Desktop** → **clone** the repo to get a **local copy** to work on

### Working with a Cloned Repo

1. Open **GitHub Desktop**...
   - **Fetch origin** → checks for updates, and if any...
   - **Pull origin** → download any updates

   *Note: You will need to fetch and pull changes from GitHub if you have pushed changes from a different computer, or made changes directly on GitHub's website*

2. Open repo in **VS Code**...
   - Edit code and save changes
   - When you have completed a new feature / bug fix...

3. Switch to **GitHub Desktop**...
   - Review changed files → added (green), edited (yellow), removed (red)
   - Write a clear **commit message**
   - **Commit to main** → snapshot of changes saved locally
   - **Push origin** → Upload changes to GitHub

      *Note: Pushing is optional during a coding session, but **required** at the end, otherwise your work won't be backed-up*

Repeat steps 2 and 3 until your coding session ends. Make sure you push any final commits!


## Tips

**Golden rules** for using Git and GitHub effectively:

- **Commit often**, after every small new feature / bug fix
- Commit all **related changes together**
- Write **clear commit messages**
- **Push regularly**, and **always at the end** of each work session

**Good commit messages** start with a verb and are specific:
- ✅ "Added user registration form"
- ✅ "Fixed database connection error"
- ✅ "Updated homepage styling"
- ✅ "Removed unused CSS files"

**Bad commit messages** are vague and non-specific:
- ❌ "Changes"
- ❌ "Fixed stuff"
- ❌ "Update"

