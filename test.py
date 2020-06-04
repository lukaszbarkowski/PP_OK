import multiprocessing as mp
counter = 5

def increment():
    global counter
    print(counter)


processes = []


def main():

    for i in range(16):
        p = mp.Process(target=increment)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    main()
