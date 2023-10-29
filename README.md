# Sprite Sheet tools

Those tools are made to facilitate the use of my custom shader for unity and vrchat. You can use them for other purpose but they are not optimized for those uses.

## prerequisites

install python to run the scripts

## optimizer

### how to use:

! WARNING ! ALL IMAGES MUST HAVE THE SAME STANDARD SIZE ex: 64x64, 256x32; if you have multiple file sizes (ex: your characters are 64x64 but your trees are 256x256) you must seperate them and optimize them separetly.

1. put all of your sprites into a folder (the folder can be arranged in multiple sub folders)

2. run the script with the correct arguments (if the input path is not given it will try and use a folder named input in the same folder as the script if it exist)

    the arguments are:
    
    -i "{INPUT_PATH}" the path to the input directory

    -o "{OUTPUT_PATH}" the path to the output directory

3. the optimized images should be in the output path if not given it will create a folder named output in the same path as the script (if the path is given but the path dosnt exist it will create the folder by itself).

## Sheet Packer

For this part there is no need to separate the different files sizes.

1. put all of your sprites in a folder the hierarchy of the folders will dictate how the final atlas will look like (i recommend renaming the folders starting with a number so they are in the correct order)

2. run the script with the correct arguments (if the input path is not given it will try and use a folder named input in the same folder as the script if it exist)

    the arguments are:
    
    -i "{INPUT_PATH}" the path to the input directory

    -o "{OUTPUT_PATH}" the path to the output directory

    -n "{NAME}" the name of the finished spritesheet

3. the resulting spritesheet will be in the given output path.