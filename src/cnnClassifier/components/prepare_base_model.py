from pathlib import Path
import tensorflow as tf
from cnnClassifier.entity import PrepareBaseModelConfig


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config


    def get_base_model(self):
        self.model = tf.keras.application.vgg16.VGG16(
            input_shape = self.config.params_image_size,
            weights = self.config.params_weights,
            include_top = self.config.params_include_top
        )  

        self.save_model(path=self.config.base_model_path, model=self.model)



    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, Learning_rate):
        if freeze_all:
            for layer in model.layers:
                model.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                model.trainable = False

        flatten_in = tf.keras.layers.flatten()(model.output)
        prediction = tf.keras.layers.Dense(
            units = classes,
            activation = "softmax"
        )(flatten_in)          


        full_model = tf.keras.models.Model(
            input = model.input,
            output = prediction
        )  

        full_model.compile(
            optimizer = tf.keras.optimizers.SGD(Learning_rate = Learning_rate),
            Loss = tf.keras.losses.CategoricalCrossentropy(),
            metrics = ["accuracy"]
        )        

        full_model.summary()
        return full_model



    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            model = self.model,
            classes = self.config.params_classes,
            freeze_all = True,
            freeze_till = None,
            Learning_rate = self.config.params_learning_rate
        )    

        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)


    @staticmethod
    def save_model(path:Path, model: tf.keras.Model):
        model.save(path)    