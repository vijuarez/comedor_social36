from tqdm import tqdm
import json

from solver import optimize

def deep_count(i):
    try:
        iterator = iter(i)
    except TypeError:
        return 1
    else:
        return sum(deep_count(j) for j in i)

def diff(original: dict, new: dict, threshold=0.05):
    return any(original.get(key, 0) * threshold < abs(original.get(key, 0) - new[key]) for key in new.keys())

def nudge_up(key: str, data: dict, solution: dict, delta_past=-1, limit=30):
    if not limit:
        return 'Inf'
    if delta_past == -1:
        delta_past = data[key]
    data = data.copy()
    delta = int(delta_past * 0.5)
    data[key] += delta
    new_solution = optimize(data)
    if diff(solution, new_solution):
        data[key] -= delta
        return nudge_up(key, data, solution, delta, limit - 1)
    else:
        if not delta:
            return data[key]
        else:
            return nudge_up(key, data, solution, delta * 2, limit - 1)

def nudge_down(key: str, data: dict, solution: dict, delta_past=-1, limit=30):
    if not limit:
        return data[key]
    if delta_past == -1:
        delta_past = data[key] * 0.5
    data = data.copy()
    delta = int(delta_past * 0.5)
    data[key] -= delta
    if data[key] < 1:
        return 0
    new_solution = optimize(data)
    if diff(solution, new_solution):
        data[key] += delta
        return nudge_down(key, data, solution, delta, limit - 1)
    else:
        if not delta:
            return data[key]
        else:
            return nudge_down(key, data, solution, delta * 2, limit - 1)


def nudge_up2(key: str, key2, data: dict, solution: dict, delta_past=-1, limit=30):
    if not limit:
        return 'Inf'
    if delta_past == -1:
        delta_past = data[key][key2]
    data = data.copy()
    delta = int(delta_past * 0.5)
    data[key][key2] += delta
    new_solution = optimize(data)
    if diff(solution, new_solution):
        data[key][key2] -= delta
        return nudge_up2(key, key2, data, solution, delta, limit - 1)
    else:
        if not delta:
            return data[key][key2]
        else:
            return nudge_up2(key, key2, data, solution, delta * 2, limit - 1)

def nudge_down2(key: str, key2, data: dict, solution: dict, delta_past=-1, limit=30):
    if not limit:
        return data[key][key2]
    if delta_past == -1:
        delta_past = data[key][key2] * 0.5
    data = data.copy()
    delta = int(delta_past * 0.5)
    data[key][key2] -= delta
    if data[key][key2] < 1:
        return 0
    new_solution = optimize(data)
    if diff(solution, new_solution):
        data[key][key2] += delta
        return nudge_down2(key, key2, data, solution, delta, limit - 1)
    else:
        if not delta:
            return data[key][key2]
        else:
            return nudge_down2(key, key2, data, solution, delta * 2, limit - 1)


def nudge_up3(key: str, key2, key3, data: dict, solution: dict, delta_past=-1, limit=30):
    if not limit:
        return 'Inf'
    if delta_past == -1:
        delta_past = data[key][key2][key3]
    data = data.copy()
    delta = int(delta_past * 0.5)
    data[key][key2][key3] += delta
    new_solution = optimize(data)
    if diff(solution, new_solution):
        data[key][key2][key3] -= delta
        return nudge_up3(key, key2, key3, data, solution, delta, limit - 1)
    else:
        if not delta:
            return data[key][key2][key3]
        else:
            return nudge_up3(key, key2, key3, data, solution, delta * 2, limit - 1)

def nudge_down3(key: str, key2, key3, data: dict, solution: dict, delta_past=-1, limit=30):
    if not limit:
        return data[key][key2][key3]
    if delta_past == -1:
        delta_past = data[key][key2][key3] * 0.5
    data = data.copy()
    delta = int(delta_past * 0.5)
    data[key][key2][key3] -= delta
    if data[key][key2][key3] < 1:
        return 0
    new_solution = optimize(data)
    if diff(solution, new_solution):
        data[key][key2][key3] += delta
        return nudge_down3(key, key2, key3, data, solution, delta, limit - 1)
    else:
        if not delta:
            return data[key][key2][key3]
        else:
            return nudge_down3(key, key2, key3, data, solution, delta * 2, limit - 1)


def main():
    with open('data.json') as f:
        data = json.loads(f.read())
    f = open('result.txt', 'w')

    print('Initial optimization')

    solution = optimize(data)

    print('Starting sensibility analysis')

    to_nudge = ["sueldo_fijo", "vol_max", "entrada"]
    to_nudge_once = ["donaciones_monetarias", "visitas", "volumen_alimentos", "duracion_alimentos", "costo_alimento"]
    to_nudge_twice = ["cantidad_alimento"]

    bar = tqdm(total=sum(len(data[x]) for x in to_nudge_once) + len(to_nudge) + sum(sum(len(y) for y in data[x]) for x in to_nudge_twice))

    for i in to_nudge:
        print(i, 'limit up', nudge_up(i, data, solution), file=f)
        print(i, 'limit down', nudge_down(i, data, solution), file=f)
        bar.update()

    for i in to_nudge_once:
        for j in range(len(data[i])):
            print(i, j, 'limit up', nudge_up2(i, j, data, solution), file=f)
            print(i, j, 'limit down', nudge_down2(i, j, data, solution), file=f)
            bar.update()

    for i in to_nudge_twice:
        for j in range(len(data[i])):
            for k in range(len(data[i][j])):
                print(i, j, k, 'limit up', nudge_up3(i, j, k, data, solution), file=f)
                print(i, j, k, 'limit down', nudge_down3(i, j, k, data, solution), file=f)
                bar.update()

    bar.close()



if __name__ == "__main__":
    main()