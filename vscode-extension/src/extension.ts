import * as vscode from 'vscode';
import axios from 'axios';

let chatPanel: ChatPanel | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('Kiro Agent extension activated');

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('kiro-agent.openChat', () => {
            if (!chatPanel) {
                chatPanel = new ChatPanel(context.extensionUri);
            }
            chatPanel.show();
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('kiro-agent.clearChat', () => {
            if (chatPanel) {
                chatPanel.clearChat();
            }
        })
    );

    // Create webview provider
    const provider = new ChatViewProvider(context.extensionUri);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('kiro-agent.chatView', provider)
    );
}

export function deactivate() {
    if (chatPanel) {
        chatPanel.dispose();
    }
}

class ChatViewProvider implements vscode.WebviewViewProvider {
    private _view?: vscode.WebviewView;
    private sessionId: string;

    constructor(private readonly _extensionUri: vscode.Uri) {
        this.sessionId = this.generateSessionId();
    }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);

        // Handle messages from webview
        webviewView.webview.onDidReceiveMessage(async (data) => {
            switch (data.type) {
                case 'sendMessage':
                    await this.sendMessage(data.message);
                    break;
                case 'approve':
                    await this.approveChange(data.changeId);
                    break;
                case 'reject':
                    await this.rejectChange(data.changeId);
                    break;
            }
        });
    }

    private async sendMessage(message: string) {
        const config = vscode.workspace.getConfiguration('kiroAgent');
        const serverUrl = config.get<string>('serverUrl', 'http://localhost:5000');
        const enableStreaming = config.get<boolean>('enableStreaming', true);

        try {
            if (enableStreaming) {
                // Streaming mode
                const response = await fetch(`${serverUrl}/api/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message,
                        session_id: this.sessionId,
                        stream: true
                    })
                });

                const reader = response.body?.getReader();
                const decoder = new TextDecoder();

                if (reader) {
                    while (true) {
                        const { done, value } = await reader.read();
                        if (done) break;

                        const chunk = decoder.decode(value);
                        const lines = chunk.split('\n');

                        for (const line of lines) {
                            if (line.startsWith('data: ')) {
                                const data = JSON.parse(line.slice(6));
                                this._view?.webview.postMessage(data);
                            }
                        }
                    }
                }
            } else {
                // Non-streaming mode
                const response = await axios.post(`${serverUrl}/api/chat`, {
                    message,
                    session_id: this.sessionId,
                    stream: false
                });

                this._view?.webview.postMessage({
                    type: 'response',
                    content: response.data.response,
                    approvals: response.data.pending_approvals
                });
            }
        } catch (error: any) {
            this._view?.webview.postMessage({
                type: 'error',
                content: error.message
            });
        }
    }

    private async approveChange(changeId: string) {
        const config = vscode.workspace.getConfiguration('kiroAgent');
        const serverUrl = config.get<string>('serverUrl', 'http://localhost:5000');

        try {
            const response = await axios.post(`${serverUrl}/api/approve`, {
                session_id: this.sessionId,
                change_id: changeId
            });

            this._view?.webview.postMessage({
                type: 'approval_result',
                success: true,
                message: response.data.message
            });
        } catch (error: any) {
            this._view?.webview.postMessage({
                type: 'error',
                content: error.message
            });
        }
    }

    private async rejectChange(changeId: string) {
        const config = vscode.workspace.getConfiguration('kiroAgent');
        const serverUrl = config.get<string>('serverUrl', 'http://localhost:5000');

        try {
            const response = await axios.post(`${serverUrl}/api/reject`, {
                session_id: this.sessionId,
                change_id: changeId
            });

            this._view?.webview.postMessage({
                type: 'approval_result',
                success: true,
                message: response.data.message
            });
        } catch (error: any) {
            this._view?.webview.postMessage({
                type: 'error',
                content: error.message
            });
        }
    }

    private generateSessionId(): string {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    private getHtmlForWebview(webview: vscode.Webview): string {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kiro Agent</title>
    <style>
        body {
            padding: 0;
            margin: 0;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
        }
        
        #chat-container {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        #messages {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 8px 12px;
            border-radius: 6px;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message {
            background-color: var(--vscode-input-background);
            border-left: 3px solid var(--vscode-focusBorder);
        }
        
        .agent-message {
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border-left: 3px solid var(--vscode-charts-green);
        }
        
        .error-message {
            background-color: var(--vscode-inputValidation-errorBackground);
            border-left: 3px solid var(--vscode-inputValidation-errorBorder);
        }
        
        .approval-card {
            margin: 10px 0;
            padding: 12px;
            background-color: var(--vscode-editor-background);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 6px;
        }
        
        .approval-header {
            font-weight: bold;
            margin-bottom: 8px;
            color: var(--vscode-charts-yellow);
        }
        
        .approval-content {
            font-family: var(--vscode-editor-font-family);
            font-size: 12px;
            background-color: var(--vscode-textCodeBlock-background);
            padding: 8px;
            border-radius: 4px;
            margin: 8px 0;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .approval-buttons {
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }
        
        button {
            padding: 6px 12px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            transition: opacity 0.2s;
        }
        
        button:hover {
            opacity: 0.8;
        }
        
        .approve-btn {
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
        }
        
        .reject-btn {
            background-color: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
        }
        
        #input-container {
            padding: 10px;
            border-top: 1px solid var(--vscode-panel-border);
            display: flex;
            gap: 8px;
        }
        
        #message-input {
            flex: 1;
            padding: 8px;
            background-color: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border: 1px solid var(--vscode-input-border);
            border-radius: 4px;
            font-family: var(--vscode-font-family);
        }
        
        #send-btn {
            padding: 8px 16px;
            background-color: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
        }
        
        .typing-indicator {
            display: inline-block;
            padding: 8px 12px;
            background-color: var(--vscode-editor-inactiveSelectionBackground);
            border-radius: 6px;
            margin-bottom: 10px;
        }
        
        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--vscode-foreground);
            margin: 0 2px;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        
        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="messages"></div>
        <div id="input-container">
            <input type="text" id="message-input" placeholder="Ask Kiro anything..." />
            <button id="send-btn">Send</button>
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');
        
        let currentMessage = null;
        let isTyping = false;

        // Send message
        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage('user', message);
            messageInput.value = '';
            
            showTypingIndicator();
            vscode.postMessage({ type: 'sendMessage', message });
        }

        sendBtn.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        // Add message to chat
        function addMessage(role, content) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + role + '-message';
            messageDiv.textContent = content;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        // Show typing indicator
        function showTypingIndicator() {
            if (isTyping) return;
            isTyping = true;
            
            const indicator = document.createElement('div');
            indicator.className = 'typing-indicator';
            indicator.id = 'typing-indicator';
            indicator.innerHTML = '<span></span><span></span><span></span>';
            messagesDiv.appendChild(indicator);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        // Hide typing indicator
        function hideTypingIndicator() {
            const indicator = document.getElementById('typing-indicator');
            if (indicator) indicator.remove();
            isTyping = false;
        }

        // Handle streaming tokens
        function handleToken(content) {
            hideTypingIndicator();
            
            if (!currentMessage) {
                currentMessage = document.createElement('div');
                currentMessage.className = 'message agent-message';
                messagesDiv.appendChild(currentMessage);
            }
            
            currentMessage.textContent += content;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        // Handle approvals
        function handleApprovals(approvals) {
            approvals.forEach(approval => {
                const card = document.createElement('div');
                card.className = 'approval-card';
                card.innerHTML = 
                    '<div class="approval-header">📋 Approval Required: ' + approval.change_id + '</div>' +
                    '<div><strong>Operation:</strong> ' + approval.operation + '</div>' +
                    '<div><strong>Path:</strong> ' + approval.path + '</div>' +
                    (approval.reason ? '<div><strong>Reason:</strong> ' + approval.reason + '</div>' : '') +
                    (approval.content ? '<div class="approval-content">' + approval.content.substring(0, 500) + '...</div>' : '') +
                    '<div class="approval-buttons">' +
                        '<button class="approve-btn" onclick="approve(\\'' + approval.change_id + '\\')">✓ Approve</button>' +
                        '<button class="reject-btn" onclick="reject(\\'' + approval.change_id + '\\')">✗ Reject</button>' +
                    '</div>';
                messagesDiv.appendChild(card);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            });
        }

        // Approve/Reject functions
        window.approve = (changeId) => {
            vscode.postMessage({ type: 'approve', changeId });
        };

        window.reject = (changeId) => {
            vscode.postMessage({ type: 'reject', changeId });
        };

        // Handle messages from extension
        window.addEventListener('message', event => {
            const message = event.data;

            switch (message.type) {
                case 'token':
                    handleToken(message.content);
                    break;
                
                case 'approvals':
                    handleApprovals(message.content);
                    break;
                
                case 'done':
                    hideTypingIndicator();
                    currentMessage = null;
                    break;
                
                case 'error':
                    hideTypingIndicator();
                    addMessage('error', 'Error: ' + message.content);
                    currentMessage = null;
                    break;
                
                case 'approval_result':
                    addMessage('agent', message.message);
                    break;
            }
        });
    </script>
</body>
</html>`;
    }
}

class ChatPanel {
    private panel: vscode.WebviewPanel | undefined;

    constructor(private extensionUri: vscode.Uri) {}

    public show() {
        if (this.panel) {
            this.panel.reveal();
        }
    }

    public clearChat() {
        // Implementation for clearing chat
    }

    public dispose() {
        this.panel?.dispose();
    }
}
