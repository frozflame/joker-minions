#!/usr/bin/env python3
# coding: utf-8

import sys


def _receive_lines(sock):
    while True:
        lines = sock.recv(2 ** 24).splitlines(keepends=True)
        if not lines:
            break
        for line in lines:
            yield line


def receive_lines(sock):
    partial_line = b''
    for line in _receive_lines(sock):
        if line.endswith(b'\n'):
            yield partial_line + line
            partial_line = b''
        else:
            partial_line = line
    if partial_line:
        yield partial_line + b'\n'


def split(binstr):
    parts = binstr.strip().split(maxsplit=1)
    if len(parts) == 2:
        return parts
    return b''.join(parts), None


def printerr(e):
    print(e.__class__.__name__, e, file=sys.stderr)


def runserver(func, host, port):
    import gevent
    from gevent import socket
    server_sock = socket.socket()
    server_sock.bind((host, port))
    server_sock.listen(500)
    while True:
        sock, _ = server_sock.accept()
        gevent.spawn(func, sock)


class ServerBase(object):
    def query(self, line):
        raise NotImplementedError

    def runserver(self, host='0.0.0.0', port=8333):
        return runserver(self.serve_client, host, port)

    def serve_client(self, sock):
        import socket
        try:
            req = sock.recv(2 ** 24)
            resp = self.query(req)
            sock.send(resp)
            sock.shutdown(socket.SHUT_WR)
        except Exception as e:
            printerr(e)
        finally:
            sock.close()


class PipedServerBase(object):
    def query(self, line):
        raise NotImplementedError

    def runserver(self, host='0.0.0.0', port=8333):
        return runserver(self.serve_client, host, port)

    def respond(self, sock, ql):
        try:
            resp = self.query(ql) + b'\n'
            sock.send(resp)
        except Exception as e:
            printerr(e)

    def serve_client(self, sock):
        with sock:
            print('sock', sock)
            for ql in receive_lines(sock):
                print('ql', ql)
                self.respond(sock, ql)
