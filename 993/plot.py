import matplotlib.pyplot as plt

lines = open('bb_values.txt').read().splitlines()
N = []
Y = []
for line in lines:
    if line.strip():
        try:
            n, v = map(int, line.split())
            N.append(n)
            Y.append(v)
        except:
            pass

plt.plot(N[:20000], Y[:20000], label="BB(N)")
plt.plot(N[:20000], [1.6666 * n for n in N[:20000]], label="5/3 N")
plt.legend()
plt.savefig("bb_plot.png")
