const vscode = require('vscode');
const cp = require('child_process');
const path = require('path');
const fs = require('fs');

let agentProc = null;

function activate(context) {
  console.log('Kiro extension activating...');
  
  const disposable = vscode.commands.registerCommand('kiro.startChat', async () => {
    console.log('kiro.startChat command triggered');
    
    const panel = vscode.window.createWebviewPanel(
      'kiroChat',
      'Kiro Chat',
      vscode.ViewColumn.One,
      { enableScripts: true }
    );

    console.log('Webview panel created');
    panel.webview.html = getWebviewContent();

    const workspaceRoot = (vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0].uri.fsPath) || null;
    console.log('Workspace root:', workspaceRoot);
    
    if (!workspaceRoot) {
      vscode.window.showErrorMessage('No workspace folder open. Please open a folder first.');
      panel.webview.postMessage({ type: 'output', text: 'Error: No workspace folder open', timestamp: new Date().toLocaleTimeString(), isError: true });
      return;
    }

    const agentDir = path.join(workspaceRoot, 'Chaitanya_coding_Agent');
    const pythonExe = path.join(workspaceRoot, '.venv', 'Scripts', 'python.exe');
    const cliPath = path.join(agentDir, 'cli.py');
    
    console.log('Agent dir:', agentDir);
    console.log('Python exe:', pythonExe);
    console.log('CLI path:', cliPath);
    
    // Check if paths exist
    if (!fs.existsSync(pythonExe)) {
      const msg = `Python not found at: ${pythonExe}`;
      vscode.window.showErrorMessage(msg);
      panel.webview.postMessage({ type: 'output', text: `Error: ${msg}`, timestamp: new Date().toLocaleTimeString(), isError: true });
      return;
    }
    
    if (!fs.existsSync(cliPath)) {
      const msg = `CLI not found at: ${cliPath}`;
      vscode.window.showErrorMessage(msg);
      panel.webview.postMessage({ type: 'output', text: `Error: ${msg}`, timestamp: new Date().toLocaleTimeString(), isError: true });
      return;
    }

    let messages = [];
    let pendingApprovals = new Map(); // Store pending file changes

    console.log('Spawning agent process...');
    
    try {
      agentProc = cp.spawn(pythonExe, ['cli.py', 'chat'], { 
        cwd: agentDir,
        stdio: ['pipe', 'pipe', 'pipe']
      });
      
      console.log('Agent spawned with PID:', agentProc.pid);
      panel.webview.postMessage({ type: 'output', text: '[Connected to Kiro Agent]', timestamp: new Date().toLocaleTimeString() });

      let outputBuffer = '';
      
      agentProc.stdout.on('data', (data) => {
        const text = data.toString();
        console.log('=== STDOUT ===', text.substring(0, 200));
        
        // Hide thinking indicator when we get output
        panel.webview.postMessage({ type: 'thinking', value: false });
        
        outputBuffer += text;
        
        // Split by newlines and process complete lines
        const lines = outputBuffer.split('\n');
        outputBuffer = lines[lines.length - 1]; // Keep incomplete line in buffer
        
        for (let i = 0; i < lines.length - 1; i++) {
          const line = lines[i].trim();
          if (!line || line === 'ready') continue;
          
          // Check if this is an approval request
          if (line.startsWith('APPROVAL_REQUEST:')) {
            try {
              const approvalData = JSON.parse(line.substring('APPROVAL_REQUEST:'.length));
              handleApprovalRequest(approvalData);
              continue;
            } catch (e) {
              console.error('Failed to parse approval request:', e);
            }
          }
          
          const timestamp = new Date().toLocaleTimeString();
          messages.push({ role: 'agent', text: line, timestamp });
          console.log('Posting message to webview:', line.substring(0, 100));
          panel.webview.postMessage({ type: 'output', text: line, timestamp });
        }
      });

      agentProc.stderr.on('data', (data) => {
        const text = data.toString();
        console.log('=== STDERR ===', text.substring(0, 200));
        if (text.trim()) {
          const timestamp = new Date().toLocaleTimeString();
          messages.push({ role: 'error', text, timestamp });
          console.log('Posting error to webview');
          panel.webview.postMessage({ type: 'output', text, timestamp, isError: true });
        }
      });

      agentProc.on('error', (err) => {
        console.error('Agent error:', err);
        const timestamp = new Date().toLocaleTimeString();
        panel.webview.postMessage({ type: 'output', text: `Error: ${err.message}`, timestamp, isError: true });
      });

      agentProc.on('exit', (code) => {
        console.log('Agent exited with code:', code);
        const timestamp = new Date().toLocaleTimeString();
        messages.push({ role: 'system', text: `Agent disconnected (exit code: ${code})`, timestamp });
        panel.webview.postMessage({ type: 'exit', code, timestamp });
      });

      agentProc.on('close', (code, signal) => {
        console.log('=== AGENT CLOSED ===', 'code:', code, 'signal:', signal);
      });

    } catch (err) {
      console.error('Failed to spawn agent:', err);
      vscode.window.showErrorMessage('Failed to start Kiro agent: ' + err.message);
      panel.webview.postMessage({ type: 'output', text: `Error: ${err.message}`, timestamp: new Date().toLocaleTimeString(), isError: true });
      return;
    }

    panel.webview.onDidReceiveMessage((message) => {
      if (message.type === 'input') {
        console.log('User input:', message.text);
        const timestamp = new Date().toLocaleTimeString();
        messages.push({ role: 'user', text: message.text, timestamp });
        if (agentProc && !agentProc.killed) {
          // Show thinking indicator
          panel.webview.postMessage({ type: 'thinking', value: true });
          agentProc.stdin.write(message.text + '\n');
        }
      } else if (message.type === 'stop') {
        console.log('Stop requested');
        if (agentProc) {
          agentProc.kill();
        }
      } else if (message.type === 'approve') {
        console.log('Approval:', message.changeId);
        handleApproval(message.changeId, true);
      } else if (message.type === 'reject') {
        console.log('Rejection:', message.changeId);
        handleApproval(message.changeId, false);
      }
    }, undefined, context.subscriptions);

    function handleApprovalRequest(approvalData) {
      const { change_id, change } = approvalData;
      pendingApprovals.set(change_id, change);
      
      // Send approval request to webview
      panel.webview.postMessage({
        type: 'approval_request',
        changeId: change_id,
        change: change,
        timestamp: new Date().toLocaleTimeString()
      });
    }

    function handleApproval(changeId, approved) {
      if (!pendingApprovals.has(changeId)) {
        console.error('Unknown change ID:', changeId);
        return;
      }

      const change = pendingApprovals.get(changeId);
      pendingApprovals.delete(changeId);

      // Send approval response to agent
      const response = {
        type: 'approval_response',
        change_id: changeId,
        approved: approved
      };

      if (agentProc && !agentProc.killed) {
        agentProc.stdin.write('APPROVAL_RESPONSE:' + JSON.stringify(response) + '\n');
      }

      // Notify webview
      const timestamp = new Date().toLocaleTimeString();
      const action = approved ? 'approved' : 'rejected';
      panel.webview.postMessage({
        type: 'output',
        text: `File change ${action}: ${change.path}`,
        timestamp,
        isSystem: true
      });
    }

    panel.onDidDispose(() => {
      console.log('Panel disposed');
      if (agentProc) {
        agentProc.kill();
        agentProc = null;
      }
    }, null, context.subscriptions);
  });

  context.subscriptions.push(disposable);
  console.log('Kiro extension activated successfully');
}

