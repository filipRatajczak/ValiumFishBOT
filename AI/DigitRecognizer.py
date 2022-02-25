import numpy
import tensorflow
from keras import models, layers

from Screen.Screenshoter import load_image


def create_tuple_of_file_names(num_from, num_to):
    tuple_of_file_names = list()
    for num_of_file in range(num_from, num_to):
        tuple_of_file_names.append(f'screenshot{num_of_file}.bmp')
    return tuple_of_file_names


def parse_rgb_vector_to_tensor(vector_of_image):
    array = numpy.array(vector_of_image).reshape(80, 310, 3)
    return tensorflow.convert_to_tensor(array)


def create_nparray_of_all_tensors(tuple_of_filenames):
    nparray_of_all_tensors = list()
    for filename in tuple_of_filenames:
        pixel_vector = get_vector_of_image_rgb_pixels(filename)
        tensor = parse_rgb_vector_to_tensor(pixel_vector)
        nparray_of_all_tensors.append(tensor)
    return numpy.asarray(nparray_of_all_tensors)


def create_nparray_from_picture(image_path):
    pixel_vector = get_vector_of_image_rgb_pixels(image_path)
    tensor = parse_rgb_vector_to_tensor(pixel_vector)
    return numpy.asarray(list(tensor))


def parse_tuple_to_np_array(array):
    return numpy.asarray(array)


def get_vector_of_image_rgb_pixels(path):
    tuple_of_pixels = list()
    image = load_image(path)
    for x in range(image.width):
        for y in range(image.height):
            pixel_in_rgb = image.getpixel((x, y))
            tuple_of_pixels.append(pixel_in_rgb)
    return tuple_of_pixels


