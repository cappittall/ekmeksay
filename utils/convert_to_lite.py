#
#
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model("./output/saved_model")
converter.target_spec.supported_ops = [
    #tf.lite.OpsSet.TFLITE_BUILTINS,  # enable TensorFlow Lite ops.
    tf.lite.OpsSet.SELECT_TF_OPS, # enable TensorFlow ops.
    tf.lite.OpsSet.TFLITE_BUILTINS
]
converter.experimental_enable_resource_variables = True

tflite_model = converter.convert()
open("./output/converted_model.tflite", "wb").write(tflite_model)