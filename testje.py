import tensorflow as tf

# Check TensorFlow version
print("TensorFlow version:", tf.__version__)

# List available GPUs
gpus = tf.config.list_physical_devices('GPU')
print(gpus)
