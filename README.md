# Intrinsic image popularity Predictor

This is a PyTorch implementation of the paper [*Intrinsic Image Popularity Assessment*](https://arxiv.org/abs/1907.01985).

This work can objectively and quantitatively predict how much traction an image will get on Instagram. 
It can help users to find the image that would be the most popular to the public.

run ```python test.py <image_path>``` to evaluate thr intrinsic image popularity of your photos on Instagram. 

This is the [Online Demo](http://e9mp3u.natappfree.cc).

### Dataset
We provide the dataset of popularity-discriminable image pairs by the form of "shortcode". You can download the images with the URL ```"https://www.instagram.com/p/<shortcode>/media/?size=l".``` 

*Note, some URLs may be invalid now.*

### Citation
```
@inproceedings{ding2019intrinsic,
  title={Intrinsic Image Popularity Assessment},
  author={Ding, Keyan and Ma, Kede and Wang, Shiqi},
  booktitle={ACM Multimedia}, 
  year={2019}
}
```
