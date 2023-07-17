import cv2
import cv2.aruco as arucom
import numpy as np
import os, sys
import base64


class Aruco:
    def __init__(self):
        # define names of each possible ArUco tag OpenCV supports
        self.ARUCO_DICT = {
            "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
            "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
            "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
            "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
            "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
            "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
            "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
            "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
            "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
            "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
            "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
            "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
            "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
            "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
            "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
            "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
            "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
            "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
            "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
            "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
            "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
        }

    def findArucoTYPE(self, img):
        try:
            # loop over the types of ArUco dictionaries
            for (arucoName, arucoDict) in self.ARUCO_DICT.items():
                # load the ArUCo dictionary, grab the ArUCo parameters, and
                # attempt to detect the markers for the current dictionary
                arucoDict = cv2.aruco.Dictionary_get(arucoDict)
                arucoParams = cv2.aruco.DetectorParameters_create()
                (corners, ids, rejected) = cv2.aruco.detectMarkers(
                    img, arucoDict, parameters=arucoParams)
                # if at least one ArUco marker was detected display the ArUco
                # name to our terminal
                lst = []
                if len(corners) > 0:
                    print("[INFO] detected {} markers for '{}'".format(len(corners), arucoName))
                    lst.append(arucoName)
                    return True, lst
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return False, []

    def findArucoMarkers(self, img, markerSize=4, totalMarkers=250, draw=True):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            key = getattr(arucom, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
            arucoDict = arucom.Dictionary_get(key)
            arucoParam = arucom.DetectorParameters_create()
            corners, id, rejected = arucom.detectMarkers(gray, arucoDict, parameters=arucoParam)
            print("Aruco IDs:", id)
            if draw:
                arucom.drawDetectedMarkers(img, corners)

            if len(corners) > 0:
                # flatten the ArUco IDs list
                id = id.flatten()
                # loop over the detected ArUCo corners
                for (markerCorner, markerID) in zip(corners, id):
                    corners = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
                    img = cv2.putText(img, str(markerID),
                                      (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                                      0.5, (0, 255, 0), 2)
                    image_64_encode = base64.encodestring(img)
                    print("Base64 Encoded Image:", image_64_encode)
                    return True, image_64_encode

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return False, "Internal error"

    def findAruco(self, path):
        try:
            cap = cv2.imread(path)

            while True:
                success, img = cap.read()
                print("Read Success:", success)
                if success == False:
                    break
                else:
                    status, types = self.findArucoTYPE(img)
                    if status == False:
                        return False, "Internal error", 500

                    if types:
                        size = (types[0].split("_")[1]).split("X")[0]
                        print("Size:", size)

                    status, resp = self.findArucoMarkers(img, size)
                    if status == False:
                        return False, "Internal error", 500

                    k = cv2.waitKey(30) & 0xff
                    if k == 94:
                        break
            cap.release()
            cv2.destroyAllWindows()
            return True, resp, 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return False, "Internal error"


aruco_obj = Aruco()
status, response, code = aruco_obj.findAruco("images\padded.png")
print("Status:", status)
print("Response:", response)
print("Code:", code)
