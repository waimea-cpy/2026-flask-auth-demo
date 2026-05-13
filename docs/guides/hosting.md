# Hosting Your App on Render

There are various places that you can host a Flask app, but many are paid-only. One service that will host a simple Flask app for free is [Render](https://render.com)

Render makes hosting very simple:
- Links directly to your GitHub repo
- Very simple setup and configuration
- Re-deploys the app every time you push a change to the repo


## Create an Account at Render

1. Go to [Render](https://render.com/) and **Sign in with GitHub**
2. Sign up for the **Hobby ($0) plan**


## Deploying Your App

### Create the Web App

1. Create a new **Web Service**
2. To see your list of **GitHub repos**, you will need to add credentials so that Render has access to your repos.
3. Select the project repo


### Configure the Web App

1. In the deployment settings, set the following:

    - Name: Can customise if you wish
    - Language: **Python 3**
    - Branch: **main**
    - Region: **Singapore**
    - Root Directory: *Leave blank*
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `flask run`
    - Instance Type: **Free**
    - Environment Variables (copy/paste from your `.env` file to start):
        - `FLASK_SECRET_KEY`  *Something long and random*
        - `DEFAULT_TIMEZONE`  **Pacific/Auckland**
        - `LOCAL_DB_PATH`     **app/db/data.sqlite**
        - `FLASK_RUN_HOST`    **0.0.0.0**
        - `FLASK_RUN_PORT`    **10000**
        - `FLASK_DEBUG`       **False**
        - Any other vars required, e.g. `ADMIN_PASSWORD`

2. **Deploy** the web service, and it should be good to go!


### Access the Deployed App

In the Render dashboard:
- Go to your web app
- Note the the **public URL** generated for the deployed app
- Open this URL in a browser and save it for future reference


### Updating the Deployed App

Every time you **push changes** to your GitHub repo, Render will **automatically re-deploy** the app - there is nothing you need to do.


## Limits of Free Hosting on Render

The free service has some limitations:
- App 'powers down' after an idle period of about 30mins
- When 'powered down', the app can take about half a minute to restart
- When it 'powers down', updates to files (e.g. the SQLite database) are **discarded**
- When restarted, the app re-uses the files from the repo (including the SQLite database) as it was last pushed to GitHub, so the app **restarts in the same state each time**.

*These limitations are fine for a 'toy app', but you would need to look at different hosting if you needed to retain database updates.*

