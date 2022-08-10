import numpy as np
import cv2
import os

class Panorama:
    __folder_path = '../visuals'
    __images = []
    __stitcher_obj = None

    def __init__(self):
        self.__stitcher_obj = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)

    def run(self):
        self.__loadImages()

        status, result = self.__stitcher_obj.stitch(self.__images)
        if status == 0:
            cropped_result = self.__cropResult(result)
            self.__saveResult(cropped_result)
        else:
            print('[ERROR] Cannot stitch images. Error code: ', str(status))

        cv2.destroyAllWindows()

    def __cropResult(self, image):
        cropped_img = image.copy()
        bw_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
        bw_image = cv2.copyMakeBorder(bw_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0,0,0))
        ret, thresh_img = cv2.threshold(bw_image, 0, 255, cv2.THRESH_BINARY)

        print('[INFO] Cropping the stitched image... This may take a while')
        try:
            contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_contour = max(contours, key = cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(max_contour)

            # In some cases, the stitched image could contain black holes that prevent the panorama from being as big as possible
            thresh_img = cv2.fillPoly(thresh_img, pts=[max_contour], color=(255,255,255))

            full_contour_mask = np.zeros(thresh_img.shape, dtype='uint8')
            cv2.rectangle(full_contour_mask, (x, y), (x + w, y + h), 255, -1)
            contained_bbox = full_contour_mask.copy()
            substraction = full_contour_mask.copy()
            kernel = np.ones((3,3), dtype='uint8')

            while cv2.countNonZero(substraction) > 0:
                contained_bbox = cv2.erode(contained_bbox, kernel)
                substraction = cv2.subtract(contained_bbox, thresh_img)

            contours, hierarchy = cv2.findContours(contained_bbox, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_contour = max(contours, key = cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(max_contour)
            
            cropped_img = cropped_img[y:y+h, x:x+w, :]
        except:
            print('[WARNING] The cropping action did not conclude')

        return cropped_img

    def __loadImages(self):
        try:
            for file in os.listdir(self.__folder_path):
                if file != 'output.jpg':
                    image = cv2.imread(self.__folder_path + '/' + file, cv2.IMREAD_COLOR)
                    cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    self.__images.append(image)
            print('[INFO] Loaded a total of', len(self.__images), 'images')
        except:
            print('[ERROR] An error occured while reading the images')
    
    def __saveResult(self, image):
        try:
            filename = '/output.jpg'
            cv2.imwrite(self.__folder_path + filename, image)
            print('[INFO] Correctly saved image in:', self.__folder_path + filename)
        except:
            print('[ERROR] An error occurred while saving the image')



if __name__ == "__main__":
    Panorama_obj = Panorama()
    Panorama_obj.run()