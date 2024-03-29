#Importing keras libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from cv2 import cv2
import joblib
import numpy as np
from keras.preprocessing import image

#Initializing CNN
classifier = Sequential()

#1Convolution
classifier.add(Convolution2D(32,3,3,padding='same',input_shape = (64,64,3), activation = 'relu'))

#2Pooling
classifier.add(MaxPooling2D(pool_size = (2,2)))

#adding 2nd and 3rd convolution layer
classifier.add(Convolution2D(32,3,3, activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2,2)))
classifier.add(Convolution2D(32,3,3, activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2,2)))

#3Flattening
classifier.add(Flatten())

#4Full_Connection
classifier.add(Dense(output_dim=128,activation = 'relu'))
classifier.add(Dense(output_dim=1,activation = 'sigmoid'))

#Compiling CNN
classifier.compile(optimizer = 'adam', loss= 'binary_crossentropy', metrics = ['accuracy'])

#Fitting CNN to images

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

train_datagen = ImageDataGenerator(rescale = 1./255)
print("\nTraining the data...\n")
training_set = train_datagen.flow_from_directory('train',
                                                target_size=(64,64),
                                                batch_size=32,
                                                class_mode='binary')

test_set = train_datagen.flow_from_directory('test',
                                            target_size=(64,64),
                                            batch_size=32,
                                            class_mode='binary')

classifier.fit_generator(training_set,
                         samples_per_epoch=100,
                         nb_epoch = 1,
                         validation_data =test_set,
                         nb_val_samples = 20)

#Making new predictions
print("\nMaking predictions for uploaded X-ray...\n")

test_image = image.load_img('corona.jpg',target_size=(64,64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)
if result[0][0] == 1:
    prediction = 'Patient is affected with Corona'
else:
    prediction = 'Patient is Healthy'
    print("\nOutcome : ",prediction)    
    
import matplotlib.pyplot as plt 
      
# reads the image 
img = cv2.imread('corona.jpg') 
im_gray = cv2.imread('corona.jpg', cv2.IMREAD_GRAYSCALE)
heatmap_img = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)
fin = cv2.addWeighted(heatmap_img, 0.7, img, 0.3, 0)
# plot heat map image 
fig=plt.figure(figsize=(18, 18))
fig.add_subplot(1,3,1)
plt.imshow(img)
fig.add_subplot(1,3,2)
plt.imshow(heatmap_img)
fig.add_subplot(1,3,3)
plt.imshow(fin)
plt.savefig('output.png')

