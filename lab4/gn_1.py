def sq_generator(N):
    for i in range(1, N + 1):
        yield i ** 2

gen = sq_generator(5)

for square in gen:
    print(square)
