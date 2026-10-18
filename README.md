# CafeCart – Online Café Ordering System

**Student:** Prajapati Bhumika  
**Enrollment No.:** 23ID01IT059  
**Institute:** P.P. Savani University  
**Course:** Diploma in Information Technology  
**Project:** Semester 3 Major/Minor Backlog Project

## About
CafeCart is an original student-level café ordering website built with HTML, CSS, JavaScript, Python Flask and SQLite. It contains a homepage, product menu, search and category filters, a browser-based cart, checkout, order confirmation, and contact/about pages.

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Visual Studio Code
- A modern web browser

## Run on Windows
1. Extract the `CafeCart` folder.
2. Open VS Code and choose **File → Open Folder**, then select `CafeCart`.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```
5. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt in VS Code and run:
   ```cmd
   .venv\Scripts\activate.bat
   ```
6. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
7. Start the website:
   ```powershell
   python app.py
   ```
8. Open `http://127.0.0.1:5000` in your browser.
9. Stop the server with `Ctrl+C` in the terminal.

The SQLite database `cafecart.db` is created automatically when the application starts.

## Features
- 15 sample products in six categories
- Search and category filtering
- Add/remove cart items and change quantities
- Checkout form and server-side price verification
- Orders stored in SQLite
- Order confirmation
- Contact form demonstration
- Responsive layout

## Important notes
- Payment choices are demonstrations only. No payment gateway is connected.
- The contact form displays a demo confirmation; it does not send email or save messages.
- This version does not include user accounts or an admin dashboard.
- The Flask development server is for local project demonstration, not public production hosting.
- Before deployment, replace `app.secret_key` with a strong random secret stored outside the source code.
- The design, text and layout are written for this project. Product illustrations use Unicode symbols rather than copied brand assets.
