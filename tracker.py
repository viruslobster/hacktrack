#! /usr/bin/python

import cv2
import cv2.cv as cv
import numpy as np
from itertools import *
from guitools import select_rectangle

def mad(template, candidate):
    '''Mean Absolute Difference'''
    return np.mean(cv2.absdiff(template, candidate))

def crop(img, rect):
    ((x1, y1), (x2, y2)) = rect
    final_crop = np.zeros((y2 - y1, x2 - x1, 3), dtype=np.uint8)
    raw_crop = img[y1:y2, x1:x2]
    (height, width, _) = raw_crop.shape
    # np.copyto(cropped_img, img[y1:y2, x1:x2])
    x = max(-x1, 0)
    y = max(-y1, 0)
    final_crop[y:y+height, x:x+width] = raw_crop
    return final_crop

def candidate_regions(img, rect, step_size):
    ((x0, y0), (x1, y1)) = rect
    yield rect
    yield ((x0 + step_size, y0), (x1 + step_size, y1))
    yield ((x0 - step_size, y0), (x1 - step_size, y1))
    yield ((x0, y0 + step_size), (x1, y1 + step_size))
    yield ((x0, y0 - step_size), (x1, y1 - step_size))

# def scale_rect(rect, scale):
#     ((x0, y0), (x1, y1)) = rect
#     v = np.array([x0-x1, y0-y1])
#     v = v
#     x0_new =

def track(cam, template, template_rect, alpha):
    while True:
        retval, img = cam.read()
        if img == None:
            print 'no image!'
            exit()

        # MAD minimization
        step_size = 3
        while step_size > 0:
            rects_and_crops = ((rect, crop(img, rect)) for rect in candidate_regions(img, template_rect, step_size))
            (rect, candidate, _) = min(((rect, candidate, mad(template, candidate)) for (rect, candidate) in rects_and_crops), key=lambda x: x[2])
            if rect == template_rect:
                if step_size > 0:
                    step_size -= 1
                else:
                    break
            else:
                template_rect = rect

        # Scaling


        # Template Adaption
        # candidate = crop(img, template_rect)
        template = (alpha * template + (1-alpha) * candidate).astype('uint8')

        (p1, p2) = template_rect
        cv2.rectangle(img, p1, p2, (255, 0, 0))
        img = cv2.flip(img, 1)
        cv2.imshow('tracker', img)
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    (rect, img) = select_rectangle(cam)
    ((x1, y1), (x2, y2)) = rect
    template = img[y1:y2, x1:x2].copy()
    print 'Tracking started'
    track(cam, template, rect, 0.95)
    print 'Tracking stopped'

    # cv2.rectangle(img, p1, p2, (255, 0, 0))
    # cv2.imshow('real image', template)
    # cv2.waitKey(0)
cv2.destroyAllWindows()
