# -*- coding: utf-8 -*-
import argparse
import os
import torch
import torchvision.models
import torchvision.transforms as transforms
from PIL import Image
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def prepare_image(image):
    if image.mode != 'RGB':
        image = image.convert("RGB")
    Transform = transforms.Compose([
        transforms.Resize([224, 224]),
        transforms.ToTensor(),
    ])
    image = Transform(image)
    image = image.unsqueeze(0)
    return image.to(device)


def predict(image, model):
    image = prepare_image(image)
    with torch.no_grad():
        preds = model(image)
    print(r'Popularity score: %.2f' % preds.item())


def setUpModel():
    model = torchvision.models.resnet50()
    # model.avgpool = nn.AdaptiveAvgPool2d(1) # for any size of the input
    model.fc = torch.nn.Linear(in_features=2048, out_features=1)
    model.load_state_dict(torch.load(
        'model/model-resnet50.pth', map_location=device))
    model.eval().to(device)
    return model


def setArgParser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-path', dest="path", nargs='+',
                        help="file or folder path")
    parser.add_argument('-e', dest="ext", help='filter extension type')
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
            print(fileName)
            predict(image, model)


if __name__ == '__main__':
    model = setUpModel()
    args = setArgParser()
    rateImages(model, args.path)
