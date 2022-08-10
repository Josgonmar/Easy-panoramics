# EASY PANORAMICS
This program creates a panoramic image from several individual images taken from the same position, sequentially.
Even though OpenCV has a high level function to perform this operation, I've added several additional operations in order to crop the resulting image, avoiding those black borders the [Stitcher()](https://docs.opencv.org/4.x/d2/d8d/classcv_1_1Stitcher.html) class generates.
## Dependencies:
* [Python](https://www.python.org/doc/) - 3.10.5
* [OpenCV](https://docs.opencv.org/4.6.0/) - 4.6.0
* [Numpy](https://numpy.org/doc/stable/) - 1.22.4
## How to use:
1. Copy all the images inside the */visuals* folder. Make sure they are all sorted in the same order they where originally taken. You can rename them in order to do this.
2. Go to the *src* folder and execute `Panoramas.py`
```console
    $ python Panoramas.py
```
3. Once the work is done (a message will be printed in the console), you will find the resulting image as `output.jpg`

Originally, the panorama would result in this:

![alt text](https://github.com/Josgonmar/Easy-panoramics/blob/master/docs/before.jpg?raw=true)

To automatically remove those black borders, several morphological operations are performed.
First, we convert it into a gray scale picture, so we can perform a thresholding operation and obtain a binary mask.
We then detect the contour within the mask, and fill it to get rid of the black holes that may appear using the [Stitcher()](https://docs.opencv.org/4.x/d2/d8d/classcv_1_1Stitcher.html) class.
After that, we create a new mask containing the filled bounding box of the contour previously obtained.

This rectangle will be eroded and substracted to the threshold image while there are still non-zero pixels. The resulting binary mask should contain a filled rectangle that fits inside the contour, getting as less black border pixels as possible.

![alt text](https://github.com/Josgonmar/Easy-panoramics/blob/master/docs/after.jpg?raw=true)

*Note that some image information may be lost, as the original one will be cropped.*

There are several demo images already in the */visuals* folder to try the code, but feel free to try it with your own pictures.
## License:
Feel free to use this programa whatever you like!
