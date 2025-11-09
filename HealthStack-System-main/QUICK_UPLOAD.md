# ⚡ Quick GitHub Upload Commands

**Fast Track: Upload HealthStack to GitHub**

---

## 🎯 Your GitHub Repository

**URL**: https://github.com/Skismail57/HealthStack-System

---

## 📋 Step-by-Step (Copy & Paste)

### **1. Install Git** (if not installed)

Download and install: https://git-scm.com/download/win

OR use PowerShell (as Administrator):
```powershell
winget install --id Git.Git -e --source winget
```

**Restart PowerShell after installation!**

---

### **2. Configure Git** (First Time Only)

```bash
git config --global user.name "Skismail57"
git config --global user.email "your-email@example.com"
```

---

### **3. Create GitHub Repository**

1. Go to: https://github.com/new
2. Repository name: `HealthStack-System`
3. Description: `Comprehensive Healthcare Management System built with Django`
4. Select: ☑ Public
5. Click: **"Create repository"**

---

### **4. Upload Your Project**

Open PowerShell and run these commands:

```bash
# Navigate to your project
cd "C:\Users\WIN11\Downloads\HealthStack-System-main\HealthStack-System-main"

# Initialize Git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: HealthStack Healthcare Management System"

# Connect to GitHub
git remote add origin https://github.com/Skismail57/HealthStack-System.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### **5. Enter Credentials**

When prompted:
- **Username**: `Skismail57`
- **Password**: Use Personal Access Token (see below)

---

## 🔑 Create Personal Access Token

If GitHub asks for password:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Note: `HealthStack Upload`
4. Expiration: `90 days`
5. Select: ☑ **repo** (all)
6. Click "Generate token"
7. **COPY THE TOKEN** (save it securely!)
8. Use this token as your password when pushing

---

## ✅ Verify Upload

Visit: https://github.com/Skismail57/HealthStack-System

You should see all your files!

---

## 🔄 Future Updates

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

---

## 🆘 Troubleshooting

**Git not recognized?**
- Install Git and restart PowerShell

**Permission denied?**
- Use Personal Access Token, not password

**Need help?**
- See full guide: `GITHUB_UPLOAD_GUIDE.md`

---

**🚀 That's it! Your project will be live on GitHub!**

Your repository: https://github.com/Skismail57/HealthStack-System
