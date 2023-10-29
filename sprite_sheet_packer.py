import sys
import cv2 as cv
import pathlib
import os
import numpy as np

# -i for specifying input directory (will recursively go through it)
# -o specify the output direcory
# -n name of the atlas file

def getargs():
    lookup = [
        ["i","o","n"]
    ]

    #get all args
    args = sys.argv
    flags = {}
    
    for flag in lookup[0]:
        try:
            index = args.index(f"-{flag}")
            if index < (args.__len__() - 1):
                flags[flag] = args[index + 1]
            else:
                flags[flag] = None
        except ValueError:
            flags[flag] = None
            
    return flags
    
def error(message):
    print(message)
    sys.exit()

def makeatlas(dirpath):
    filepaths = list(filter(lambda item: item.is_file(), dirpath.glob("*")))
    dirpaths = list(filter(lambda item: item.is_dir(), dirpath.glob("*")))
    
    dirpaths_len = dirpaths.__len__()
    filepaths_len = filepaths.__len__()
    
    #image files in subdir
    recursivesheetsimages = []
    for i in range(dirpaths_len):
        recursivesheetsimages.append(makeatlas(dirpaths[i]))
        
    #image file in dir
    images = []
    sprite_sizes = []
    sheet_size = [0,0,3]
    for i in range(filepaths_len):
        images.append(cv.imread(filepaths[i].as_posix()))
        shape = images[i].shape
        sheet_size[0] += shape[1]
        sheet_size[1] = shape[0] if shape[0] > sheet_size[1] else sheet_size[1]
        sprite_sizes.append([shape[1],shape[0]])
        
    
    
    sheetimage = np.zeros((sheet_size[1],sheet_size[0],3), np.uint8)
    
    offsetX = 0
    for i in range(filepaths_len):
        sheetimage[0:sprite_sizes[i][1],offsetX:offsetX + sprite_sizes[i][0]] = images[i]
        offsetX += sprite_sizes[i][0]
            
    #find the size of the atlas
    atlas_size = [sheet_size[1],sheet_size[0],sheet_size[2]]
    for i in range(recursivesheetsimages.__len__()):
        shape = recursivesheetsimages[i].shape
        atlas_size[0] += shape[0] 
        atlas_size[1] = shape[1] if shape[1] > atlas_size[1] else atlas_size[1]
    
    atlasimage = np.zeros((atlas_size[0],atlas_size[1],3), np.uint8)
    if sheet_size != [0,0,3]:
        atlasimage[0:sheet_size[1], 0:sheet_size[0]] = sheetimage

    offsetY = sheet_size[1]
    for i in range(recursivesheetsimages.__len__()):
        atlasimage[offsetY:offsetY + recursivesheetsimages[i].shape[0],0:recursivesheetsimages[i].shape[1]] = recursivesheetsimages[i]
        offsetY += recursivesheetsimages[i].shape[0]

    return atlasimage

def main():
    
    __args__ = getargs()    
    __dirpath__ = os.path.dirname(os.path.realpath(__file__))
    
    if __args__["i"] == None:
        __args__["i"] = os.path.join(__dirpath__,"input")
        if not os.path.exists(__args__["i"]):
            error("the input directory does not exist")
    if __args__["o"] == None:
        __args__["o"] = __dirpath__
    if __args__["n"] == None:
        __args__["n"] = "atlas"
    
    
    
    print(f"\nstarting sprite_sheet_spliter on the directories :")
    print(f"input :  \"{__args__['i']}\"")
    print(f"output :  \"{__args__['o']}\"")
    print(f"output file name :  \"{__args__['n']}\"\n")

    input_path = pathlib.Path(__args__["i"])
    
    if list(filter(lambda item: item.is_file(), input_path.rglob("*"))).__len__() == 0 :
        error("no images found in the given input file")

    img = makeatlas(input_path)
    
    print(f"writing {__args__['n']}.png in output directory")
    
    atlaspath = f"{os.path.join(__args__['o'],__args__['n'])}.png"
    cv.imwrite(atlaspath,img)    
    return

if __name__ == "__main__":
    main()