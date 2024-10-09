import os
import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
from keras.applications import MobileNetV2
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
import model_compression_toolkit as mct
from model_compression_toolkit.core import QuantizationErrorMethod

# Set up directories and constants
MODELS_DIR = 'models/'
if not os.path.exists(MODELS_DIR):
    os.mkdir(MODELS_DIR)

MODEL = MODELS_DIR + 'mobilenet-posture'
MODEL_KERAS = MODELS_DIR + 'mobilenet-quant-posture.keras'

BATCH_SIZE = 32
IMAGE_SHAPE = (224, 224)

def load_posture_dataset():
    (train_ds, validation_ds), info = tfds.load(
        name="posture",  # Replace with posture dataset
        split=["train", "test"],
        with_info=True,
        as_supervised=True,
        shuffle_files=True,
        batch_size=BATCH_SIZE
    )
    return train_ds, validation_ds, info

train_ds, validation_ds, info = load_posture_dataset()

class_names = ["slouched", "sitting_straight", "standing"]
num_classes = len(class_names)

def preprocess_data(image, label):
    image = tf.keras.applications.mobilenet_v2.preprocess_input(tf.cast(image, tf.float32))
    image = tf.image.resize(image, IMAGE_SHAPE)
    return image, label

train_ds = train_ds.map(preprocess_data)
validation_ds = validation_ds.map(preprocess_data)

# Data augmentation
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomRotation(0.2),
])

train_ds = train_ds.map(lambda x, y: (data_augmentation(x), y))
train_ds = train_ds.prefetch(tf.data.experimental.AUTOTUNE)
validation_ds = validation_ds.prefetch(tf.data.experimental.AUTOTUNE)

# Create and compile the model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=IMAGE_SHAPE+(3,))
x = base_model.output
x = GlobalAveragePooling2D()(x)
predictions = Dense(num_classes, activation=tf.nn.softmax)(x)
float_model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False

float_model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

# Train the model
EPOCHS = 20
callback = tf.keras.callbacks.EarlyStopping(
    monitor="val_accuracy",
    baseline=0.8,
    min_delta=0.01,
    mode='max',
    patience=5,
    verbose=1,
    restore_best_weights=True,
    start_from_epoch=5,
)

history = float_model.fit(
    train_ds,
    validation_data=validation_ds,
    epochs=EPOCHS,
    callbacks=[callback]
)

float_model.save(MODEL)

# Quantization
def get_representative_dataset():
    def representative_dataset():
        for _ in range(10):
            yield train_ds.take(1).get_single_element()[0].numpy()
    return representative_dataset

representative_dataset_gen = get_representative_dataset()

tpc = mct.get_target_platform_capabilities("tensorflow", 'imx500', target_platform_version='v1')

q_config = mct.core.QuantizationConfig(
    activation_error_method=QuantizationErrorMethod.MSE,
    weights_error_method=QuantizationErrorMethod.MSE,
    weights_bias_correction=True,
    shift_negative_activation_correction=True,
    z_threshold=16
)

ptq_config = mct.core.CoreConfig(quantization_config=q_config)

quantized_model, quantization_info = mct.ptq.keras_post_training_quantization(
    in_model=float_model,
    representative_data_gen=representative_dataset_gen,
    core_config=ptq_config,
    target_platform_capabilities=tpc
)

# Export the quantized model
mct.exporter.keras_export_model(model=quantized_model, save_model_path=MODEL_KERAS)

print(f"Quantized model saved to {MODEL_KERAS}")
