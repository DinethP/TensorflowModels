# -*- coding: utf-8 -*-
"""HiddenMarkovModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mKCxp9f5mxAOZXzpYxD4HmH_F9JXZLTF
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x  # this line is not required unless you are in a notebook

!pip install tensorflow_probability --user --upgrade

import tensorflow_probability as tfp  # We are using a different module from tensorflow this time
import tensorflow as tf

"""###Weather Model
Taken direclty from the TensorFlow documentation (https://www.tensorflow.org/probability/api_docs/python/tfp/distributions/HiddenMarkovModel). 

We will model a simple weather system and try to predict the temperature on each day given the following information.
1. Cold days are encoded by a 0 and hot days are encoded by a 1.
2. The first day in our sequence has an 80% chance of being cold.
3. A cold day has a 30% chance of being followed by a hot day.
4. A hot day has a 20% chance of being followed by a cold day.
5. On each day the temperature is
 normally distributed with mean and standard deviation 0 and 5 on
 a cold day and mean and standard deviation 15 and 10 on a hot day.

If you're unfamiliar with **standard deviation** it can be put simply as the range of expected values. 

In this example, on a hot day the average temperature is 15 and ranges from 5 to 25.

To model this in TensorFlow we will do the following.
"""

# Create distributiom values to model our weather system

tfd = tfp.distributions # making a shortcut for later on
# our probability notation will be [cold_day, hot_day]
initial_distribution = tfd.Categorical(probs=[0.8, 0.2]) # Refer to point 2 above (We have 2 states, so have 2 probabilities)
transition_distribution = tfd.Categorical(probs=[[0.7, 0.3],
                                                [0.2, 0.8]]) # refer to points 3 and 4 above
observation_distribution = tfd.Normal(loc=[0., 15.], scale=[5., 10.])
# the loc argument represents the mean and the scale is the standard devitation
# Average temperature is 0 on a hot day, 15 on a cold day    
# Standard deviation is 5 for a hot day, 10 for a cold day           
# A dot is added to make them float values as tfd.Normal() requires float values

# Build the model

model = tfd.HiddenMarkovModel(
    initial_distribution = initial_distribution,
    transition_distribution = transition_distribution,
    observation_distribution = observation_distribution,
    num_steps = 7  # Steps is how day we want to predict for
)

# Get the expected temperatures on each day
mean = model.mean() # model.mean() is a partially defined tensor

# due to the way TensorFlow works on a lower level we need to evaluate part of the graph
# from within a session to see the value of this tensor

# in the new version of tensorflow we need to use tf.compat.v1.Session() rather than just tf.Session()
with tf.compat.v1.Session() as sess:  
  print(mean.numpy())  # mean.numpy() runs this part of the graph

# No matter how many times we run, we should get the same output as probabilities are deterministic