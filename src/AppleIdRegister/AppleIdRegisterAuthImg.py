#!/usr/bin/python3
#coding=utf-8

##############################################
#
# Author:       Shen Wenrui
# Date:         20180522
# Description:
#
##############################################

import base64
#from IPython.display import Image
import PIL.Image

from .AppleIdRegisterXpath import appleIdRegisterXpath
from .AutoCodeRecognizeLib import authImgRecongizer


class appleIdAuthImgOpt():
    def __init__(self, appleIdRegisterBrowser):
        self.__xpath = appleIdRegisterXpath()
        self.__appleIdRegisterBrowser = appleIdRegisterBrowser
        self.__authImgRecongizer = authImgRecongizer()

    # Auth image.
    def __extractAuthImg(self):
        try:
            authImgBase64Xpath = self.__xpath.getAuthImgBase64Xpath()

            authImgElement = self.__appleIdRegisterBrowser.find_element_by_xpath(authImgBase64Xpath)
            # print('authImgElement is: ' + str(authImgElement.get_attribute('innerHTML')))

            authImgBase64 = authImgElement.get_attribute('src')
            # print(authImgBase64)
            return authImgBase64
        except Exception as err:
            print("[ERROR] ExtractAuthImg Failed: " + repr(err))
            return None

    def __saveAuthImg(self, authImgBase64, filename='001.jpeg'):
        authImgStr = base64.b64decode(authImgBase64[len('data:image/jpeg;base64, '):])
        authImg_f = open("001.jpeg", "wb")
        authImg_f.write(authImgStr)
        authImg_f.close()

    #def __showAuthImg(self, filename='001.jpeg'):
        # Show in jupyter:
        #Image(filename)

        # show in system:
        #im = PIL.Image.open('001.jpeg')
        #im.show()

    def __recognizeAuthImg(self, authImgBase64):
        parsed_auth_code = self.__authImgRecongizer.authCodeParseRequest(authImgBase64[len('data:image/jpeg;base64, '):])
        # parsed_auth_code = "CF6MZ"
        print(parsed_auth_code)
        return None

    def __inputAutnCode(self, recognizedAuthCode):
        authCodeInputXpath = self.__xpath.getAuthCodeInptuXpath()
        authCodeInputElement = self.__appleIdRegisterBrowser.find_element_by_xpath(authCodeInputXpath)
        authCodeInputElement.clear()
        authCodeInputElement.send_keys(recognizedAuthCode)
        return False

    def appleIdAuthImgProcessor(self):
        authImgBase64 = self.__extractAuthImg()
        recognizedAuthCode = self.__recognizeAuthImg(authImgBase64)
        self.__inputAutnCode(recognizedAuthCode)
        return True

