import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([3, 5, 5, 3, 7, 6, 7, 7])
plt.plot(x, y, 'r')
plt.plot(x, y, 'g', lw=10)
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([13, 25, 17, 36, 21, 16, 10, 15])
plt.bar(x, y, 0.2, alpha=1, color='b')
plt.show()
