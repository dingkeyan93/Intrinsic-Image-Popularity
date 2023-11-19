# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image
from django.conf import settings
from urllib.request import urlopen
from io import BytesIO
from google.cloud import storage

import logging

logger = logging.getLogger(__file__)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.debug(device.type)
logger.debug(
    f'path: {os.path.join(os.getcwd(), "credential.json")}, creds: {settings.GS_CREDENTIALS}'
)
# logger.debug(f'GCP MODE: {settings.GCP_DEV}, su: {os.environ.get("DJANGO_SUPERUSER_PASSWORD")}, {os.environ.get("DJANGO_SUPERUSER_USERNAME")}')


popularityDictionary = {}


def prepare_image(image):
    logger.debug("prepare")
    if image.mode != "RGB":
        image = image.convert("RGB")
    Transform = transforms.Compose(
        [
            transforms.Resize([224, 224]),
            transforms.ToTensor(),
        ]
    )
    image = Transform(image)
    image = image.unsqueeze(0)
    logger.debug(image.to(device))
    return image.to(device)


def predict(image, model):
    logger.debug("predict")
    image = prepare_image(image)
    # logger.debug(image)
    with torch.no_grad():
        # logger.debug(model)
        preds = model(image)
        logger.debug(preds.item())
    return round(preds.item(), 4)


def setUpModel():
    model = torchvision.models.resnet50()
    # model.avgpool = nn.AdaptiveAvgPool2d(1) # for any size of the input
    model.fc = torch.nn.Linear(in_features=2048, out_features=1)
    model.load_state_dict(torch.load("model/model-resnet50.pth", map_location=device))
    model.eval().to(device)
    return model


def setArgParser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-path", dest="path", nargs="+", help="file or folder path")
    parser.add_argument("-e", dest="ext", help="filter extension type")
    args = parser.parse_args()
    return args


def getImagePaths(paths):
    imagePaths = set()
    for root, dirs, files in os.walk(os.path.join(paths)):
        for fileName in files:
            imagePaths.add(os.path.join(root, fileName))
        for dirName in dirs:
            imagePaths.union(getImagePaths(os.path.join(root, dirName)))
    return imagePaths


def rateImages(model, paths):
    paths = getImagePaths(paths[0])
    for path in paths:
        if os.path.isfile(path):
            fileName, fileExtension = os.path.splitext(path)
        if args.ext == fileExtension:
            image = Image.open(path)
            popularityDictionary[fileName] = predict(image, model)


def setUpModelApp(modelPath):
    logger.debug(modelPath)
    model = torchvision.models.resnet50()
    # model.avgpool = nn.AdaptiveAvgPool2d(1) # for any size of the input
    model.fc = torch.nn.Linear(in_features=2048, out_features=1)
    model.load_state_dict(torch.load(modelPath, map_location=device))
    model.eval().to(device)
    with open(os.path.join(os.getcwd(), "state_dict.txt"), "w") as neep:
        for tensor in model.state_dict():
            neep.write(f'{tensor}: {model.state_dict()[tensor]}\n')
        neep.close()
    return model


def rateImagesApp(imagePath, modelPath):
    logger.debug("In rateImagesApp")
    try:
        popularityDictionary = {}
        logger.debug(modelPath)
        try:
            model = setUpModelApp(os.path.abspath(modelPath))
        except Exception as err:
            raise err
        logger.debug("post model setup")
        for path in imagePath:
            if settings.LOCAL_DEV and settings.GCP:
                logger.debug("A path:" + path)
                processedPath = os.path.abspath(os.curdir + "/IIPA/media" + path)
                logger.debug("A.1 processed path" + processedPath)
                fileName = None
                fileExtension = None
                if os.path.isfile(processedPath):
                    fileName, fileExtension = os.path.splitext(processedPath)
                    logger.debug(fileName, fileExtension)
                if fileExtension != None:
                    if fileExtension in [".jpg", ".jpeg", ".png"]:
                        image = Image.open(processedPath)
                        logger.debug(image)
                        popularityDictionary[path] = predict(image, model)
                        logger.debug(popularityDictionary, "ffff")
                else:
                    logger.debug(path + " C")
            else:
                logger.debug("B not local")
                logger.debug(path)
                gStorage = storage.Client(credentials=settings.GS_CREDENTIALS)
                processedPath = gStorage._http.get(path).content

                image = Image.open(BytesIO(processedPath))
                # logger.debug("im: " + image.__str__())
                x = predict(image, model)
                logger.debug("prediction: " + str(x))
                popularityDictionary[path] = x
                # logger.debug(popularityDictionary.__str__())
            return popularityDictionary
    except Exception as err:
        logger.debug(err)
        raise err


if __name__ == "__main__":
    model = setUpModel()
    args = setArgParser()
    rateImages(model, args.path)
    print(dict(sorted(popularityDictionary.items(), key=lambda item: item[1])))
