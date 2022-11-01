def representative_dataset():
  for data in dataset:
    yield {
      "image": data.image,
      "bias": data.bias,
    }


saved_model_dir = './output/saved_model'
import tensorflow as tf
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8  # or tf.uint8
converter.inference_output_type = tf.int8  # or tf.uint8
tflite_quant_model = converter.convert()

# Save the model.
with open('./output/saved_model.tflite', 'wb') as f:
  f.write(tflite_quant_model)

  