function deactivate() {
  if (agentProc) {
    try { agentProc.kill(); } catch (e) {}
    agentProc = null;
  }
}

function getWebviewContent() {
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kiro Chat</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', -apple-system, sans-serif;
      background: #1e1e1e;
      color: #d4d4d4;
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }
    #output {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      background: #1e1e1e;
    }
    .message {
      display: flex;
      margin-bottom: 12px;
      animation: fadeIn 0.3s;
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    .message-content {
      background: #252526;
      border-radius: 6px;
      padding: 10px 12px;
      max-width: 85%;
      border-left: 3px solid #0e639c;
    }
    .message.user .message-content {
      background: #1e4d2b;
      border-left-color: #4ec9b0;
      margin-left: auto;
    }
    .message.agent .message-content {
      background: #252526;
    }
    .message.error .message-content {
      background: #3d2626;
      border-left-color: #f48771;
    }
    .message.system .message-content {
      background: #2d2d30;
      border-left-color: #9cdcfe;
    }
    .approval-request {
      background: #3d3d30;
      border: 2px solid #d7ba7d;
      border-radius: 6px;
      padding: 12px;
      margin: 12px 0;
      animation: fadeIn 0.3s;
    }
    .approval-header {
      font-weight: bold;
      color: #d7ba7d;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .approval-icon {
      font-size: 18px;
    }
    .approval-details {
      background: #252526;
      padding: 8px;
      border-radius: 4px;
      margin: 8px 0;
      font-family: monospace;
      font-size: 12px;
    }
    .approval-path {
      color: #4ec9b0;
      font-weight: bold;
    }
    .approval-operation {
      color: #d7ba7d;
      text-transform: uppercase;
      font-size: 11px;
    }
    .approval-diff {
      background: #1e1e1e;
      padding: 8px;
      border-radius: 4px;
      margin: 8px 0;
      font-family: 'Courier New', monospace;
      font-size: 11px;
      max-height: 200px;
      overflow-y: auto;
      white-space: pre;
    }
    .approval-buttons {
      display: flex;
      gap: 8px;
      margin-top: 8px;
    }
    .approval-buttons button {
      flex: 1;
      padding: 8px 16px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-weight: bold;
    }
    .approve-btn {
      background: #4ec9b0;
      color: #1e1e1e;
    }
    .approve-btn:hover {
      background: #5fd9c0;
    }
    .reject-btn {
      background: #be3f1d;
      color: #fff;
    }
    .reject-btn:hover {
      background: #d93e23;
    }
    .message-text {
      white-space: pre-wrap;
      word-wrap: break-word;
      font-family: monospace;
      font-size: 13px;
      line-height: 1.5;
    }
    .message-meta {
      font-size: 11px;
      color: #858585;
      margin-top: 4px;
    }
    #thinking {
      padding: 8px 16px;
      background: #2d2d30;
      border-top: 1px solid #3e3e42;
      color: #9cdcfe;
      font-size: 12px;
      display: none;
      align-items: center;
      gap: 8px;
    }
    #thinking.active {
      display: flex;
    }
    .spinner {
      width: 12px;
      height: 12px;
      border: 2px solid #3e3e42;
      border-top-color: #9cdcfe;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    #controls {
      display: flex;
      padding: 8px;
      border-top: 1px solid #3e3e42;
      gap: 8px;
      background: #252526;
    }
    #input {
      flex: 1;
      padding: 10px;
      background: #3c3c3c;
      color: #d4d4d4;
      border: 1px solid #3e3e42;
      border-radius: 4px;
    }
    #input:focus {
      outline: none;
      border-color: #0e639c;
    }
    button {
      padding: 8px 16px;
      background: #0e639c;
      color: #fff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    button:hover {
      background: #1177bb;
    }
    button#stop {
      background: #be3f1d;
    }
    button#stop:hover {
      background: #d93e23;
    }
  </style>
