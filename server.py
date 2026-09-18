#!/usr/bin/env python3
"""
Local dev server for Green Powers site.
Serves .html files for extensionless URLs (e.g. /about-us -> about-us.html).
Uses threading so the browser can make concurrent requests.
"""
import http.server
import socketserver
import os

PORT = 8081
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0].split('#')[0]
        bare = path.lstrip('/')

        candidates = [
            bare or 'index.html',
            bare + '.html' if bare and not bare.endswith('.html') else None,
            os.path.join(bare, 'index.html') if bare else None,
        ]

        for candidate in candidates:
            if candidate and os.path.isfile(os.path.join(ROOT, candidate)):
                self.path = '/' + candidate
                break

        return super().do_GET()

    def log_message(self, fmt, *args):
        print("  %s %s" % (args[0], args[1]))


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == '__main__':
    os.chdir(ROOT)
    with ThreadedServer(('0.0.0.0', PORT), Handler) as httpd:
        print("Green Powers dev server: http://localhost:%d" % PORT)
        httpd.serve_forever()
