# Ticket Scanner

Scans and parses tickets

### Libraries 📚

- [regex](https://pypi.org/project/regex/)
    - Not used in project.
    - Support for fuzzy regex matching.
    - Completely inefficient for BEST_MATCH
- [marshmallow](https://marshmallow.readthedocs.io/en/stable/)
    - Used in project
    - Serialization and deserialization of objects in python.
- [opencv](https://docs.opencv.org/3.1.0/index.html)
    - Used in project
    - image recognition.

### Links 🔗

- Referenced tutorials for image recognition
    - [OpenCV OCR and text recognition with Tesseract](https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/)
    - [OpenCV Text Detection (EAST text detector)](https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/)
    - [Using Tesseract OCR with Python](https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/)
    - [Basic Operations on Images](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_basic_ops/py_basic_ops.html)
- Tesseract data files
    - [language files](https://github.com/tesseract-ocr/tesseract/wiki/Data-Files)

### See Also

- [Deep Learning OCR using TensorFlow and Python](https://nicholastsmith.wordpress.com/2017/10/14/deep-learning-ocr-using-tensorflow-and-python/)
- [Links to awesome OCR projects](https://github.com/kba/awesome-ocr)
- 

## Troubleshooting & Known issues

## Performance analysis

- Processing the ticket from Mercadona takes about 23s
- Half of this time is consumed by PyTesseract (~12s) running in a different process.
    + This could be parallelized since there are 36 calls, which is exactly one call per line in the ticket.
- The other half is not fully understood yet.
- Pytesseract might be a bit slower than just using the C-api offered by tesseract
- According to Postman, a request usually takes 12s to get the result, so the rest might be just the time it takes to set up the profiler. This concludes that the top priority is to parallelize the usage of tesseract in order to speed up the response time.

#### Resources

- [Parallelize pytesseract](https://appliedmachinelearning.blog/2018/06/30/performing-ocr-by-running-parallel-instances-of-tesseract-4-0-python/)
- [C API for tesseract from Python](https://stackoverflow.com/questions/21745205/using-c-api-of-tesseract-3-02-with-ctypes-and-cv2-in-python)

The following output shows the profiling output of the post method in Server.py, ordered by time:

```
         145142 function calls (144334 primitive calls) in 12.175 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      108   11.448    0.106   11.448    0.106 {method 'poll' of 'select.poll' objects}
       36    0.131    0.004    0.131    0.004 {method 'encode' of 'ImagingEncoder' objects}
      180    0.074    0.000    0.074    0.000 {built-in method posix.read}
        1    0.062    0.062    0.062    0.062 {filter2D}
       36    0.056    0.002    0.056    0.002 {built-in method _posixsubprocess.fork_exec}
       75    0.026    0.000    0.026    0.000 {method 'copy' of 'numpy.ndarray' objects}
     8496    0.021    0.000    0.022    0.000 glob.py:114(_iterdir)
       36    0.018    0.000    0.018    0.000 {method 'tobytes' of 'numpy.ndarray' objects}
       36    0.017    0.000    0.189    0.005 subprocess.py:656(__init__)
        1    0.016    0.016    0.016    0.016 {imread}
      108    0.015    0.000    0.015    0.000 {built-in method posix.remove}
      221    0.013    0.000    0.013    0.000 {built-in method io.open}
       36    0.012    0.000    0.169    0.005 subprocess.py:1383(_execute_child)
       72    0.008    0.000    0.008    0.000 {method 'close' of '_io.BufferedRandom' objects}
       36    0.008    0.000   11.478    0.319 subprocess.py:1633(_communicate)
        1    0.008    0.008    0.008    0.008 slicer.py:140(<listcomp>)
       36    0.007    0.000    0.007    0.000 {GaussianBlur}
        1    0.007    0.007    0.007    0.007 slicer.py:142(<listcomp>)
        2    0.006    0.003    0.006    0.003 {built-in method _scproxy._get_proxy_settings}
       17    0.006    0.000    0.006    0.000 {method 'read' of '_io.FileIO' objects}
        5    0.006    0.001    0.006    0.001 {method 'recv_into' of '_socket.socket' objects}
       36    0.005    0.000   11.683    0.325 pytesseract.py:199(run_tesseract)
       36    0.005    0.000   11.999    0.333 pytesseract.py:232(run_and_get_output)
```

## Experiment with OCR

Summary of results with OCR. As of 3 Oct 2019 two tests were done to check how did payed services of OCR performed as
compared to the algorithms we implemented here.

In a first approach Microsoft's service was not as convincing as Amazon's so a couple of details will be given on this last one only.

- A test service is available (no account needed) where an image can be tested [here](https://us-east-2.console.aws.amazon.com/textract/home?region=us-east-2#/demo)
- Pricing can be checked out [here](https://aws.amazon.com/textract/pricing/). Main advantages: pay for use, OCR service is the cheapest in Computer Vision (~1.50$ for 1000 pages - EU Ireland server prices). 
- An account can be created following [this](https://docs.aws.amazon.com/textract/latest/dg/getting-started.html) start guide. Although there is already an administrator account created that can give access and create other accounts to test (Miguel).
- A bucket must be created for the service to work with images that are **already** uploaded into the bucket.
  - On a production environment, the aws-cli or boto3 (the tools provided by AWS) would have to be used to do the upload. In any case architecture would be a change, **the previous point refers to tests and notebook in proyect**.

At first AWS detects correctly most of the ticket (even more than we do as of now, for the example used). Following, an example of one of the texts detected and returned in the response:
```
[ 
  # ...
  {'BlockType': 'LINE',
  'Confidence': 71.305419921875,
  'Text': 'MERCADONA S S.A. A -O',
  'Geometry': {'BoundingBox': {'Width': 0.5924637317657471,
    'Height': 0.014716140925884247,
    'Left': 0.2752343714237213,
    'Top': 0.06579777598381042},
   'Polygon': [{'X': 0.2752343714237213, 'Y': 0.06579777598381042},
    {'X': 0.867698073387146, 'Y': 0.06579777598381042},
    {'X': 0.867698073387146, 'Y': 0.08051391690969467},
    {'X': 0.2752343714237213, 'Y': 0.08051391690969467}]},
  'Id': '640273c1-e92c-4b79-89ba-2e20bef5f174',
  'Relationships': [{'Type': 'CHILD',
    'Ids': ['01caab35-eb44-4fda-a1fd-0de39f1f1575',
     'cd4edff5-ad6c-4a0b-b625-f3d53e5df3c9',
     '0a542472-ee4e-48f0-b55b-ba65a42b01b1',
     '48795198-fcf5-4f5f-b31e-61a2b34388f9',
     '714372f2-aff2-42bf-8167-8fb9734dc217']}]},
 {'BlockType': 'LINE',
  'Confidence': 89.66963195800781,
  'Text': 'C/ MAYOR, 7 ESPINARDO',
  'Geometry': {'BoundingBox': {'Width': 0.4979221224784851,
    'Height': 0.01784255914390087,
    'Left': 0.25247466564178467,
    'Top': 0.11675985157489777},
   'Polygon': [{'X': 0.25247466564178467, 'Y': 0.11675985157489777},
    {'X': 0.7503967881202698, 'Y': 0.11675985157489777},
    {'X': 0.7503967881202698, 'Y': 0.1346024125814438},
    {'X': 0.25247466564178467, 'Y': 0.1346024125814438}]},
  'Id': '96f3aa64-0316-4213-9472-1413e5afe947',
  'Relationships': [{'Type': 'CHILD',
    'Ids': ['44fd17c9-b84f-4545-99b7-339bea76840e',
     '68b0843b-97f1-4efc-a1a0-8b184538ac71',
     'ec881e63-9234-4e98-84d4-c9a08c806beb',
     '8c0d83eb-a0a9-4b76-aa47-7fe8fdf92d16']}]}
     #...
]
```



### Note

This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
