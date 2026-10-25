# Rankrush Speed Test

A small Flask speed-test demo branded for Rankrush and deployable to Vercel.

## Project structure

- `app.py` Flask endpoints
- `templates/index.html` user interface
- `static/assets/rankrush-logo.png` logo
- `static/assets/rankrush-icon.png` favicon
- `requirements.txt` Python dependency
- `.python-version` Python runtime

## Deploy to Vercel

1. Upload the contents of this folder to the root of your GitHub repository. Make sure `app.py`, `requirements.txt`, `.python-version`, `templates/`, and `static/` are at the repository root.
2. In Vercel, import the repository or redeploy the latest commit.
3. Open the deployment URL and hard-refresh with `Ctrl+Shift+R`.

## Measurement limitations

This is an estimate of the browser-to-Vercel-server route, not a full ISP-grade speed test. Each transfer is limited to 4 MiB because Vercel Functions have request/response payload limits. The browser takes three download trials and three upload trials and uses the median to reduce the influence of a single outlier. Response time is HTTP latency to this app, not ICMP ping.

On fast connections, short serverless transfers can still under-report or vary because of serverless startup, request overhead, routing, and the location/capacity of the Vercel function. For more reliable ISP-level measurements, use a dedicated speed-test backend with larger transfers and geographically distributed test servers. Do not interpret this app's numbers as guaranteed exact results.

## Local development

```bash
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. The UI intentionally disables tests on localhost because localhost testing does not measure the internet route.
