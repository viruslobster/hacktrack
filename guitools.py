import cv2
import cv2.cv as cv

class RectangleInfo:
    '''Stores the state of the rectangle selection tool'''
    def __init__(self):
        self.p1 = None # upper left corner of the selection
        self.p2 = None # lower right corner of the selection
        self.selection_started = False
        self.selection_finished = False

    def __str__(self):
        return "(%s, %s, %s, %s, %s)" % (self.x0, self.y0, self.x1, self.y1, self.selected)

def select_rectangle(cam):
    info = RectangleInfo()
    window_name = 'Select Rectangle'
    cv2.namedWindow(window_name)

    while not info.selection_finished:
        retval, img = cam.read()
        cv.SetMouseCallback(window_name, create_mouse_event_handler(img, info), 0)
        img_copy = img.copy()
        cv2.rectangle(img_copy, info.p1, info.p2, (0, 0, 255))
        cv2.imshow(window_name, img_copy)

        if cv2.waitKey(33) == 27:
            cv2.destroyAllWindows()
            break
    return ((info.p1, info.p2), img)

def create_mouse_event_handler(img, info):
    def on_mouse(event, x, y, flags, params):
        if info.selection_started:
            info.p2 = (x, y)

        if event == cv.CV_EVENT_LBUTTONDOWN:
            info.selection_started = True
            info.p1 = (x, y)
            info.p2 = (x, y)

        elif event == cv.CV_EVENT_LBUTTONUP:
            info.selection_finished = True
    return on_mouse
