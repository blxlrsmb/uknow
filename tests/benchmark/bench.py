#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: bench.py
# $Date: Sat Dec 14 23:57:04 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import os
import time
import errno
import psutil
import resource
import subprocess


NR_REQUESTS = 10000
CONCURRENCY = 4
OUTPUT_DIR = 'output'

SERVER_PROC_NAME = 'standalone'
SERVER_PID = None

USER = {
    'username': 'test',
    'password': 'test'
}

HOST = 'localhost'
PORT = '5000'

FETCHER_ID = 'thu_learn'
TAB_NAME = 'tab'
TAG_NAME = 'Guokr'

TESTS = {
    '/login': {
        'param': USER
    },
    '/fetcher/list': {
        'login': True
    },
    '/fetcher/enable': {
        'login': True,
        'param': {
            'fetcher_id': FETCHER_ID,
            'username': USER['username'],
            'password': USER['password']
        }
    },
    '/fetcher/disable': {
        'login': True,
        'param': {
            'fetcher_id': FETCHER_ID
        }
    },
    '/add_tab': {
        'login': True,
        'param': {
            'name': TAB_NAME
        }
    },
    '/get_all_tabs': {
        'login': True,
    },
    '/del_lab': {
        'login': True,
        'param': {
            'name': TAB_NAME
        }
    },
    '/get_tab_article': {
        'login': True,
        'param': {
            'name': TAB_NAME
        }
    },
    '/logout': {
        'login': True
    },
    '/register': {
        'param': USER
    },
    '/add_tag': {
        'method': 'POST',
        'login': True,
        'param': {
            'name': TAG_NAME
        },
        'require': ['/add_tab']
    },
    '/set_tag': {
        'method': 'POST',
        'login': True,
        'param': {
            'name': TAG_NAME,
            'tab': TAB_NAME
        },
        'require': ['/add_tab']
    },
    '/get_all_tags': {
        'login': True,
    },
    '/del_tag': {
        'login': True,
        'param': {
            'name': TAG_NAME,
            'tab': TAG_NAME
        }
    },
    '/filter/list': {
        'login': True,
    },
    '/filter/enable': {
        'login': True,
    },
    '/filter/disable': {
        'login': True,
    },
    '/refresh': {
        'login': True,
    }
}


def get_login_cookie():
    from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
    import cookielib

    cj = cookielib.CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())

    req = Request(
        "http://localhost:5000/login?" +
        "username={username}&password={password}" . format(**USER))
    f = opener.open(req)

    html = f.read()
    return cj


def gen_ab_cookie_args(cookies):
    args = []
    for cookie in cookies:
        args.append('-C')
        args.append("{}={}" . format(cookie.name, cookie.value))
    return args


def get_url(page):
    return 'http://{}:{}{}' . format(HOST, PORT, page)


