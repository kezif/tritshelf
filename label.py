import cv2    
import math
import os
import numpy as np

def excract_frames(videoFilePath, savePath=None):
    savePath = savePath if savePath is not None else 'frames\\' + os.path.splitext(os.path.basename(videoFilePath))[0] # if save path is not specified then create it from video filename
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    count = 0
    videoFile = videoFilePath
    cap = cv2.VideoCapture(videoFile)  # capturing the video from the given path
    frameRate = cap.get(5)  # frame rate
    x=1
    total_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while(cap.isOpened()):
        frameId = cap.get(1)  # current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate)*2 == 0):
            filename = savePath + "\\frame{:04d}.jpg".format(count);count+=1  
            cv2.imwrite(filename, rescale_frame(frame))
            print(f'Current frame {frameId:.0f} of {total_len:.0f} total or {frameId/total_len:.2f}', end='\r')
    cap.release()
    print (f'\nDone! Created {count} frames')

def rescale_frame(frame):
    return cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)

def label_data(folderPath, start_from=0):
    files = os.listdir(folderPath)
    files_path = [os.path.join(folderPath, fi) for fi in files]

    labels = []
    for fi in files_path:
        code = get_code(fi)
        if code is not None:
            labels.append(code)
        else:
            break

    arr = np.column_stack((files[:len(labels)], labels))
    np.savetxt(os.path.join(folderPath,'mapping.csv'), arr, delimiter=',', fmt='%s', header="Image_ID, Class")
    


def get_code(path):
    img = cv2.imread(path)
    while(1):
        cv2.imshow('Labelling',img)
        k = cv2.waitKey(0)
        cv2.destroyAllWindows()
        if k==27:    # Esc key to stop and break while cycle
            return None
        elif k==ord('a'):  # if a key pressed - corelete with 1 class
            return 1
        else:
            return 0

excract_frames('video\\PokemonS17E35.mkv')
label_data('frames\\PokemonS17E35')