</head>
<body>
  <div id="output"></div>
  <div id="thinking">
    <div class="spinner"></div>
    <span>Agent is thinking...</span>
  </div>
  <div id="controls">
    <input id="input" type="text" placeholder="Type message and press Enter..." />
    <button id="send">Send</button>
    <button id="stop">Stop</button>
  </div>

  <script>
    const vscode = acquireVsCodeApi();
    const output = document.getElementById('output');
    const input = document.getElementById('input');
    const send = document.getElementById('send');
    const stop = document.getElementById('stop');
    const thinking = document.getElementById('thinking');

    function addMessage(text, role, time) {
      const div = document.createElement('div');
      div.className = 'message ' + role;
      
      const content = document.createElement('div');
      content.className = 'message-content';
      
      const msg = document.createElement('div');
      msg.className = 'message-text';
      msg.textContent = text.trim();
      
      const meta = document.createElement('div');
      meta.className = 'message-meta';
      meta.textContent = role + ' @ ' + time;
      
      content.appendChild(msg);
      content.appendChild(meta);
      div.appendChild(content);
      output.appendChild(div);
      output.scrollTop = output.scrollHeight;
    }

    send.onclick = () => {
      const text = input.value.trim();
      if (!text) return;
      const time = new Date().toLocaleTimeString();
      addMessage(text, 'user', time);
      vscode.postMessage({ type: 'input', text });
      input.value = '';
      input.focus();
    };

    input.onkeydown = (e) => {
      if (e.key === 'Enter') {
        send.click();
        e.preventDefault();
      }
    };

    stop.onclick = () => {
      vscode.postMessage({ type: 'stop' });
      addMessage('Stop requested', 'system', new Date().toLocaleTimeString());
    };

    window.addEventListener('message', event => {
      const msg = event.data;
      const time = msg.timestamp || new Date().toLocaleTimeString();
      if (msg.type === 'output') {
        const role = msg.isError ? 'error' : msg.isSystem ? 'system' : 'agent';
        addMessage(msg.text, role, time);
      } else if (msg.type === 'exit') {
        addMessage('Agent disconnected', 'system', time);
        thinking.classList.remove('active');
      } else if (msg.type === 'thinking') {
        if (msg.value) {
          thinking.classList.add('active');
        } else {
          thinking.classList.remove('active');
        }
      } else if (msg.type === 'approval_request') {
        showApprovalRequest(msg.changeId, msg.change, time);
      }
    });

    function showApprovalRequest(changeId, change, time) {
      const div = document.createElement('div');
      div.className = 'approval-request';
      div.id = 'approval-' + changeId;
      
      const header = document.createElement('div');
      header.className = 'approval-header';
      header.innerHTML = '<span class="approval-icon">⚠️</span><span>File Change Approval Required</span>';
      
      const details = document.createElement('div');
      details.className = 'approval-details';
      
      const operation = document.createElement('div');
      operation.innerHTML = '<span class="approval-operation">' + change.operation + '</span> <span class="approval-path">' + change.path + '</span>';
      details.appendChild(operation);
      
      if (change.reason) {
        const reason = document.createElement('div');
        reason.textContent = 'Reason: ' + change.reason;
        reason.style.marginTop = '4px';
        reason.style.color = '#d4d4d4';
        details.appendChild(reason);
      }
      
      // Show diff for modifications
      if (change.operation === 'modify' && change.old_content && change.content) {
        const diffDiv = document.createElement('div');
        diffDiv.className = 'approval-diff';
        diffDiv.textContent = generateDiff(change.old_content, change.content);
        details.appendChild(diffDiv);
      }
      
      // Show content preview for create
      if (change.operation === 'create' && change.content) {
        const preview = document.createElement('div');
        preview.className = 'approval-diff';
        preview.textContent = change.content.substring(0, 500) + (change.content.length > 500 ? '...' : '');
        details.appendChild(preview);
      }
      
      const buttons = document.createElement('div');
      buttons.className = 'approval-buttons';
      
      const approveBtn = document.createElement('button');
      approveBtn.className = 'approve-btn';
      approveBtn.textContent = '✓ Approve';
      approveBtn.onclick = () => {
        vscode.postMessage({ type: 'approve', changeId: changeId });
        div.remove();
      };
      
      const rejectBtn = document.createElement('button');
      rejectBtn.className = 'reject-btn';
      rejectBtn.textContent = '✗ Reject';
      rejectBtn.onclick = () => {
        vscode.postMessage({ type: 'reject', changeId: changeId });
        div.remove();
      };
      
      buttons.appendChild(approveBtn);
      buttons.appendChild(rejectBtn);
      
      div.appendChild(header);
      div.appendChild(details);
      div.appendChild(buttons);
      
      output.appendChild(div);
      output.scrollTop = output.scrollHeight;
    }

    function generateDiff(oldText, newText) {
      const oldLines = oldText.split('\\n');
      const newLines = newText.split('\\n');
      let diff = '';
      const maxLines = Math.max(oldLines.length, newLines.length);
      
      for (let i = 0; i < Math.min(maxLines, 20); i++) {
        const oldLine = oldLines[i] || '';
        const newLine = newLines[i] || '';
        
        if (oldLine !== newLine) {
          if (oldLine) diff += '- ' + oldLine + '\\n';
          if (newLine) diff += '+ ' + newLine + '\\n';
        } else {
          diff += '  ' + oldLine + '\\n';
        }
      }
      
      if (maxLines > 20) {
        diff += '\\n... (' + (maxLines - 20) + ' more lines)';
      }
      
      return diff;
    }

    input.focus();
  </script>
</body>
</html>`;
}

module.exports = { activate, deactivate };
