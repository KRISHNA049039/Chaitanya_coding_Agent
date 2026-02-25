# ⚡ Quick Fix: Ctrl+Shift+K Not Working (5 minutes)

## Step 1: Check if Extension is Installed ✓

1. Open VS Code
2. Press **Ctrl+Shift+X** (Extensions)
3. Search: `Kiro`
4. Do you see "Kiro Chat"?

### If YES → Go to Step 2
### If NO → Install Now

```bash
cd kiro-vscode-extension
npm install
npm run package
code --install-extension ./kiro-vscode-extension-0.1.0.vsix
```

Then reload: **Ctrl+Shift+P** → "Reload Window" → Try Ctrl+Shift+K

---

## Step 2: Activate the Extension ✓

1. Press **Ctrl+Shift+P**
2. Type: `Kiro: Start Chat`
3. Press Enter

**Does the chat panel open?**

### If YES ✓
Extension is working! The keybinding might just need activation:
- Close the panel
- Press **Ctrl+Shift+K** now
- It should work!

### If NO ✗
Go to Step 3

---

## Step 3: Reinstall Extension ✓

```bash
# Navigate to extension folder
cd kiro-vscode-extension

# Clean install
rm -rf node_modules
npm install

# Build
npm run package

# Uninstall old version
code --uninstall-extension kiro-vscode-extension

# Install fresh
code --install-extension ./kiro-vscode-extension-0.1.0.vsix
```

Then:
1. Close VS Code completely
2. Reopen workspace
3. Try **Ctrl+Shift+K**

---

## Step 4: Check Prerequisites ✓

Make sure you have:

```bash
# Python 3.8+
python --version

# Node 14+
node --version

# npm 6+
npm --version

# VS Code 1.60+
# Help → About (check version)
```

If any are missing, install them.

---

## Step 5: Try Alternate Method ✓

If keybinding still doesn't work:

1. Press **Ctrl+Shift+P**
2. Type: `Kiro: Start Chat`
3. Hit Enter

This should open the chat. Then bookmark this command for easy access.

---

## 🎯 Success = Chat Panel Opens

You should see:
```
┌─────────────────────────┐
│ 💬 Kiro Chat            │
├─────────────────────────┤
│ (chat messages here)    │
├─────────────────────────┤
│ [input box] [Send][Stop]│
└─────────────────────────┘
```

---

## 💡 If Nothing Works

1. Check full guide: [TROUBLESHOOTING_KEYBINDING.md](TROUBLESHOOTING_KEYBINDING.md)
2. Try dev mode: Open `kiro-vscode-extension` → Press F5
3. Check that Ollama is running: `ollama serve`
4. Verify `.env` file exists in workspace root

---

**Most likely fix: Step 1 (install) or Step 3 (reinstall)**
