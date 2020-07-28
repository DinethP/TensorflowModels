# -*- coding: utf-8 -*-
"""Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZN4INgfZqqgz7zEYPXIWDi9eCkcxcn_9
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x  # this line is not required unless you are in a notebook

from __future__ import absolute_import, division, print_function, unicode_literals


import tensorflow as tf

import pandas as pd

CSV_COLUMN_NAMES = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'Species']
SPECIES = ['Setosa', 'Versicolor', 'Virginica']
# Lets define some constants to help us later on

train_path = tf.keras.utils.get_file(
    "iris_training.csv", "https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv")
test_path = tf.keras.utils.get_file(
    "iris_test.csv", "https://storage.googleapis.com/download.tensorflow.org/data/iris_test.csv")
#Get the files from Keras and store them locally

train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
test = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)
# Here we use keras (a module inside of TensorFlow) to grab our datasets and read them into a pandas dataframe

train.head()
# We can see that our labels (Species) is already defined numerically. We don't need to convert the categorical data to numerical data

train_y = train.pop('Species')
test_y = test.pop('Species')
train.head()



train.shape  # we have 120 entires with 4 features

# input_fn doesn't return a function
def input_fn(features, labels, training=True, batch_size=256):
  # Convert the inputs to a Dataset
  # We dont need to find unique values to categorise because the labels are already numeric
  dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

  # Shuffle and repeat if you are in training mode
  if training:
    dataset = dataset.shuffle(1000).repeat()

  return dataset.batch(batch_size)

# Feature columns describe how to use the input.
my_feature_columns = []
for key in train.keys():
  my_feature_columns.append(tf.feature_column.numeric_column(key=key))
print(my_feature_columns)

"""###Building the Model
And now we are ready to choose a model. For classification tasks there are variety of different estimators/models that we can pick from. Some options are listed below.
- ```DNNClassifier``` (Deep Neural Network)
- ```LinearClassifier```

We can choose either model but the DNN seems to be the best choice. This is because we may not be able to find a linear coorespondence in our data.
"""

# Build a DNN with 2 hidden layers with 30 and 10 hidden nodes each.
classifier = tf.estimator.DNNClassifier(
    feature_columns = my_feature_columns,
    # Two hidden layers of 30 and 10 nodes respectively.
    hidden_units = [30,10],
    # The model must choose between 3 classes.
    n_classes = 3
)

# Train the model

# We use a lambda anonymous function because our input_fn above doesn't return a function.
# So we use the lambda function to call the input_fn() => A function calling a function
# We include a lambda to avoid creating an inner function previously
classifier.train(
    input_fn = lambda: input_fn(train, train_y, training=True),
    steps = 5000
)

# Test the model

eval_result = classifier.evaluate(
  input_fn=lambda: input_fn(test, test_y, training=False))

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

def input_fn(features, batch_size=256):
    # Convert the inputs to a Dataset without labels.
    return tf.data.Dataset.from_tensor_slices(dict(features)).batch(batch_size)

features = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
predict = {} # store predicted values from the model. Predictions are outputted as dictionary, so this stores a dictionary of dictionaries

print("Please type numeric values as prompted.")

# Get a valid numerical response from user for each feature
for feature in features:
  valid = True
  while valid: 
    val = input(feature + ": ")
    if not val.isdigit(): valid = False

  predict[feature] = [float(val)] # Even if we are only testing for one data item, 'classifier.predict()' requires it to be in a list object.

predictions = classifier.predict(input_fn=lambda: input_fn(predict))
for pred_dict in predictions: # Each predicted dictionary
    print(pred_dict)
    class_id = pred_dict['class_ids'][0]
    probability = pred_dict['probabilities'][class_id]

    print('Prediction is "{}" ({:.1f}%)'.format(
        SPECIES[class_id], 100 * probability))

# Here is some example input and expected classes you can try above
expected = ['Setosa', 'Versicolor', 'Virginica']
predict_x = {
    'SepalLength': [5.1, 5.9, 6.9],
    'SepalWidth': [3.3, 3.0, 3.1],
    'PetalLength': [1.7, 4.2, 5.4],
    'PetalWidth': [0.5, 1.5, 2.1],
}