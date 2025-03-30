import random

def Constrain(value:int, span:list):
    if value > span[1]:
        return span[1]
    elif value < span[0]:
        return span[0]
    else:
        return value
    
def RandFloat(start, end):
    return random.random() * (end-start) + start

def generate_random_sequence(n, a, b, target_avg):
    assert a <= target_avg <= b, "Target average must be within the range [a, b]"

    # Start with random values in [a, b]
    seq = [random.randint(a, b) for _ in range(n)]

    current_sum = sum(seq)
    target_sum = round(target_avg * n)
    diff = target_sum - current_sum

    # Adjust the sequence to bring average closer to target
    while diff != 0:
        i = random.randint(0, n - 1)
        if diff > 0 and seq[i] < b:
            seq[i] += 1
            diff -= 1
        elif diff < 0 and seq[i] > a:
            seq[i] -= 1
            diff += 1

    return seq

