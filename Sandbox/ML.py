import tensorflow as tf
import numpy as np
import pandas as pd 

#bankAdditional = pd.read_csv("https://raw.githubusercontent.com/reddyprasade/Machine-Learning-Problems-DataSets/refs/heads/master/Classification/Bank%20additional%20full.csv")




#(X , y), (Test_X , Test_y ) = 

tf.random.set_seed(1337)


model_1 = tf.keras.Sequential({
    tf.keras.layers.Dense(64, "relu"),
    tf.keras.layers.Dense(16),
    tf.keras.layers.Dense(4),
    tf.keras.layers.Dense(1, "softmax")
})

model_1.compile(loss = tf.keras.losses.LogCosh,
                optimizer = tf.keras.optimizers.Adam(.005),
                metrics = ["accuracy"])

#model_1.fit(X, y , epochs = 100)


model_1.summary()


def compound(principal, interest, time):
    return principal*(1+interest)^time\


print(compound(5000.0, 0.05, 31.0))