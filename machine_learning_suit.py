# -*- coding: utf-8 -*-
"""machine-learning-suit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xLJumpUZKb6GDAN7w5TP4dI1pvIk_hiV

Nama : Ilzan Afif <br>

Email : ilzamafif@gmail.com

import libraray tensorflow
"""

import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator

"""cek versi dari tensorflow"""

print(tf.__version__)

"""download dataset"""

!wget --no-check-certificate https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip -O rockpaperscissors.zip

"""melakukan extraksi pada file"""

import zipfile,os
local_zip = 'rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('rps')
zip_ref.close()

"""install splitfolders"""

!pip install split_folders

"""mengimpor splitfolders dan memecah dir """

import splitfolders
 
splitfolders.ratio('rps/rockpaperscissors/rps-cv-images', 'rps/rockpaperscissors/data', seed=1, ratio=(.6, .4))

"""base dir"""

base_dir = 'rps/rockpaperscissors/data'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'val')
os.listdir('rps/rockpaperscissors/data/train')
os.listdir('rps/rockpaperscissors/data/val')

train_rock_dir = os.path.join(train_dir, 'train')
train_scissors_dir = os.path.join(train_dir, 'scissors')
train_paper_dir = os.path.join(train_dir, 'paper')
 
validation_crock_dir = os.path.join(validation_dir, 'rock')
validation_scissors_dir = os.path.join(validation_dir, 'scissors')
validation_paper_dir = os.path.join(validation_dir, 'paper')

from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
  rescale=1./255, # rescale all pixel values from 0-255, so aftre this step all our pixel values are in range (0,1)
  shear_range=0.2, #to apply some random tranfromations
  zoom_range=0.2, #to apply zoom
  horizontal_flip=True) # image will be flipper horiztest_datagen = ImageDataGenerator(rescale=1./255)
 
test_datagen = ImageDataGenerator(
  rescale=1./255, # rescale all pixel values from 0-255, so aftre this step all our pixel values are in range (0,1)
  shear_range=0.2, #to apply some random tranfromations
  zoom_range=0.2, #to apply zoom
  horizontal_flip=True)

"""train"""

train_generator = train_datagen.flow_from_directory(
  train_dir, # set to the path where your ‘n’ classes of folders are present.
  target_size=(224, 224),# size of your input images, every image will be resized to this size.
  batch_size=32, # No. of images to be yielded from the generator per yu.
  color_mode='rgb', # if the image is either black and white or grayscale set “grayscale” or if the image has three color channels, set “rgb”.
  class_mode='categorical', # Set “binary” if you have only two classes to predict, if not set to“categorical”, in case if you’re developing an Autoencoder system, both input and the output would probably be the same image, for this case set to “input”
  shuffle = True, # Set True if you want to shuffle the order of the image that is being yielded, else set False
  seed=42) # Random seed for applying random image augmentation and shuffling the order of the image.
validation_generator = test_datagen.flow_from_directory(
  validation_dir,
  target_size=(224, 224),
  batch_size=32,
  color_mode='rgb',
  class_mode='categorical',
  shuffle = True,
  seed=42)

sample_train_images, _ = next(train_generator)
sample_val_images, _ = next(validation_generator)

def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

"""import matlotlib"""

import matplotlib.pyplot as plt
 
plotImages(sample_train_images[:5])
plotImages(sample_val_images[:5])

"""confiurasi model"""

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])
 
model.summary()

"""mengkompile model"""

model.compile(loss='categorical_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])

"""train model"""

historrry = model.fit(train_generator, 
          steps_per_epoch=25, 
          epochs=20, 
          validation_data=validation_generator,
          validation_steps=5,
          verbose=1)

"""menampilkan hasil training resource"""

import matplotlib.pyplot as plt
 
acc = historrry.history['accuracy']
val_acc = historrry.history['val_accuracy']
 
loss = historrry.history['loss']
val_loss = historrry.history['val_loss']
 
plt.plot(acc, color='blue')
plt.plot(val_acc, color='red')
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
 
plt.plot(loss, color='blue')
plt.plot(val_loss, color='red')
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

"""menjalankan prediksi"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline
 
uploaded = files.upload()
 
for fn in uploaded.keys():
 
  # predicting images
  path = fn
  img = image.load_img(path, target_size=(224,224))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
 
  images = np.vstack([x])
  classes = model.predict(images, batch_size=32)
 
  if classes[0,0]!=0:
    print('PAPER')
  elif classes[0,1]!=0:
    print('ROCK')
  else:
    print('SCISSORS')