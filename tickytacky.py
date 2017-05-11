import cv2
import numpy as np
import logging
# from os import listdir
# from os.path import isfile, join


def main():
    # onlyfiles = [f for f in listdir('images') if isfile(join('images', f))]
    # for f in onlyfiles:
    #    process(f)

    print(process('images/1.png'))
    print(process('images/2.jpg'))
    print(process('images/3.jpg'))
    print(process('images/4.jpg'))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def process(img_loc):
    img = cv2.imread(img_loc)
    height, width = img.shape[:2]
    scaled_width = 1000
    scaled_height = height/width * scaled_width
    res = cv2.resize(img, (1000, scaled_height), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('threshold', thresh)

    # Threshold: 250 to find vertical lines, higher (350) to find only horiz that matter.
    vlines = [l for l in cv2.HoughLines(thresh, 1, np.pi/2, 250)[0] if l[1] == 0]
    hlines = [l for l in cv2.HoughLines(thresh, 1, np.pi/2, 360)[0]
              if (np.pi/2+.3) > l[1] > np.pi/2-.3]
    logging.info("vertical lines: {0}\nhorizontal lines: {1}".format(len(vlines), len(hlines)))

    # Remove lines close to edge of image
    x_margin = thresh.shape[0] * .08
    y_margin = thresh.shape[1] * .08
    my_vlines = []
    my_hlines = []
    l_border = (0, 0)
    r_border = (thresh.shape[0], 0)
    t_border = (0, np.pi/2)
    b_border = (thresh.shape[1], np.pi/2)

    # Removing cluster of lines at left and right margins
    for rho, theta in vlines:
        if abs(rho) < x_margin:  # left margin
            if rho > l_border[0]:
                l_border = (rho, theta)
            continue
        if abs(rho) > (thresh.shape[0] - x_margin):  # right margin
            if rho < r_border[0]:
                r_border = (rho, theta)
            continue
        my_vlines.append((rho, theta))
    # my_vlines.append(l_border)
    # my_vlines.append(r_border)

    # Removing cluster of lines at top and bottom margins
    for rho, theta in hlines:
        if abs(rho) < y_margin:  # top margin
            if rho > t_border[0]:
                t_border = (rho, theta)
            continue
        if abs(rho) > (thresh.shape[1] - y_margin):  # bottom margin
            if rho < b_border[0]:
                b_border = (rho, theta)
            continue
        my_hlines.append((rho, theta))
    # my_hlines.append(t_border)
    # my_hlines.append(b_border)

    vertical_line_offsets = []
    for rho, theta in my_vlines:
        # make list of normalized line offsets from center
        vertical_line_offsets.append(rho)
        # drawline(rho, theta, res)

    horiz_line_offsets = []
    for rho, theta in my_hlines:
        # make list of normalized line offsets from center
        horiz_line_offsets.append(rho)
        # drawline(rho, theta, res)

    # cv2.imshow(img_loc, res)
    # cv2.imwrite('output/'+img_loc, res)
    # print(vertical_line_offsets)
    # print(horiz_line_offsets)

    # These steps for later clustering calculation
    # vertical_line_offsets = normalize_offset_from_mean(vertical_line_offsets)
    # horiz_line_offsets = normalize_offset_from_mean(horiz_line_offsets)
    return (horiz_line_offsets, vertical_line_offsets)


def normalize_offset_from_mean(numbers):
    mean = float(sum(numbers)) / max(len(numbers), 1)
    print('mean: ' + str(mean))
    result = [(mean-x)/mean for x in numbers]
    result.sort(key=lambda n: abs(n))
    return result


def drawline(rho, theta, img):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)


if __name__ == '__main__':
    main()
