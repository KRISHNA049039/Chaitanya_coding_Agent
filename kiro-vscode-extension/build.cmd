@echo off
REM Package the extension as VSIX (Windows batch script)

setlocal enabledelayedexpansion

echo 🔨 Building Kiro VS Code Extension...

where npm >nul 2>nul
if errorlevel 1 (
  echo ❌ npm is not installed. Please install Node.js and npm.
  exit /b 1
)

echo 📦 Installing dependencies...
call npm install

echo 📦 Packaging extension...
call npx vsce package

echo ✅ Done! Generated: kiro-vscode-extension-*.vsix
echo.
echo To install locally:
echo   code --install-extension ./kiro-vscode-extension-*.vsix
echo.
echo To publish to Marketplace:
echo   npx vsce publish
