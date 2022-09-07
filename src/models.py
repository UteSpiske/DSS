from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, BatchNormalization, Dropout,\
    Activation, Concatenate, Conv1D, MaxPool1D, GlobalAveragePooling1D, Reshape,\
    Conv2D, LSTM, Masking, Normalization
from .layers import transformer_encoder


def get_model(ret):
    nb_classes = 20
    class_names = ['accel_x', 'accel_y', 'accel_z']  # , 'time_event', 'time_millis', 'time_nanos']
    if ret.arch == "rnn":
        inputs = Input(shape=(50, 3))

        x = Masking(mask_value=0.0, input_shape=(50, 3))(inputs)
        # x = Normalization(axis=-1, mean=None, variance=None)(x)  # @TODO: Vector of nb_features for mean and variance
        x = LSTM(32)(x)
        x = Dropout(rate=0.5)(x)
        x = Dense(32)(x)
        x = Activation("relu")(x)
        x = Dense(nb_classes, activation="softmax")(x)  # @TODO: Y U NO SOFTMAX?
        return Model(inputs=inputs, outputs=x)

    elif ret.arch == "transformer":
        inputs = Input(shape=(50, 3))
        x = inputs
        for _ in range(4):
            x = transformer_encoder(x, head_size=256, num_heads=4, ff_dim=4, dropout=0)

        x = GlobalAveragePooling1D(data_format="channels_first")(x)
        for dim in [128]:
            x = Dense(dim, activation="relu")(x)
            x = Dropout(0.4)(x)
        outputs = Dense(nb_classes, activation="softmax")(x)
        return Model(inputs, outputs)

    else:
        raise ValueError("Unknown architecture provided:", ret.arch)