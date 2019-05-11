# Readme de pruebas realizadas

- _tickets1.0.ipynb_ (1):
  - Prueba realizada.
  - Seguimos las instrucciones del ejemplo en el repositorio de [transformaciones 2D](https://github.com/albertoruiz/umucv/blob/28e7cf831c0f8388320cddec06e2aa1b691f53f2/notebooks/transf2D.ipynb) y la documentación listada en el notebook.
  - Logramos juntar dos fraciones de un tiquet que quedan en escala de grises sobre otra imagen nueva.
- _tickets1.2.ipynb_:
  - SIFT y SURF son algoritmos patentados que en un eventual caso no deberían usarse para una versión comercial del producto.
  - Comienzo una versión nueva probando ORB, que según quién, dicen que puede ser más rápido, y es de uso libre.
  - Paramos en drawMatches la estructura apenas saca puntos en común entre las dos imágenes. Los puntos clave son pésimos.
- _tickets1.3.ipynb_ (2):
  - Continuamos con este fichero, haciendo uso de nuevo de SIFT.
  - Modificamos el contrastThreshold (ver [documentacion](https://docs.opencv.org/3.4/d5/d3c/classcv_1_1xfeatures2d_1_1SIFT.html)) para que detecte una cantidad mucho menor de _keypoints_ y así podamos reducir el tiempo del _Matcher_
  - Tenemos que hacer los matches del que menos puntos le han salido con el que más `bf.knnMatch(descs2,descs,k=2)` por... [Parece ser que esto no es así]
- _tickets1.4.ipynb_:
  - En este conseguimos meter todo en un bucle, y almacenar las variables que necesitamos todas en listas.
  - las imágenes ya se solapan bien, y falta ver una manera de ir combinándolas todas. Quizá en el mismo bucle, quizá simpelemente hay una manera.
- _tickets1.5.ipynb_:
  - Comienzo de pruebas de preprocesamiento
  - Siguiendo [el siguiente tuto](https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/)

Pruebas post procesamiento.

- output1
```
# convert the warped image to grayscale
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    # sharpen image
    sharpen = cv2.GaussianBlur(gray, (0,0), 3)
    sharpen = cv2.addWeighted(gray, 1.5, sharpen, -0.5, 0)

    # apply adaptive threshold to get black and white effect
    thresh = cv2.adaptiveThreshold(sharpen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 15)
```
- output 2
```
# convert the warped image to grayscale
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    # sharpen image
    sharpen = cv2.GaussianBlur(gray, (0,0), 3)
    sharpen = cv2.addWeighted(gray, 2.5, sharpen, -0.5, 0)

    # apply adaptive threshold to get black and white effect
    thresh = cv2.adaptiveThreshold(sharpen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 15)
```

## 11/05/2019

- lineas-1.0.py: Lee una imagen, busca líneas, y divide la imagen en tantas líneas como encuentre. Pendiente de probar:
  1. threshold de altura que no divida la imágen en más trozos de los que debería. Es decir, que no pase trozos blancos, sino sólo aquellos de más de X.
  2. Threshold también para que las sub-imágenes muy altas, sean procesadas de nuevo a ver si es que hemos cortado 3 líneas juntas (esto pasa ya por ejemplo en el de mercadona)
  3. Colorear de blanco los fragmentos vacíos para mejorar la detección de líneas
  4. Experimentar con preprocesamiento de imagen (eliminación de ruido, blancos más blancos, negros más negros, etc)

- document-scanner: Fragmento prestado y modificado de un tuto. Escanea un documento a partir de una imagen. Se ha ajustado el código a nuestro caso (problemas de precisión, demasiadas asunciones para un caso real) Pendiente de probar/mejorar:
  1. Tickets torcidos
  2. Y si el ticket se sale de la pantalla?
  3. Si son varias fotografías? Integrar código previo de sticker (en notebooks).
