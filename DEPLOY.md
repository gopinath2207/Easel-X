# Deploying to Render

This guide explains how to deploy your Django project to Render for free.

## Prerequisites

1.  **GitHub Account**: You need a GitHub account to connect to Render.
2.  **Render Account**: Sign up at [render.com](https://render.com/).

## Steps

### 1. Push to GitHub

Make sure your code is pushed to a GitHub repository.

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. Create a Web Service on Render

1.  Go to your [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub repository.
4.  Configure the service:
    *   **Name**: Choose a name for your app (e.g., `easelx`).
    *   **Region**: Select the region closest to you.
    *   **Branch**: `main` (or your default branch).
    *   **Root Directory**: Leave empty (since `manage.py` is in the root).
    *   **Runtime**: `Python 3`.
    *   **Build Command**: `./build.sh`
    *   **Start Command**: `gunicorn EaselX.wsgi`
    *   **Instance Type**: Select **Free**.

### 3. Configure Environment Variables

Scroll down to the **Environment Variables** section and add the following:

| Key | Value |
| :--- | :--- |
| `PYTHON_VERSION` | `3.10.0` (or your local version) |
| `SECRET_KEY` | Generate a strong random string (you can use an online generator). |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*` (or your Render URL, e.g., `easelx.onrender.com`) |
| `DATABASE_URL` | (See next step) |

### 4. Create a Postgres Database

1.  Open a new tab and go to your [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** and select **PostgreSQL**.
3.  Configure the database:
    *   **Name**: `easelx-db`
    *   **Instance Type**: Select **Free**.
4.  Click **Create Database**.
5.  Once created, copy the **Internal Database URL**.
6.  Go back to your Web Service settings (Environment Variables).
7.  Add a new variable:
    *   **Key**: `DATABASE_URL`
    *   **Value**: Paste the Internal Database URL you copied.

### 5. Deploy

1.  Click **Create Web Service** (or **Save Changes** if you're editing).
2.  Render will start building your app. You can watch the logs in the dashboard.
3.  Once the build finishes, your app will be live at the provided URL (e.g., `https://easelx.onrender.com`).

## Troubleshooting

-   **Build Failures**: Check the logs. Common issues include missing dependencies in `requirements.txt` or errors in `build.sh`.
-   **Database Errors**: Ensure `DATABASE_URL` is correct and the database is running.
-   **Static Files**: If images/CSS are missing, check if `collectstatic` ran successfully in the build logs.
