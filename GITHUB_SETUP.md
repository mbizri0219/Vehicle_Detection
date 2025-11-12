# GitHub Setup Instructions

Your local Git repository is ready! Follow these steps to push it to GitHub:

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name it `vehicle_detection` (or any name you prefer)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Connect and Push to GitHub

After creating the repository, GitHub will show you commands. Use these commands in your terminal:

```bash
cd C:\Object_Detection_Projects\vehicle_detection
git remote add origin https://github.com/YOUR_USERNAME/vehicle_detection.git
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username.

If you're using SSH instead of HTTPS:

```bash
git remote add origin git@github.com:YOUR_USERNAME/vehicle_detection.git
```

## Step 3: Working Between Computers

### On your work computer (after making changes):

```bash
git add .
git commit -m "Description of your changes"
git push
```

### On your laptop (to get the latest changes):

```bash
git pull
```

### First time on laptop (clone the repository):

```bash
cd C:\Object_Detection_Projects
git clone https://github.com/YOUR_USERNAME/vehicle_detection.git
cd vehicle_detection
```

## Important Notes

- **Video files are excluded** from Git (they're too large). If you need to share videos, consider using:

  - Git LFS (Large File Storage)
  - Cloud storage (Google Drive, Dropbox, etc.)
  - A separate data repository

- **Always commit and push** before switching computers
- **Always pull** when you start working on a different computer
