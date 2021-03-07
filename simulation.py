import argparse
import csv


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Request:
    def __init__(self, request_seconds, process_time):
        self.timestamp = request_seconds
        self.process_time = process_time

    def get_stamp(self):
        return self.timestamp

    def get_time(self):
        return self.process_time

    def wait_time(self, current_time):
        return current_time - self.timestamp


class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task is not None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task is not None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_time()


def simulateOneServer(filename):
    req_queue = Queue()
    one_server = Server()
    waiting_times = []

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        requests = list(csv_reader)

    for request_seconds, _, process_time in requests:
        request_seconds, process_time = \
            int(request_seconds), int(process_time)
        request = Request(request_seconds, process_time)
        req_queue.enqueue(request)

        if not one_server.busy() and not req_queue.is_empty():
            next_req = req_queue.dequeue()
            waiting_times.append(next_req.wait_time(request_seconds))
            one_server.start_next(next_req)

        one_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs" % average_wait)


def simulateManyServers(filename, n_servers):
    req_queue = Queue()
    many_servers = [Server() for _ in range(n_servers)]
    waiting_times = []

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        requests = list(csv_reader)

    for request_seconds, _, process_time in requests:
        request_seconds, process_time = \
            int(request_seconds), int(process_time)
        request = Request(request_seconds, process_time)
        req_queue.enqueue(request)

        for one_server in many_servers:
            if not one_server.busy() and not req_queue.is_empty():
                next_req = req_queue.dequeue()
                waiting_times.append(next_req.wait_time(request_seconds))
                one_server.start_next(next_req)

            one_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs" % average_wait)


def main(file_name, n_servers):
    if n_servers:
        simulateManyServers(file_name, n_servers)
    else:
        simulateOneServer(file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='csv to read for request inputs',
                        type=str, required=True)
    parser.add_argument("--servers", help="number of servers to simulate",
                        type=int)
    args = parser.parse_args()
    main(args.file, args.servers)