def create_cnn_model():
    model = models.Sequential()
    model.add(layers.Conv2D(320, 1, 1, activation='relu', input_shape=(80, 310, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(320, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(320, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(320, activation='relu'))
    model.add(layers.Dense(320, activation='relu'))
    model.summary()
    model.compile(optimizer='adam',
                  loss=tensorflow.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    train_file_names = create_tuple_of_file_names(0, 799)
    test_file_names = create_tuple_of_file_names(800, 916)
    train = create_nparray_of_all_tensors(train_file_names)
    validate = parse_tuple_to_np_array((1, 1, 4, 2, 3, 2, 1, 4, 5, 2, 4, 5, 3, 5, 2, 1, 1, 2, 2, 4, 5, 1, 1, 3, 1, 3, 5,
                                        5, 1, 5, 1, 3, 1, 3, 2, 3, 4, 4, 2, 2, 4, 3, 5, 2, 4, 4, 3, 5, 5, 2, 2, 3, 3, 4,
                                        4, 2, 1, 2, 3, 5, 2, 1, 4, 2, 1, 2, 2, 3, 5, 3, 5, 5, 1, 2, 3, 5, 1, 5, 2, 2, 5,
                                        4, 3, 1, 2, 2, 5, 1, 2, 4, 3, 1, 3, 4, 3, 1, 2, 3, 3, 1, 1, 4, 1, 4, 3, 2, 3, 5,
                                        1, 5, 4, 5, 3, 5, 3, 2, 2, 4, 2, 4, 4, 1, 2, 5, 3, 5, 5, 3, 2, 2, 4, 3, 5, 5, 5,
                                        5, 4, 3, 2, 5, 1, 4, 2, 3, 2, 3, 5, 4, 2, 1, 1, 4, 4, 1, 5, 2, 3, 1, 2, 5, 3, 3,
                                        4, 5, 1, 1, 5, 3, 5, 4, 2, 5, 3, 2, 2, 3, 1, 2, 1, 2, 3, 4, 1, 2, 5, 3, 3, 1, 2,
                                        1, 2, 2, 4, 1, 2, 2, 4, 2, 4, 1, 4, 5, 4, 2, 3, 3, 5, 2, 5, 4, 2, 1, 3, 3, 4, 3,
                                        2, 3, 5, 4, 5, 4, 5, 5, 4, 3, 1, 4, 5, 4, 1, 2, 4, 5, 3, 2, 1, 3, 1, 3, 2, 2, 5,
                                        1, 3, 3, 3, 2, 5, 5, 4, 3, 3, 2, 5, 2, 2, 4, 1, 4, 2, 4, 1, 4, 2, 4, 1, 3, 5, 5,
                                        3, 2, 4, 5, 5, 3, 2, 3, 5, 5, 2, 4, 1, 5, 2, 3, 4, 1, 1, 5, 2, 4, 2, 5, 2, 5, 1,
                                        1, 1, 1, 5, 2, 1, 3, 2, 2, 2, 3, 1, 2, 1, 5, 5, 4, 5, 4, 3, 5, 5, 1, 3, 5, 3, 1,
                                        5, 5, 2, 5, 2, 4, 4, 3, 5, 3, 2, 1, 1, 1, 3, 1, 5, 2, 2, 4, 2, 4, 3, 4, 1, 5, 2,
                                        3, 5, 1, 1, 5, 4, 5, 5, 1, 4, 4, 1, 5, 2, 5, 5, 1, 3, 2, 3, 3, 1, 1, 1, 3, 3, 5,
                                        2, 2, 2, 1, 5, 2, 1, 5, 4, 5, 5, 4, 4, 2, 2, 2, 3, 4, 5, 3, 4, 4, 5, 4, 5, 1, 3,
                                        1, 4, 4, 4, 3, 1, 5, 5, 4, 4, 1, 3, 1, 5, 5, 3, 1, 3, 1, 5, 5, 4, 4, 4, 2, 3, 1,
                                        3, 5, 4, 4, 3, 3, 4, 2, 1, 4, 4, 1, 4, 3, 2, 4, 5, 5, 3, 2, 3, 4, 4, 5, 3, 2, 3,
                                        2, 5, 4, 2, 2, 4, 4, 3, 3, 2, 3, 5, 1, 5, 1, 1, 3, 2, 3, 5, 5, 2, 5, 5, 1, 3, 5,
                                        4, 5, 4, 4, 4, 5, 1, 5, 4, 4, 3, 1, 1, 5, 1, 1, 2, 2, 4, 4, 3, 4, 4, 3, 3, 3, 1,
                                        5, 1, 2, 1, 2, 4, 4, 2, 2, 2, 2, 4, 5, 3, 4, 4, 3, 4, 3, 4, 2, 2, 1, 4, 5, 5, 1,
                                        5, 3, 4, 5, 4, 3, 3, 2, 4, 1, 1, 3, 2, 1, 1, 5, 5, 1, 3, 1, 2, 2, 1, 4, 4, 2, 4,
                                        1, 4, 2, 3, 2, 2, 2, 2, 3, 3, 5, 1, 4, 1, 4, 3, 2, 3, 4, 1, 2, 2, 5, 5, 1, 1, 1,
                                        2, 3, 1, 2, 5, 2, 3, 5, 3, 4, 1, 4, 1, 4, 4, 1, 3, 5, 3, 3, 1, 2, 1, 4, 3, 3, 1,
                                        2, 2, 4, 1, 2, 4, 3, 3, 3, 2, 3, 4, 4, 5, 5, 2, 4, 3, 5, 2, 4, 3, 4, 3, 5, 2, 5,
                                        4, 2, 4, 5, 5, 2, 3, 2, 1, 1, 5, 1, 3, 3, 5, 2, 1, 5, 5, 2, 5, 4, 2, 5, 3, 1, 4,
                                        4, 2, 1, 4, 1, 1, 1, 4, 4, 3, 4, 1, 4, 2, 2, 1, 2, 1, 4, 5, 5, 4, 5, 3, 2, 5, 5,
                                        2, 4, 5, 1, 3, 3, 1, 3, 2, 5, 2, 3, 3, 3, 2, 1, 5, 2, 1, 5, 3, 4, 2, 1, 3, 2, 3,
                                        3, 1, 5, 1, 1, 4, 2, 3, 4, 4, 4, 5, 1, 2, 3, 5, 5, 2, 3, 1, 5, 3, 4, 1, 1, 4, 3,
                                        2, 5, 4, 1, 3, 2, 4, 2, 5, 1, 4, 3, 3, 4, 5, 2, 1, 3, 4, 5, 3, 3, 4, 2, 5, 4, 1,
                                        4, 4, 3, 2, 4, 4, 4, 2, 5, 2, 4, 1, 2, 3, 4, 4))
    test_data = create_nparray_of_all_tensors(test_file_names)
    test_validate = parse_tuple_to_np_array((2, 4, 3, 5, 2, 1, 2, 2, 1, 2, 1, 1, 2, 3, 3, 5, 4, 4, 1, 2, 4, 5, 5, 3, 4,
                                             1, 3, 1, 1, 1, 1, 4, 5, 4, 5, 1, 4, 3, 2, 4, 5, 3, 1, 1, 5, 4, 1, 4, 5, 1,
                                             1, 4, 1, 2, 3, 2, 3, 3, 4, 5, 5, 3, 4, 3, 3, 3, 4, 5, 2, 4, 1, 4, 1, 1, 4,
                                             3, 3, 5, 5, 4, 3, 1, 3, 4, 2, 1, 5, 4, 5, 3, 3, 4, 1, 5, 1, 2, 5, 4, 5, 1,
                                             1, 4, 2, 2, 4, 1, 1, 3, 4, 2, 4, 3, 2, 5, 1, 2))
    model.fit(train, validate, epochs=50, validation_data=(test_data, test_validate))
    return model


def predict_single_input(single_input, model):
    single_input = tensorflow.reshape(single_input, (1, 80, 310, 3))
    prediction = model.predict(single_input)
    classes = numpy.argmax(prediction, axis=1)
    return classes.data[0]


def get_number_from_model(screenshot_path, model):
    data = create_nparray_from_picture(screenshot_path)
    num_of_spaces_to_click = predict_single_input(data, model)
    return num_of_spaces_to_click
