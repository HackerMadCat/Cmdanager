import time
from multiprocessing import Pool

from src.logger import logger
from src.tasks import CounterTask, MultiTask


def multiplier(datum1, datum2):
    result = datum1 * datum2
    time.sleep(0.01)
    task2.update()
    return result


@logger.trace
def multiplex(data, pool: Pool):
    logger.show(progress2)
    # return [multiplier(datum1, datum2) for datum1, datum2 in data]
    return pool.starmap(multiplier, data)


def summator(datum1, datum2):
    result = datum1 + datum2
    time.sleep(0.01)
    task3.update()
    return result


@logger.trace
def sum(data, pool: Pool):
    logger.show(progress3)
    # return [summator(datum1, datum2) for datum1, datum2 in data]
    return pool.starmap(summator, data)


data = range(2 ** 10)
task2 = CounterTask(len(data) / 2, "mul")
task3 = CounterTask(len(data) / 4, "sum")
task1 = MultiTask("tasks", task2, task3)
progress1 = logger.progress(task1, 50, "hui_0")
progress2 = logger.progress(task2, 40, "hui_1")
progress3 = logger.progress(task3, 30, "hui_2")
with Pool(2) as pool:
    logger.show(progress1)
    data = zip(data[0::2], data[1::2])
    data = multiplex(data, pool)
    data = zip(data[0::2], data[1::2])
    data = sum(data, pool)
# logger.print(data)

logger.print(task1.completeness())
logger.print(task2.completeness())
logger.print(task3.completeness())
