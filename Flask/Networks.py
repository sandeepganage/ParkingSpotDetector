import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import *
import tensorflow.keras.backend as K
K.set_image_data_format('channels_first')

# --------------------------------------------------------------------------------
global flag
flag = False


def UNET_inception_ResNet_TooSmallSize_Modified(width, height, depth, classes, weightsPath=None):
    global flag

    data_shape = width * height
    input_shape = (depth, height, width)
    input_img = Input(shape=input_shape)


    x = ZeroPadding2D((3, 3), input_shape=(depth, height, width))(input_img)
    '''
    Add step-2, number of layer 6, size (128,128)
    '''
    x = Conv2D(16, (7, 7), strides=(2, 2), padding='valid', activation='relu', kernel_initializer='he_normal')(x)
    x_1 = BatchNormalization(axis=1)(x, training=flag)
    # x = Activation('relu')(x)
    x_2 = MaxPooling2D((2, 2), strides=(2, 2))(x_1)  # First Pooling Layer (Pool1)##

    conv1_1 = Conv2D(16, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(x_2)

    conv1_1 = BatchNormalization(axis=1)(conv1_1, training=flag)
    conv1_2 = Conv2D(16, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(x_2)
    conv1_2 = BatchNormalization(axis=1)(conv1_2, training=flag)
    # conv1_3 = Conv2D(32, (3,3), padding= 'same', activation='relu', kernel_initializer = 'he_normal')(inputs)
    conv1_3 = Conv2D(16, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv1_2)
    conv1_3 = BatchNormalization(axis=1)(conv1_3, training=flag)
    conv1 = concatenate([conv1_1, conv1_2, conv1_3, x_2], axis=1)
    conv1 = Conv2D(16, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv1)
    conv1 = BatchNormalization(axis=1)(conv1, training=flag)
#    conv1 = Dropout(rate=0.1)(conv1)
    pool1 = MaxPooling2D((2, 2))(conv1)

    '''
    mark end of step-3, number of layer =20, size (64,64)
    '''

    conv1_1 = Conv2D(64, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(pool1)
    conv1_1 = BatchNormalization(axis=1)(conv1_1, training=flag)
    conv1_2 = Conv2D(64, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(pool1)
    conv1_2 = BatchNormalization(axis=1)(conv1_2, training=flag)
    # conv1_3 = Conv2D(64, (3,3), padding= 'same', activation='relu', kernel_initializer = 'he_normal')(pool1)
    conv1_3 = Conv2D(64, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv1_2)
    conv1_3 = BatchNormalization(axis=1)(conv1_3, training=flag)
    conv2 = concatenate([conv1_1, conv1_2, conv1_3, pool1], axis=1)
    conv2 = Conv2D(64, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv2)
    conv2 = BatchNormalization(axis=1)(conv2, training=flag)
#    conv2 = Dropout(rate=0.1)(conv2)
    pool2 = MaxPooling2D((2, 2))(conv2)

    '''        ## mark end of step-4, number of layer =20, size (32,32)

    '''

    conv1_1 = Conv2D(128, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(pool2)
    conv1_1 = BatchNormalization(axis=1)(conv1_1, training=flag)
    conv1_2 = Conv2D(128, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(pool2)
    conv1_2 = BatchNormalization(axis=1)(conv1_2, training=flag)
    # conv1_3 = Conv2D(128, (3,3), padding= 'same', activation='relu', kernel_initializer = 'he_normal')(pool2)
    conv1_3 = Conv2D(128, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv1_2)
    conv1_3 = BatchNormalization(axis=1)(conv1_3, training=flag)
    conv3 = concatenate([conv1_1, conv1_2, conv1_3, pool2], axis=1)
    conv3 = Conv2D(128, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv3)
    conv3 = BatchNormalization(axis=1)(conv3, training=flag)
#    conv3 = Dropout(rate=0.1)(conv3)
    pool3 = MaxPooling2D((2, 2))(conv3)

    '''         ## mark end of step-5, number of layer =48, size (16,16)
    '''

    conv4 = Conv2D(128, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(pool3)
    conv4 = BatchNormalization(axis=1)(conv4, training=flag)
    conv4 = Conv2D(128, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv4)
    conv4 = BatchNormalization(axis=1)(conv4, training=flag)

    '''         ## mark end of step-6, number of layer =48, size (16,16)
    '''

    up_samp2 = concatenate([Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(conv4), conv3], axis=1)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(up_samp2)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv7)
    conv7 = concatenate([conv7, up_samp2], axis=1)
    conv7 = Conv2D(128, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(conv7)
    conv7 = BatchNormalization(axis=1)(conv7, training=flag)

    '''         ## mark end of step-7, number of layer =64, size (32,32)
    '''

    up_samp3 = concatenate([Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(conv7), conv2], axis=1)
    conv8 = Conv2D(64, (3, 3), activation='relu',padding='same', kernel_initializer='he_normal')(up_samp3)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv8)
    conv8 = concatenate([conv8, up_samp3], axis=1)
    conv8 = Conv2D(64, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(conv8)
    conv8 = BatchNormalization(axis=1)(conv8, training=flag)

    '''         ## mark end of step-8, number of layer =64, size (64,64)
    '''

    up_samp4 = concatenate([Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(conv8), conv1], axis=1)
    conv9 = Conv2D(16, (3, 3), activation='relu',padding='same', kernel_initializer='he_normal')(up_samp4)
    conv9 = Conv2D(16, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
    conv9 = concatenate([conv9, up_samp4], axis=1)
    conv9 = Conv2D(16, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(conv9)
    conv9 = BatchNormalization(axis=1)(conv9, training=flag)

    '''         ## mark end of step-9, number of layer =84, size (128,128)
    '''

    # vb= Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(conv9)
    up_samp5 = concatenate([Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(conv9), x_1], axis=1)
    conv9 = Conv2D(16, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(up_samp5)
    conv9 = Conv2D(16, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
    conv9 = concatenate([conv9, up_samp5], axis=1)
    conv9 = Conv2D(16, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(conv9)
    conv9 = BatchNormalization(axis=1)(conv9, training=flag)

    '''         ## mark end of step-10, number of layer =94, size (256,256)
    '''
    up_samp6 = UpSampling2D(size=(2, 2))(conv9)
    # up_samp6 = concatenate([Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(conv9),x], axis=1)
    conv9 = Conv2D(16, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(up_samp6)
    conv9 = Conv2D(16, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
    conv9 = concatenate([conv9, up_samp6], axis=1)
    conv9 = Conv2D(16, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(conv9)
    conv9 = BatchNormalization(axis=1)(conv9, training=flag)

    '''         ## mark end of step-11, number of layer =103, size (512,512)
    '''
    conv10 = Conv2D(classes, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
    # conv10 = Conv2D(classes, (3, 3), padding='same')(conv9)
    reshape = Reshape((classes, data_shape), input_shape=(classes, height, width))(conv10)
    # reshape = Reshape((classes, data_shape), input_shape=(height, width,classes))(conv10)

    permut = Permute((2, 1))(reshape)
    softmax = Activation('softmax', dtype="float32")(permut)
    model = keras.Model(inputs=[input_img], outputs=[softmax])

    if weightsPath is not None:
        model.load_weights(weightsPath)
        print("pre-trained weights loaded successfully")
    return model


def UNET_inception_ResNet_TooSmallSize(width, height, depth, classes, weightsPath=None):
    data_shape = height * width
    inputs = Input((depth, width, height))
    conv1_1 = Conv2D(
        16, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(inputs)
    conv1_1 = BatchNormalization(axis=1)(conv1_1)
    conv1_2 = Conv2D(
        16, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(inputs)
    conv1_2 = BatchNormalization(axis=1)(conv1_2)
    # conv1_3 = Conv2D(32, (3,3), padding= 'same', activation='relu', kernel_initializer = 'he_normal')(inputs)
    conv1_3 = Conv2D(
        16, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv1_2)
    conv1_3 = BatchNormalization(axis=1)(conv1_3)
    conv1 = concatenate(
        [conv1_1, conv1_2, conv1_3, inputs], axis=1)
    conv1 = Conv2D(
        16, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv1)
    conv1 = BatchNormalization(axis=1)(conv1)
    conv1 = Dropout(rate=0.1)(conv1)
    pool1 = MaxPooling2D((2, 2))(conv1)

    conv1_1 = Conv2D(
        64, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(pool1)
    conv1_1 = BatchNormalization(axis=1)(conv1_1)
    conv1_2 = Conv2D(
        64, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(pool1)
    conv1_2 = BatchNormalization(axis=1)(conv1_2)
    # conv1_3 = Conv2D(64, (3,3), padding= 'same', activation='relu', kernel_initializer = 'he_normal')(pool1)
    conv1_3 = Conv2D(
        64, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv1_2)
    conv1_3 = BatchNormalization(axis=1)(conv1_3)
    conv2 = concatenate(
        [conv1_1, conv1_2, conv1_3, pool1], axis=1)
    conv2 = Conv2D(
        64, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv2)
    conv2 = BatchNormalization(axis=1)(conv2)
    conv2 = Dropout(rate=0.1)(conv2)
    pool2 = MaxPooling2D((2, 2))(conv2)

    conv1_1 = Conv2D(
        128, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(pool2)
    conv1_1 = BatchNormalization(axis=1)(conv1_1)
    conv1_2 = Conv2D(
        128, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(pool2)
    conv1_2 = BatchNormalization(axis=1)(conv1_2)
    # conv1_3 = Conv2D(128, (3,3), padding= 'same', activation='relu', kernel_initializer = 'he_normal')(pool2)
    conv1_3 = Conv2D(
        128, (3, 3), padding='same', activation='relu', kernel_initializer='he_normal')(conv1_2)
    conv1_3 = BatchNormalization(axis=1)(conv1_3)
    conv3 = concatenate(
        [conv1_1, conv1_2, conv1_3, pool2], axis=1)
    conv3 = Conv2D(128, (3, 3), padding='same',
                                activation='relu', kernel_initializer='he_normal')(conv3)
    conv3 = BatchNormalization(axis=1)(conv3)
    conv3 = Dropout(rate=0.1)(conv3)
    pool3 = MaxPooling2D((2, 2))(conv3)

    conv4 = Conv2D(128, (3, 3), padding='same',
                                activation='relu', kernel_initializer='he_normal')(pool3)
    conv4 = BatchNormalization(axis=1)(conv4)
    conv4 = Conv2D(128, (3, 3), padding='same',
                                activation='relu', kernel_initializer='he_normal')(conv4)
    conv4 = BatchNormalization(axis=1)(conv4)

    up_samp2 = concatenate([Conv2DTranspose(
        128, (2, 2), strides=(2, 2), padding='same')(conv4), conv3], axis=1)
    conv7 = Conv2D(128, (3, 3), activation='relu',
                                padding='same', kernel_initializer='he_normal')(up_samp2)
    conv7 = Conv2D(
        128, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv7)
    conv7 = concatenate([conv7, up_samp2], axis=1)
    conv7 = Conv2D(128, (1, 1), padding='same',
                                activation='relu', kernel_initializer='he_normal')(conv7)
    conv7 = BatchNormalization(axis=1)(conv7)

    up_samp3 = concatenate([Conv2DTranspose(
        64, (2, 2), strides=(2, 2), padding='same')(conv7), conv2], axis=1)
    conv8 = Conv2D(64, (3, 3), activation='relu',
                                padding='same', kernel_initializer='he_normal')(up_samp3)
    conv8 = Conv2D(
        64, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv8)
    conv8 = concatenate([conv8, up_samp3], axis=1)
    conv8 = Conv2D(
        64, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(conv8)
    conv8 = BatchNormalization(axis=1)(conv8)

    up_samp4 = concatenate([Conv2DTranspose(
        16, (2, 2), strides=(2, 2), padding='same')(conv8), conv1], axis=1)
    conv9 = Conv2D(16, (3, 3), activation='relu',
                                padding='same', kernel_initializer='he_normal')(up_samp4)
    conv9 = Conv2D(
        16, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
    conv9 = concatenate([conv9, up_samp4], axis=1)
    conv9 = Conv2D(
        16, (1, 1), padding='same', activation='relu', kernel_initializer='he_normal')(conv9)
    conv9 = BatchNormalization(axis=1)(conv9)

    conv10 = Conv2D(
        classes, (3, 3), activation='relu', padding='same', kernel_initializer='he_normal')(conv9)
    # conv10 = Conv2D(classes, (3, 3), padding='same')(conv9)
    reshape = Reshape(
        (classes, data_shape), input_shape=(classes, height, width))(conv10)
    # reshape = Reshape((classes, data_shape), input_shape=(height, width,classes))(conv10)

    permut = Permute((2, 1))(reshape)
    softmax = Activation('softmax')(permut)
    model = keras.Model(inputs=[inputs], outputs=[softmax])

    if weightsPath is not None:
        model.load_weights(weightsPath)
    return model