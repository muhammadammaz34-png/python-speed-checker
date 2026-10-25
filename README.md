# Python Speed Checker for Vercel

## Deploy to Vercel

Vercel supports Flask and can detect the `app` instance in the root `app.py` file automatically.

### Option A: Vercel CLI (recommended if Node.js/npm is installed)

1. Extract this ZIP into a folder, for example `D:\python-speed-checker-vercel`.
2. Open PowerShell in that folder.
3. Install and sign in to the Vercel CLI:

   ```powershell
   npm install -g vercel
   vercel login
   ```

4. Deploy a preview:

   ```powershell
   vercel
   ```

   Follow the prompts. For a new project, accept the suggested project settings. Do not add a custom build command or output directory.

5. If the preview URL works, deploy production:

   ```powershell
   vercel --prod
   ```

6. Open the public HTTPS URL Vercel prints and run the test there. The test is intentionally disabled on `localhost`.

### Option B: Git repository

1. Create a repository on GitHub.
2. Upload the contents of this folder to the repository root (the `app.py`, `requirements.txt`, `.python-version`, and `templates` folder must be at the root).
3. In Vercel, choose **Add New → Project**, import the repository, and deploy with the default settings.
4. Open the deployed HTTPS URL.

## Important measurement limitations

- Vercel Functions have a maximum request or response payload of 4.5 MB, so the app uses 4 MiB download and upload transfers.
- These small payloads can underestimate speeds on fast connections because the test is short.
- The measurement represents the path from the visitor's browser to the Vercel function, not a definitive measurement of the visitor's ISP line rate.
- HTTP response time is not ICMP ping.
- The in-memory rate limiter is per instance and is not a complete public-abuse safeguard.
- For a production-grade speed-test service, use a purpose-built test server or CDN/object-storage transfer endpoints and distributed measurement locations.

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. The browser UI explains why the speed test is disabled locally.
