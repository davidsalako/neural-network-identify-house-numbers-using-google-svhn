# Neural Networks - A Model That Can Accurately Identify House Numbers In An Image Using Google's Street View House Numbers (SVHN) Dataset. - By David Salako.

## Background and Context

The ability to process visual information using machine learning algorithms can be very useful as demonstrated in various applications. The Street View House Numbers (SVHN) dataset is one of the most popular ones. It has been used in neural networks created by Google to read house numbers and match them to their geolocations. This is a great benchmark dataset to play with, learn and train models that accurately identify street numbers, and incorporate them into all sorts of projects.

## Objective

In this project, we will use a dataset with images centered around a single digit (many of the images do contain some distractors at the sides). Although this is a sample of the data which is simple, it is more complex than MNIST because of the distractors. Given the dataset, the aim is to build a model that can identify house numbers in an image.

## Dataset

The SVHN dataset (SVHN_single_grey1.h5) has the following features:

    Number of classes: 10
    Training data: 42000 images
    Validation data: 60000 images
    Testing data: 18000 images
    
The large image file in .h5 format is freely available online.
