import sys
import cv2 as cv
import pathlib
import os

# -i for specifying input directory (will recursively go through it)
# -o specify the output direcory

def get__args__():
    lookup = [
        ["i","o"],  
    ]

    #get all __args__
    __args__ = sys.argv
    flags = {}
    
    for flag in lookup[0]:
        try:
            index = __args__.index(f"-{flag}")
            if index < (__args__.__len__() - 1):
                flags[flag] = __args__[index + 1]
            else:
                flags[flag] = None
        except ValueError:
            flags[flag] = None
    
    return flags
    
def error(message):
    print(message)
    sys.exit()

def getboundingbox(img):
    shape = img.shape
    bound = [shape[1],shape[0],0,0]

    for y in range(shape[0]): 
        for x in range(shape[1]):
            if not isemptypixel(img[y][x]):
                bound[0] = x if bound[0] > x else bound[0]
                bound[1] = y if bound[1] > y else bound[1]
                bound[2] = x if bound[2] < x else bound[2]
                bound[3] = y if bound[3] < y else bound[3]
                
    return bound

def getbiggestboundingbox(boundingboxes):
    t = boundingboxes[0]
    for b in boundingboxes:
        if t[0] > b[0]:
            t[0] = b[0]
        if t[1] > b[1]:
            t[1] = b[1]
        if t[2] < b[2]:
            t[2] = b[2]
        if t[3] < b[3]:
            t[3] = b[3]
    
    return t

def isemptypixel(p):
    return (p==0).all()

def main():
    
    __args__ = get__args__()    
    __dirpath__ = os.path.dirname(os.path.realpath(__file__))
    
    if __args__["i"] == None:
        __args__["i"] = os.path.join(__dirpath__,"input")
        if not os.path.exists(__args__["i"]):
            error("the input directory does not exist")
    if __args__["o"] == None:
        __args__["o"] = os.path.join(__dirpath__,"output")
        if not os.path.exists(__args__["o"]):
            os.makedirs(__args__["o"])
            
    print(f"starting sprite_optimizer.py on the directories :\ninput :  \"{__args__['i']}\"\noutput :  \"{__args__['o']}\"")

    input_image_path = []
    input_path = pathlib.Path(__args__["i"])
    
    if input_path.is_file():
        input_image_path.append(input_path)
    else:
        input_image_path = list(filter(lambda item: item.is_file(), input_path.rglob("*")))
    
    if input_image_path.__len__() == 0:
        error("no image found in the input directory")
    
    boundingboxes = []
    print(f"-> calculating smallest binding box: (0/{input_image_path.__len__()})")
    disp_counter = 0
    
    for path in input_image_path:
        disp_counter += 1
        print(f"\u001b[1F-> calculating smallest binding box: ({disp_counter}/{input_image_path.__len__()})")
        img = cv.imread(path.as_posix())
        boundingboxes.append(getboundingbox(img))

    bound = getbiggestboundingbox(boundingboxes)
    print(f"-> creating optimized sprite: (0/{input_image_path.__len__()})")
    
    disp_counter = 0
    for p in input_image_path:
        disp_counter += 1
        print(f"\u001b[1F-> creating optimized sprite: ({disp_counter}/{input_image_path.__len__()})")
        path = p.as_posix()
        img = cv.imread(path)
        roi = img[bound[1]:bound[3]+1,bound[0]:bound[2]+1]

        output_path = pathlib.Path(__args__["o"]+ path[len(__args__["i"]):])
        if not os.path.exists(output_path.parent):
            os.makedirs(output_path.parent)
        cv.imwrite(output_path.as_posix(),roi)
    
    print(f"-> finished sprite optimization\nexiting program")
    
    input("press ENTER to exit")
    return

if __name__ == "__main__":
    main()