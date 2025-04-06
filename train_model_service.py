from flask import Flask, request, jsonify
import tensorflow as tf
import os

app = Flask(__name__)

AUTOTUNE = tf.data.AUTOTUNE

# Default model builder
def build_model(image_size, num_classes):
    return tf.keras.Sequential([
        tf.keras.layers.Rescaling(1./255, input_shape=(*image_size, 3)),
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

@app.route('/api/train-model', methods=['POST'])
def train_model():
    try:
        data = request.get_json()

        # 
        epochs = int(data.get("epochs", 15))
        batch_size = int(data.get("batch_size", 16))
        image_size = tuple(data.get("image_size", [128, 128]))
        model_path = data.get("model_path", "training/")

        # data
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            "data/train", image_size=image_size, batch_size=batch_size
        )
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            "data/val", image_size=image_size, batch_size=batch_size
        )

        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        num_classes = len(train_ds.class_names)

        # build 
        model = build_model(image_size, num_classes)
        model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )

        # train
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )

        final_acc = history.history['val_accuracy'][-1]
        final_loss = history.history['val_loss'][-1]

        # save model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model.save(model_path)

        return jsonify({
            "message": "Model trained successfully",
            "epochs": epochs,
            "val_accuracy": round(float(final_acc), 4),
            "val_loss": round(float(final_loss), 4),
            "model_path": model_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
