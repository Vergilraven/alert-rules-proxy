import http.server
import json
import requests


class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # 检查 Authorization 头
        auth_header = self.headers.get('Authorization')
        if auth_header != 'Bearer 123456':
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data)
            # 根据webhook内容进行转发，这里假设转发到百度搜索
            query = data.get('query', '')  # 假设问题内容在 JSON 中的 'query' 字段
            forward_url = f"https://www.baidu.com/s?wd={query}"
            response = requests.post(forward_url, json=data)
            self.send_response(response.status_code)
            self.end_headers()
            self.wfile.write(response.content)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")

def run(server_class=http.server.HTTPServer, handler_class=WebhookHandler, port=4443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()