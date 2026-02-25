# 🔧 Troubleshooting: Ctrl+Shift+K Not Working

If pressing `Ctrl+Shift+K` (or `Cmd+Shift+K` on Mac) doesn't open Kiro Chat, follow these steps:

## ✅ Checklist

### 1. Is the extension installed?

**Check:**
1. Open VS Code
2. Press **Ctrl+Shift+X** (Extensions panel)
3. Search for **"Kiro"**
4. Look for "Kiro Chat" in the list

**If NOT installed:**
→ Jump to [Installation Steps](#-installation-steps)

**If installed but disabled:**
1. Click **Enable** button next to "Kiro Chat"
2. Reload VS Code: Ctrl+Shift+P → "Developer: Reload Window"

---

## 📦 Installation Steps

### Option A: Build & Install from VSIX (Recommended)

1. **Open terminal** in the `kiro-vscode-extension` folder:
   ```bash
   cd kiro-vscode-extension
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Build the extension**:
   ```bash
   npm run package
   ```
   This creates `kiro-vscode-extension-0.1.0.vsix`

4. **Install the VSIX**:
   ```bash
   code --install-extension ./kiro-vscode-extension-0.1.0.vsix
   ```

5. **Reload VS Code**:
   - Close all VS Code windows
   - Reopen the workspace

6. **Test**: Press `Ctrl+Shift+K`

---

### Option B: Development Mode (F5)

If you want to test without installing:

1. **Open** `kiro-vscode-extension` folder in VS Code
2. **Press F5** to launch Extension Development Host
3. A new VS Code window opens with the extension active
4. **Press Ctrl+Shift+K** in the dev window

---

### Option C: Reinstall

If already installed but not working:

1. **Uninstall**:
   - Ctrl+Shift+X → Find "Kiro Chat" → Click **Uninstall**

2. **Reload**: Ctrl+Shift+P → "Developer: Reload Window"

3. **Rebuild**:
   ```bash
   cd kiro-vscode-extension
   npm install
   npm run package
   ```

4. **Reinstall**:
   ```bash
   code --install-extension ./kiro-vscode-extension-0.1.0.vsix
   ```

5. **Test**: Press `Ctrl+Shift+K`

---

## 🔍 Verify Keybinding

### Check if keybinding is registered:

1. Press **Ctrl+Shift+P** (Command Palette)
2. Type: `Keyboard Shortcuts`
3. Click: `Preferences: Open Keyboard Shortcuts (JSON)`
4. Search for `kiro.startChat`
5. Should show:
   ```json
   {
     "key": "ctrl+shift+k",
     "command": "kiro.startChat"
   }
   ```

### If not listed:

The extension may not be activated. Try:
- **Ctrl+Shift+P** → type `Kiro: Start Chat`
- This will activate the extension
- Then try `Ctrl+Shift+K` again

---

## 🧪 Test the Extension

### Method 1: Command Palette

1. Press **Ctrl+Shift+P**
2. Type: `Kiro: Start Chat`
3. Press Enter
4. Should open chat panel on the right

**If this works:** The extension is active, just the keybinding might need reload

---

### Method 2: Check Extension is Active

1. Press **Ctrl+Shift+P**
2. Search: `Developer: Show Running Extensions`
3. Look for `kiro-vscode-extension` in the list
4. If not listed, extension isn't active

**Fix:** Run any Kiro command to activate it, then try keybinding

---

## 🆘 Common Issues & Fixes

### Issue 1: "npm: command not found"

**Solution:**
- Install Node.js from https://nodejs.org/
- Add to PATH
- Test: `node --version` and `npm --version`

### Issue 2: "vsce: command not found"

**Solution:**
```bash
cd kiro-vscode-extension
npm install
npm run package
```

### Issue 3: VSIX file not found

**Solution:**
```bash
cd kiro-vscode-extension
ls *.vsix  # Check if file exists
npm run package  # Rebuild if missing
```

### Issue 4: Keybinding conflicts

**Solution:**
1. Ctrl+Shift+K might be used by another extension
2. Check: Ctrl+Shift+P → "Preferences: Open Keyboard Shortcuts (JSON)"
3. Search for `ctrl+shift+k` to find conflicts
4. Remap Kiro to a different key:
   ```json
   {
     "key": "ctrl+alt+k",
     "command": "kiro.startChat"
   }
   ```

### Issue 5: Extension installed but not working after update

**Solution:**
1. Uninstall: Ctrl+Shift+X → Find Kiro Chat → Uninstall
2. Reload: Ctrl+Shift+P → "Developer: Reload Window"
3. Clear cache: `rm -rf ~/.vscode/extensions/kiro*` (macOS/Linux)
4. Reinstall: `code --install-extension ./kiro-vscode-extension-*.vsix`

---

## 📋 Full Troubleshooting Checklist

Use this checklist in order:

- [ ] Extension "Kiro Chat" appears in Extensions panel (Ctrl+Shift+X)
- [ ] Extension is **Enabled** (not Disabled)
- [ ] Ctrl+Shift+P → "Kiro: Start Chat" **works**
- [ ] Chat panel opens on right side
- [ ] Ctrl+Shift+K **now works**

If any step fails, follow the instructions above.

---

## 🐛 Debug Mode

### Step-by-step debugging:

1. **Open Developer Tools**:
   - Ctrl+Shift+P → "Developer: Toggle Developer Tools"

2. **Open Console tab** (should be already visible)

3. **Watch for errors** when you:
   - Press Ctrl+Shift+K
   - Run "Kiro: Start Chat" command
   - Try to send a message

4. **Copy any errors** and check:
   - [EXTENSION_USAGE_GUIDE.md](EXTENSION_USAGE_GUIDE.md#troubleshooting)
   - [EXTENSION_FEATURES.md](EXTENSION_FEATURES.md#-debugging)

### Common error messages:

| Error | Meaning | Fix |
|-------|---------|-----|
| "Cannot find module 'child_process'" | Extension not loading correctly | Reinstall extension |
| "Error spawning agent" | Python/CLI not found | Check Python PATH, verify `.env` |
| "LLM service unavailable" | Ollama not running | Run `ollama serve` |

---

## ✨ Success Indicators

Once working, you should see:

✅ Ctrl+Shift+K opens a chat panel on the right  
✅ Panel shows "Kiro Chat" title  
✅ Input box at bottom says "Type your message..."  
✅ Can type and send messages  

---

## 🎯 Next Steps

Once working:
1. Read [QUICK_START_EXTENSION.md](QUICK_START_EXTENSION.md)
2. Follow the 5-minute setup
3. Start chatting!

---

## 💬 Still Not Working?

1. **Verify prerequisites**:
   ```bash
   python --version  # Should be 3.8+
   node --version    # Should be 14+
   npm --version     # Should be 6+
   ollama --version  # If installed
   ```

2. **Check VS Code version**:
   - Help → About → Version should be 1.60+

3. **Try alternative keyboard shortcut**:
   - Ctrl+Shift+P → "Kiro: Start Chat"
   - If this works, keybinding might conflict

4. **Completely uninstall & reinstall**:
   ```bash
   # Uninstall
   code --uninstall-extension kiro-vscode-extension
   
   # Reinstall
   code --install-extension ./kiro-vscode-extension-0.1.0.vsix
   ```

---

**If still stuck:** Check [EXTENSION_USAGE_GUIDE.md](EXTENSION_USAGE_GUIDE.md) Troubleshooting section for more help!
