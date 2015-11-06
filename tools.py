from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average


def compare_images(img1, img2):
    diff = img1 - img2
    m_norm = sum(abs(diff))
    z_norm = norm(diff.ravel(), 0)
    return m_norm, z_norm


def to_grayscale(arr):
    if len(arr.shape) == 3:
        return average(arr, -1)
    else:
        return arr
