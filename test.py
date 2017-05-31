import np
from tickytacky import process
from os import listdir
from os.path import isfile, join
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


marker = float(2000)


def mydistance(a, b):
    dist = float(0)
    for idx, x in enumerate(a):
        dist = dist + abs(a[idx] - b[idx])
    # for n in range(0, a[1]):
    #    if b[1][n] is not None:
    #        dist = dist + a[1][n] - b[1][n]
    return dist

index = {}
onlyfiles = [f for f in sorted(listdir('images')) if isfile(join('images', f))]
samples = np.zeros((len(onlyfiles), 16))
for idx, f in enumerate(onlyfiles):
    index[idx] = f
    (hlines, vlines) = process('images/{0}'.format(f))
    # lines = hlines + vlines
    for i, l in enumerate(hlines):
        if i < 8:
            samples[idx][i] = float(l)
    for i, l in enumerate(vlines):
        if i < 8:
            samples[idx][8+i] = float(l)
    # scaled = StandardScaler().fit_transform(samples[idx].reshape(-1, 1))
    # samples[idx] = scaled

scaled = samples/float(1000)
for x in samples:
    print('{0}'.format(x))
for x in scaled:
    print('{0}'.format(x))

labels = DBSCAN(eps=.8, min_samples=2, metric=mydistance).fit_predict(scaled)

for idx, label in enumerate(labels):
    f = index[idx]
    print("{0} is a {1}".format(f, label))
