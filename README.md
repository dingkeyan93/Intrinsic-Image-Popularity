# Intrinsic image popularity Predictor

This is a PyTorch implementation of *Intrinsic Image Popularity Prediction: Focusing on the Visual Content*.

This work can objectively and quantitatively predict how much traction an image will get on Instagram by computing the image popularity score. It can help users to choose the image that would be the most popular to the public.

run ```python test.py <image_path>``` to evaluate thr intrinsic image popularity of your photos on Instagram. 

Here is our [Web Demo](http://popularity.keyan.work/).

**Wait to add**:
1. The raw data of Instagram post information, contains the collection time, post url, id, content type, upload time, caption (including emojis, hashtags and @ people), the number of likes and comments.
This is the first publicly available large-scale dataset on Instagram. It opens the doors for several interesting directions on Instagram, not only for image popularity prediction, but image captioning, image tagging, emoji prediction, visual and text sentiment analysis and so on.

2. The generated 2.5m DPIP dataset, including training set and testing set.
