# Intrinsic image popularity Assessment

This is a PyTorch implementation of the paper [Intrinsic Image Popularity Assessment](https://arxiv.org/abs/1907.01985).

This work can quantitatively predict how much traction an image will get on Instagram. 

It can help users to find the image that would be the most popular to the public.

Run ```python test.py --image_path <image_path>``` to evaluate the intrinsic image popularity of your photos on Instagram. 

<!-- This is the [Online Demo](https://iipa.ngrok2.xiaomiqiu.cn) (unstable). -->

This project use the MIT license.

### Dataset
We provide the dataset of popularity-discriminable image pairs by the form of "shortcode". You can download the images with the URL ```"https://www.instagram.com/p/<shortcode>/media/?size=l".``` 

*Note, some URLs may be invalid now.*

### Citation
```
@inproceedings{ding2019intrinsic,
  title={Intrinsic Image Popularity Assessment},
  author={Ding, Keyan and Ma, Kede and Wang, Shiqi},
  booktitle={ACM International Conference on Multimedia},
  pages={1979--1987},
  year={2019},
  publisher={ACM}
}
```
