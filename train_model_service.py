# train_model_service.py

from flask import Flask, request, jsonify
import tensorflow as tf
import os

app = Flask(__name__)

# Load dataset (adjust paths as needed)
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "data/train", image_size=(180, 180), batch_size=32
)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "data/val", image_size=(180, 180), batch_size=32
)

# Prefetch for performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Get number of classes
class_names = train_ds.class_names
num_classes = len(class_names)

# Default model builder
def build_model(num_classes):
    model = tf.keras.Sequential([
        tf.keras.layers.Rescaling(1./255, input_shape=(180, 180, 3)),
        tf.keras.layers.Conv2D(16, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes)
    ])
    return model

@app.route('/api/train-model', methods=['POST'])
def train_model():
    try:
        # Read training options
        data = request.get_json()
        epochs = int(data.get("epochs", 10))
        batch_size = int(data.get("batch_size", 32))

        # Build and compile model
        model = build_model(num_classes)
        model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )

        # Train the model
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )

        # Get final accuracy and loss
        final_acc = history.history['val_accuracy'][-1]
        final_loss = history.history['val_loss'][-1]

        # Save model
        model.save("saved_model/classifier_model")

        return jsonify({
            "message": "Model trained successfully",
            "epochs": epochs,
            "val_accuracy": round(float(final_acc), 4),
            "val_loss": round(float(final_loss), 4),
            "model_path": "saved_model/classifier_model"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