def get_output_path_by_page(page):
    assert page.startswith('/')
    return os.path.join(OUTPUT_DIR, page[1:].replace('/', '.'))


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def plot_single_line(x, y, xlabel='', ylabel='', title='',
                     output=''):
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()

    plt.title(title)

    plt.plot(x, y, lw=2, color='#9061C2')
    #plt.legend(loc = 3, fancybox = True, shadow = True)
    plt.grid(color='gray', linestyle='dashed')
    plt.ylim([0, max(max(y), 1.0) * 1.1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    plt.savefig(output)
    plt.close(fig)


def plot_multi_line(data, xlabel='', ylabel='', title='',
                    output=''):
    """:param data is a list of tuple (x, y, label) or (x, y)"""
    import matplotlib.pyplot as plt

    fig = plt.figure()

    plt.title(title)

    colors = ['#9061C2', '#BE80FF', '#02779E', '#4E9CB5',
              '#327CCB', '#14B694', '#EB540A', '#2DFF78',
              '#1A20BA', '#251137', '#4C6C0A', '#0B2DE5']

    for ind, (x, y, label) in enumerate(data):
        plt.plot(x, y, label=label, lw=2,
                 color=colors[ind % len(colors)])

    plt.legend(loc=4, fancybox=True, shadow=True)
    plt.grid(color='gray', linestyle='dashed')
    plt.ylim([0, max(max(y), 1.0) * 1.1])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    plt.savefig(output)

    plt.close(fig)


def plot_page_serv_time(page):
    import numpy as np

    fpath = get_output_path_by_page(page)
    with open(fpath) as f:
        data = [i.rstrip().split(',') for i in f]
    xlabel, ylabel = data[0]
    data = np.array(map(lambda x: map(float, x), data[1:]))
    x, y = data[:, 0], data[:, 1]
    title = 'benchmark of page {} with {} request at concurrency of {}' \
            . format(page, NR_REQUESTS, CONCURRENCY)

    plot_single_line(x, y, xlabel, ylabel, title, fpath + '.serv-time.png')


def start_bench_prog(page):
    """return Popen instance"""
    global login_cookie_args

    cookies = []
    option = TESTS[page]
    if 'login' in option and option['login'] is True:
        cookies = login_cookie_args
    output_path = get_output_path_by_page(page)
    mkdir_p(os.path.dirname(output_path))
    url = get_url(page)

    args = ['ab', '-k', '-n', str(NR_REQUESTS), '-e', output_path]
    args.extend(cookies)
    args.append(url)
    devnull = open('/dev/null', 'w')
    bench_prog = subprocess.Popen(args, stdout=devnull, stderr=devnull)
    return bench_prog


def plot_cpu_stats(page, time_checkpoint, cpu_times):
    assert len(time_checkpoint) == len(cpu_times)
    x = []
    for i in range(len(cpu_times)):
        x.append(time_checkpoint[i] - time_checkpoint[0])

    title = 'cpu benchmark of page {} with {} request at concurrency of {}' \
            . format(page, NR_REQUESTS, CONCURRENCY)
    output = get_output_path_by_page(page) + ".cpu.png"
    plot_single_line(
        x, cpu_times, xlabel='time in s', ylabel='cpu time percentage',
        title=title, output=output)


def plot_memory_stats(page, time_checkpoint, memory_info):
    import numpy as np
    memory_info = np.array(memory_info)
    title = 'cpu benchmark of page {} with {} request at concurrency of {}' \
            . format(page, NR_REQUESTS, CONCURRENCY)
    output = get_output_path_by_page(page) + ".mem.png"
    x = map(lambda x: x - time_checkpoint[0], time_checkpoint)
    y = memory_info[:, 1] / 2 ** 20
    plot_single_line(x, y, xlabel='time in s',
                     ylabel='Memory Usage in MB',
                     title=title, output=output)


def plot_io_stats(page, time_checkpoint, io_counters):
    assert(len(time_checkpoint) == len(io_counters))
    import numpy as np
    io_counters = np.array(io_counters)
    title = \
        'IO count benchmark of page {} with {} request at concurrency of {}' \
        .format(page, NR_REQUESTS, CONCURRENCY)
    output = get_output_path_by_page(page) + ".io-count.png"
    x = map(lambda x: x - time_checkpoint[0], time_checkpoint)
    print io_counters[:, 0]
    print io_counters[:, 0] - io_counters[0][0]
    plot_multi_line([
        (x, io_counters[:, 0] - io_counters[0][0], 'read count'),
        (x, io_counters[:, 1] - io_counters[0][1], 'write count')],
        xlabel='time in s', ylabel='IO count',
        title=title, output=output)


def get_cpu_time(pid):
    p = subprocess.Popen(['ps', '-u', '--pid', str(pid)],
                         stdout=subprocess.PIPE)
    p.wait()
    stdoutdata, stderrdata = p.communicate()
    stdoutdata.split('\n')
    return float(stdoutdata.split('\n')[1].split()[2])


def benchmark_page(page):
    global SERVER_PID

    bench_prog = start_bench_prog(page)
    p = psutil.Process(SERVER_PID)
    time_checkpoint = []
    cpu_times = []
    memory_info = []
    io_counters = []

    SLEEP_INTERVAL = 0.01
    try:
        while bench_prog.poll() is None:
            time_checkpoint.append(time.time())
            cpu_times.append(get_cpu_time(SERVER_PID))
            memory_info.append(p.get_memory_info())
            io_counters.append(p.get_io_counters())
            time.sleep(SLEEP_INTERVAL)
    except Exception as e:
        print e
        bench_prog.terminate()

    min_n = min(len(time_checkpoint), len(cpu_times),
                len(memory_info), len(io_counters))
    time_checkpoint = time_checkpoint[:min_n]
    cpu_times = cpu_times[:min_n]
    memory_info = memory_info[:min_n]
    io_counters = io_counters[:min_n]

    plot_cpu_stats(page, time_checkpoint, cpu_times)
    plot_memory_stats(page, time_checkpoint, memory_info)
    plot_io_stats(page, time_checkpoint, io_counters)


def get_server_pid():
    global SERVER_PROC_NAME
    procs = []
    for i in psutil.process_iter():
        for cmd in i.cmdline:
            if cmd.find(SERVER_PROC_NAME) != -1:
                procs.append(i)
                break
    return sorted(procs, key=lambda x: x.pid)[-1].pid


def main():
    global login_cookie_args, SERVER_PID
    login_cookie_args = gen_ab_cookie_args(get_login_cookie())

    SERVER_PID = get_server_pid()
    for page in TESTS:
        print '## testing {} ...' . format(page)
        benchmark_page(page)
        plot_page_serv_time(page)

if __name__ == '__main__':
    main()

# vim: foldmethod=marker
