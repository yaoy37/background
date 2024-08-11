from fastapi.responses import HTMLResponse


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <button onclick="sendMessage()">Send Message</button>
        <ul id='messages'>
        </ul>
        <script>
            let ws = new WebSocket("ws://127.0.0.1:7008/ws");
            ws.onmessage = function(event) {
                let messages = document.getElementById('messages')
                let message = document.createElement('li')
                let content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };

            function sendMessage() {
                ws.send("Hello from client!")
            }
        </script>
    </body>
</html>
"""


async def get_test_wb_html():
    return HTMLResponse(html)

