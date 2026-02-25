#!/usr/bin/env bash
# Package the extension as VSIX

set -e

echo "🔨 Building Kiro VS Code Extension..."

# Check if npm/node are available
if ! command -v npm &> /dev/null; then
  echo "❌ npm is not installed. Please install Node.js and npm."
  exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the extension
echo "📦 Packaging extension..."
npx vsce package

echo "✅ Done! Generated: kiro-vscode-extension-*.vsix"
echo ""
echo "To install locally:"
echo "  code --install-extension ./kiro-vscode-extension-*.vsix"
echo ""
echo "To publish to Marketplace:"
echo "  npx vsce publish"
