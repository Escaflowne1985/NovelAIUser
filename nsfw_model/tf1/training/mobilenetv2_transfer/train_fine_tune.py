import os
from keras.preprocessing.image import ImageDataGenerator
from keras.backend import clear_session
from keras.optimizers import SGD
from pathlib import Path
from keras.models import Sequential, Model, load_model

# reusable stuff
import constants
import callbacks
import generators

# No kruft plz
clear_session()
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
sess = tf.Session(config=config)
set_session(sess)  # set this TensorFlow session as the default session for Keras

# Config
height = constants.SIZES['basic']
width = height
weights_file = "weights.best_mobilenet" + str(height) + ".hdf5"

print ('Starting from last full model run')
model = load_model("nsfwnsfw_mobilenet2." + str(width) + "x" + str(height) + ".h5")

# Unlock a few layers deep in Mobilenet v2
model.trainable = False
set_trainable = False
for layer in model.layers:
    if layer.name == 'block_11_expand':
        set_trainable = True
    if set_trainable:
        layer.trainable = True
    else:
        layer.trainable = False

# Let's see it
print('Summary')
print(model.summary())

# Load checkpoint if one is found
if os.path.exists(weights_file):
        print ("loading ", weights_file)
        model.load_weights(weights_file)

# Get all model callbacks
callbacks_list = callbacks.make_callbacks(weights_file)

print('Compile model')
opt = SGD(momentum=.9)
model.compile(
    loss='categorical_crossentropy',
    optimizer=opt,
    metrics=['accuracy']
)

# Get training/validation data via generators
train_generator, validation_generator = generators.create_generators(height, width)

print('Start training!')
history = model.fit_generator(
    train_generator,
    callbacks=callbacks_list,
    epochs=constants.TOTAL_EPOCHS,
    steps_per_epoch=constants.STEPS_PER_EPOCH,
    shuffle=True,
    workers=4,
    use_multiprocessing=False,
    validation_data=validation_generator,
    validation_steps=constants.VALIDATION_STEPS
)

# Save it for later
print('Saving Model')
model.save("nsfwnsfw_mobilenet2." + str(width) + "x" + str(height) + ".h5")
