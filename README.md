# Project A.C.T. — Action Changes Things

A employee-led Corporate Social Responsibility initiative website for Revital Healthcare (EPZ) Ltd.

## 🚀 Deploy to Netlify via GitHub

### **Step 1: GitHub Setup**

```bash
# 1. Initialize git (if not already)
git init

# 2. Add all website files
git add *.html css/ js/ Images/

# 3. Commit
git commit -m "Initial website deployment"

# 4. Create a new repository on GitHub
# Go to https://github.com/new and create a repo (e.g., "project-act-website")

# 5. Link your local repo to GitHub
git remote add origin https://github.com/YOUR-USERNAME/project-act-website.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

### **Step 2: Netlify Setup**

1. **Sign up / Log in to Netlify**: https://app.netlify.com

2. **Connect your GitHub repo**:
   - Click "Add new site" → "Import an existing project"
   - Connect your GitHub account
   - Select your repository

3. **Configure build settings**:
   - **Build command**: `npm run build` (leave empty - no build needed for static site)
   - **Publish directory**: `.` (current directory - all files are at root)
   - **Build status**: Skip build step ✅

4. **Deploy**:
   - Click "Deploy site"
   - Your site will be live at a random URL (e.g., `https://project-act.netlify.app`)

### **Step 3: Custom Domain (Optional)**

1. In Netlify Dashboard → "Domain settings"
2. Click "Add custom domain"
3. Enter your domain (e.g., `projectact.or.ke` or `revitalhealthcare.com`)
4. Follow DNS configuration instructions

### **Step 4: Automatic Deployments**

After initial setup, any changes pushed to GitHub will automatically deploy:

```bash
# Make changes to your website
git add .
git commit -m "Update content"
git push
# Netlify auto-deploys within seconds!
```

---

## 📁 Project Structure

```
ACT WEB/
├── index.html              # Homepage
├── copacabana.html         # Phase 02
├── kuruitu.html            # Phase 03
├── vipingo.html            # Phase 04
├── eye-camp.html           # Phase 05
├── world-environment-day.html # Phase 06
├── archive.html            # Full archive
├── infrastructure.html       # Infrastructure details
├── css/
│   ├── index.css
│   ├── copacabana.css
│   └── ... (other stylesheets)
├── js/
│   └── main.js
└── Images/
    └── (all website images)
```

---

## 🎯 Quick Start

Just open `index.html` in any browser - no server required! For production, deploy to Netlify for global CDN, HTTPS, and automatic deployments.