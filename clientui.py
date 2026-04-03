import socket
import threading
import curses

def receive_messages(sock, stdscr, chat_win, max_y, max_x):
    while True:
        try:
            message = sock.recv(1024).decode()
            chat_win.addstr(f"{message}\n")
            chat_win.refresh()
        except:
            break

def chat_client(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()

    chat_win = curses.newwin(max_y - 3, max_x, 0, 0)
    input_win = curses.newwin(3, max_x, max_y - 3, 0)
    input_win.addstr(1, 1, "You: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 12345))

    threading.Thread(target=receive_messages, args=(sock, stdscr, chat_win, max_y, max_x), daemon=True).start()

    while True:
        input_win.refresh()
        input_win.move(1, 6)
        input_win.clrtoeol()
        curses.echo()
        msg = input_win.getstr().decode()
        curses.noecho()
        if msg.lower() == "/quit":
            break
        sock.send(msg.encode())

    sock.close()

curses.wrapper(chat_client)
