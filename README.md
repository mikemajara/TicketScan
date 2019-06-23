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
  1. threshold de altura que no divida la imágen en más trozos de los que debería. Es decir, que no pase trozos blancos,
   sino sólo aquellos de más de X.
  2. Threshold también para que las sub-imágenes muy altas, sean procesadas de nuevo a ver si es que hemos cortado 3 
  líneas juntas (esto pasa ya por ejemplo en el de mercadona)
  3. Colorear de blanco los fragmentos vacíos para mejorar la detección de líneas
  4. Experimentar con preprocesamiento de imagen (eliminación de ruido, blancos más blancos, negros más negros, etc)

- document-scanner: Fragmento prestado y modificado de un tuto. Escanea un documento a partir de una imagen. Se ha 
ajustado el código a nuestro caso (problemas de precisión, demasiadas asunciones para un caso real) Pendiente de 
probar/mejorar:
  1. Tickets torcidos
  2. Y si el ticket se sale de la pantalla?
  3. Si son varias fotografías? Integrar código previo de sticker (en notebooks).

## 19/05/2019

- El script `scan-and-cut.py` ahora hace todo el proceso de escaneado y detección de líneas.
- Hay un problema con los bordes del documento. Cuando los bordes hacen sombra, al aplicar el threshold a la imagen en 
escala de grises, sale una línea gruesa que afecta a la media de píxeles negros por línea. he probado aplicando pesos a
cada una de las líneas de manera que un 5% de los márgenes tenga menos peso en la media. Aún está por ver la validez de 
la solución.
- PENDIENTE: Cómo funciona el threshold que dibuja las líneas
    - Quizá puedo dibujar líneas por cada fila de array "casi" vacío en lugar de lo que está
    haciendo el algoritmo actual. Ningún threshold vale en general para todo. 
    
## 21/05/2019

- Prueba 1: He probado poniendo a 0 todos los elementos que estaban por debajo del threshold, pero el resultado en la 
práctica es el mismo. 
- Prueba 2: Ahora estoy probando a jugar con las medias. El problema es que la media de píxeles oscuros de una línea
no tiene por qué hacer justicia a los elementos que hay en esa línea. Un ejemplo es que una de las últimas líneas de
merc3.jpeg hay un "3030". En ese conjunto de líneas, las partes centrales de las mitades superior e inferior (si
separamos horizontalmente en 5 partes iguales la línea, la 1 y la 3, tienen menos píxeles que los extremos y el 
ecuador). Para _threshold_ altos, que rinden bien en otras líneas (píxel y=459), el "3030", se parte en 4 líneas...
    - Ahora mismo estoy probando a sacar la media de 3 líneas y de ahí probar un threshold normal. Sin embargo , la 
    media lo que hace realmente es suavizar o "difuminar", las diferencias y no parece funcionar bien.

- PENDIENTE: Hay que probar a sacar medias ponderadas en que se de más valor a medias altas. o podemos probar
también haciendo la función nosotros en lugar de REDUCE_AVG, con REDUCE_SUM. También podemos hacer esta función por
partes: si un píxel tiene inmediatamente encima y/o inmediatamente debajo otro, le damos más valor. Así elaboramos
un sistema de "premios", que daría mucho más peso a píxeles rodeados, y evitaría el problema de líneas sueltas como
en el píxel y=459
- PENDIENTE: Probar a "emborronar" la foto horizontalmente, sacando la media de los píxeles del entorno en _X_.
    
## 25/05/2019

- BINGO! Haciendo un difuminado horizontal (horizontal blur) de la imagen, las líneas quedan mejor definidas, y se
evitan imprecisiones como la que se daba en la línea del "3030" para la parte media e la línea. Sin embargo, se observan
algunos problemas con las mayúsculas (en upper camel case) y línas ligeramente torcidas por un lado, y por otro con 
aquellas líneas que tienen distintas alturas (por distintas fuentes por ejemplo).
    - Líneas de distinta altura: En el píxel y=240 y el y=260, la palabra "NIF" es más alta que el propio NIF, que está 
    en una fuente ligeramente menor. Esto da lugar a la detección de 2 líneas, en lugar de 1 como realmente es.
    Igual pasa para teléfono.
    - Líneas mayúsculas y ligeramente torcidas: En el caso del título "Avenida Infante Juan Manuel", el ticket está
    ligeramente abombado en el centro, lo que tuerce suavemente la línea como una campana de gauss., algunas letras
    quedan por este motivo ligeramente cortadas, y hay que observar la capacidad que tiene el OCR de sobreponerse a
    esta falta de información.    
    
- [ ] PENDIENTE: Cómo se genera el kernel? Generar uno combinado? Es decir, combinando bluring horizontal y vertical.
    - [ ] Probar un bluring vertical muy pequeño tras el horizontal para ver si de esa manera conseguimos
homogeneizar los problemas de líneas.
- [x] Probar a dibujar las líneas un píxel por encima del detectado, para superiores, y uno por debajo para
inferiores. El número "3030" queda cortado por abajo por estar ligeramente torcido el primer 3 (más exterior en la 
hoja)
- [ ] PENDIENTE: (también para "homogeneizar" el problemad de las líneas) Probar a sacar una media de altura de línea y
a partir de ahí, sacar un porcentaje de margen para cortar cada imagen.
- [ ] PENDIENTE: Probar a sacar las proporciones del ticket para aplicar thresholds distintos a cada porción.
- [ ] PENDIENTE: Dejo pendiente probar con thresholds distintos (para detección de líneas con texto), en los distintos
puntos del ticket. Ejemplo: Podríamos usar un threshold de 11.0 en el primer tercio del ticket, uno de 15.0 en el
segundo, y uno de 3.0 en el tercero, según la longitud de las líneas, la alineación, etc.

    
## 10/06/2019 

- Me pongo con el reconocimiento de texto.
- Apis: he probado varias apis para ver qué resultados dan. La mayoría no valen para nada. Google Cloud es 
indescifrable. Por lo demás he probado Cloudmersive, Taggun y alguna más, todas fallan estrepitosamente. La única que
detecta muy bien toda la información es Textract de aws.
- [ ] PENDIENTE: AWS devuelve información sobre los puntos en los que encuentra texto? Si lo hace podríamos obtener
líneas de producto de esa manera.
- [ ] PENDIENTE: Estudiar la viabilidad de integrar AWS, o de entrenar nuestro propio OCR.
- Me he quedado a medio de hacer este 
(tutorial)[https://docs.aws.amazon.com/es_es/IAM/latest/UserGuide/getting-started_create-admin-group.html]
he creado un usuario administrador de IAM (consola).
- Y si implemento un detector de texto, y con las coordenadas xy es como detecto las líneas??...