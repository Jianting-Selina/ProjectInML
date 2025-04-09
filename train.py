# train.py

import os
import random
import shutil
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras
import mlflow
import mlflow.tensorflow
from kagglehub import dataset_download

from dotenv import load_dotenv
import ast
load_dotenv()

# === Global Config ===
# BATCH_SIZE = 32
# IMAGE_SIZE = (128, 128)
# EPOCHS = 5
# EPOCHS=os.getenv('EPOCHS')

# BATCH_SIZE=os.getenv('BATCH_SIZE')

# IMAGE_SIZE=os.getenv('IMAGE_SIZE')
IMAGE_SIZE = ast.literal_eval(os.getenv('IMAGE_SIZE'))
BATCH_SIZE = int(os.getenv('BATCH_SIZE'))
EPOCHS = int(os.getenv('EPOCHS'))

AUTOTUNE = tf.data.AUTOTUNE

# === Step 1: Download + Prepare Data ===
print("🔽 Downloading dataset...")
dataset_dir = dataset_download("tombackert/brain-tumor-mri-data")
print("✅ Dataset downloaded to:", dataset_dir)

# Dataset folders
dataset_path = os.path.join(dataset_dir, "brain-tumor-mri-dataset")
train_path = os.path.join(dataset_dir, "train")
val_path = os.path.join(dataset_dir, "val")
test_path = os.path.join(dataset_dir, "test")

# Create folders
os.makedirs(train_path, exist_ok=True)
os.makedirs(val_path, exist_ok=True)
os.makedirs(test_path, exist_ok=True)

train_ratio = 0.7
val_ratio = 0.1
test_ratio = 0.2
assert train_ratio + val_ratio + test_ratio == 1.0

# Split images
for category in os.listdir(dataset_path):
    category_path = os.path.join(dataset_path, category)
    if not os.path.isdir(category_path): continue

    train_cat = os.path.join(train_path, category)
    val_cat = os.path.join(val_path, category)
    test_cat = os.path.join(test_path, category)
    os.makedirs(train_cat, exist_ok=True)
    os.makedirs(val_cat, exist_ok=True)
    os.makedirs(test_cat, exist_ok=True)

    images = os.listdir(category_path)
    random.shuffle(images)

    train_val_images = images[:int(len(images) * (train_ratio + val_ratio))]
    test_images = images[int(len(images) * (train_ratio + val_ratio)):]

    train_images = train_val_images[:int(len(train_val_images) * (train_ratio / (train_ratio + val_ratio)))]
    val_images = train_val_images[int(len(train_val_images) * (train_ratio / (train_ratio + val_ratio))):]

    for img in train_images:
        shutil.copy(os.path.join(category_path, img), os.path.join(train_cat, img))
    for img in val_images:
        shutil.copy(os.path.join(category_path, img), os.path.join(val_cat, img))
    for img in test_images:
        shutil.copy(os.path.join(category_path, img), os.path.join(test_cat, img))

print("✅ Data prepared into train, val, test sets.")

# === Step 2: Load Datasets ===
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_path,
    labels='inferred',
    label_mode='int',
    batch_size=BATCH_SIZE,
    image_size=IMAGE_SIZE,
    shuffle=True
)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    val_path,
    labels='inferred',
    label_mode='int',
    batch_size=BATCH_SIZE,
    image_size=IMAGE_SIZE,
    shuffle=True
)
test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    test_path,
    labels='inferred',
    label_mode='int',
    batch_size=BATCH_SIZE,
    image_size=IMAGE_SIZE,
    shuffle=True
)



# === Step 3: Model Definition ===
num_classes = len(train_ds.class_names)
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

model = tf.keras.Sequential([
    layers.Input(shape=(*IMAGE_SIZE, 3)),
    layers.Rescaling(1./255),
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# === Step 4: MLflow Tracking ===
#mlflow.set_experiment("Brain Tumor Classification")

#with mlflow.start_run(nested=True):
mlflow.log_param("batch_size", BATCH_SIZE)
mlflow.log_param("epochs", EPOCHS)
mlflow.log_param("image_size", IMAGE_SIZE)

    # ModelCheckpoint
checkpoint_cb = keras.callbacks.ModelCheckpoint(
    filepath="./training/samplecnn_mlflow.h5",
    save_best_only=True,
    monitor="val_loss",
    save_weights_only=False
)

print("🚀 Starting training...")
history = model.fit(
    train_ds,
    epochs=EPOCHS,
    validation_data=val_ds,
    callbacks=[checkpoint_cb]
)

print("✅ Training complete!")

# Evaluate on test set
loss, acc = model.evaluate(test_ds)
print(f"Test Accuracy: {acc:.4f}")

# Log metrics
mlflow.log_metric("test_accuracy", acc)
mlflow.log_metric("test_loss", loss)

# Log full model
mlflow.tensorflow.log_model(model, "model")

print("📦 Model & metrics logged to MLflow.")

