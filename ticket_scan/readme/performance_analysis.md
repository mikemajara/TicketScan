# Performance analysis

## Summary

- Processing the ticket from Mercadona takes about 23s
- Half of this time is consumed by PyTesseract (~12s) running in a different process.
    + This could be parallelized since there are 36 calls, which is exactly one call per line in the ticket.
- The other half is not fully understood yet.
- Pytesseract might be a bit slower than just using the C-api offered by tesseract
- According to Postman, a request usually takes 12s to get the result, so the rest might be just the time it takes to set up the profiler. This concludes that the top priority is to parallelize the usage of tesseract in order to speed up the response time.

## Resources

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
