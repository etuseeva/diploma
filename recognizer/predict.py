﻿import tensorflow as tf
import numpy as np
import os
import glob
import cv2
import sys
import argparse

from utility.image import read_image
from models.params import Params

def predict(x_batch, params):
    session = tf.Session()

    # ВОССТАНОВЛЕНИЕ МОДЕЛИ
    # ----------
    # Загружаем/восстанавливаем сохраненную обученную модель
    saver = tf.train.import_meta_graph(
        params.base_params.model_dir + params.base_params.model_name + '.meta'
    )
    saver.restore(session, tf.train.latest_checkpoint(params.base_params.model_dir))

    graph = tf.get_default_graph()

    # Отвечает за предсказание сети
    y_pred = graph.get_tensor_by_name("y_pred:0")

    # Передаем данные сети на вход
    x = graph.get_tensor_by_name("x:0")
    y = graph.get_tensor_by_name("y:0")

    # Узнаем сколько/каких классов нужно нам распознать
    classes = os.listdir(params.base_params.train_path)

    y_test_images = np.zeros((1, len(classes)))

    # ПРЕДСКАЗАНИЕ
    # ----------
    feed_dict_test = {x: x_batch, y: y_test_images}
    result = session.run(y_pred, feed_dict=feed_dict_test)

    # Возвращаем какой класс и какая вертоятность что это он
    return classes[np.argmax(result)], np.amax(result) * 100


def console_prediction():
    # Инициализируем наши параметры 
    params = Params()

    # ПОДГОТОВКА ВХОДНЫХ ДАННЫХ
    # ----------
    # Получаем данные о местоположении файла
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = sys.argv[1]
    file_name = dir_path + '/' + image_path

    # Считываем изображение, которое необходимо распознать
    # Ввиду того, что вход НС имеет вид [None, image_height, image_width, num_channels]
    # мы преобразуем наши данные к нужной форме
    images = [read_image(file_name, params.base_params.image_size)]
    images = np.array(images, dtype=np.uint8)
    x_batch = images.reshape(
        1,
        params.base_params.image_height,
        params.base_params.image_width,
        params.base_params.num_channels
    )

    cls, probability = predict(x_batch, params)
    print('Это {0} на {1}%'.format(cls, probability))


def web_prediction(image_url):
    print('web_prediction = ' + image_url)
    # Распознавание данных переданных по сети
    # @todo считать и преобразовать данные, которые скачаны из сети


if __name__ == '__main__':
    console_prediction()