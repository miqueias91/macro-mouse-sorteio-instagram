from cv2 import cv2
from os import listdir
from random import randint
from random import random
import pyscreenshot as ImageGrab
import numpy as np
import pyautogui
import time
import mss

use_click_and_drag_instead_of_scroll = False
scroll_size = 60
click_and_drag_amount = 200
commom = 0.8
default = 0.7
scroll_attemps = 3


def main():
      # pyautogui.alert('Screenshot feito com sucesso.')
    global images
    images = carregarImagens()

    global imagem_tela_principal
    imagem_tela_principal = carregarImagensPrincipais()

    atualizarAlvo()


def carregarImagens(dir_path='./targets/'):
    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[removerSufixo(file, '.png')] = cv2.imread(path)

    return targets


def removerSufixo(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def carregarImagensPrincipais():
    file_names = listdir('./screenshot')
    heroes = []
    for file in file_names:
        path = './screenshot/' + file
        heroes.append(cv2.imread(path))

    return heroes


def atualizarAlvo():
    irNoAlvo()

def irNoAlvo():
    texto = '@joao.m1990'
    if clickBtn(images['caixa_texto']):
        inserirTexto(texto)

    time.sleep(1)
    clickBtn(images['botao_publicar_preenchido'])
    time.sleep(randint(1, 3))


def clickBtn(img, timeout=3, threshold= default):
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(img, threshold=threshold)

        if(len(matches) == 0):
            has_timed_out = time.time()-start > timeout
            continue

        x, y, w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x, pos_click_y, 1)
        pyautogui.click()
        return True

    return False


def positions(target, threshold=0.7, img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def moveToWithRandomness(x, y, t):
    pyautogui.moveTo(addRandomness(x, 10), addRandomness(y,10),t+random()/2)


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:, :, :3]


def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    return int(randomized_n)


def inserirTexto(texto):
    pyautogui.write(texto, interval=0.50)


def scroll():
    commoms = positions(images['barra_lateral'], threshold=commom)
    if (len(commoms) == 0):
        return
    x, y, w,h = commoms[len(commoms)-1]
    moveToWithRandomness((x), y, 1)

    if not use_click_and_drag_instead_of_scroll:
        pyautogui.scroll(-scroll_size)
    else:
        pyautogui.dragRel(0, -click_and_drag_amount, duration=1, button='left')


if __name__ == '__main__':
    main()
