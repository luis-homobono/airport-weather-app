from typing import List
from multiprocessing import Pool, cpu_count


def apply_parallel(func, payloads: List) -> List:
    saved = []
    with Pool(cpu_count()) as p:
        ret_list = p.map(func, payloads)
        saved.append(ret_list)
    return saved
