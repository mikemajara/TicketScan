python-tesseract-3.02-training
==============================

A script to partially automate the training of new fonts/languages with Tesseract 3.02 - part of the Open ICR Project:
http://opensource.newmediaist.com/open-source-icr.html

<p>The <a href="https://code.google.com/p/tesseract-ocr/">Tesseract OCR Engine</a> is a powerful open source text recognition engine, designed specifically for machine-printed text (fonts). Tesseract can be trained to both improve recognition accuracy, as well as teach it new languages. Training Tesseract is just another way of saying adding new fonts to tesseract. Training Tesseract 3.02 can be difficult for the novice though, as the <a href="https://code.google.com/p/tesseract-ocr/wiki/TrainingTesseract3">official instructions</a> are long and complex. We built a simple Python script to somewhat automate the Tesseract 3.02 language file build process. 
</p>

<h2>How to use</h2>
<p>Usage of this script assumes <b>Python</B> and <b>Tesseract</b> are both installed correctly on computer, and also that you have </b>already generated your training text and box files</b>. If you have not generated your training text yet, here is one of the simplest methods to do so:
<ol>
<li><b>Collect image of text in TIF format</b> - scan a sample document printed in the desired font, or create a <a href="http://michaeljaylissner.com/blog/adding-new-fonts-to-tesseract-3-ocr-engine#create-training-docs" target="_blank">new sample document</a></li>
<li><b>Upload TIF to <a href="http://pp19dd.com/tesseract-ocr-chopper/" target="_blank">this online box editor</a></b>, and correct any errors in character detection. Select the box file information from the right side of the tool, copy it to your clipboard, and paste it into a new blank text file. Save the textfile with the same name as the document image, but with a .box extension - for example, "scanned-image.box".</a>
</ol>
Save your training image and box file into the same directory as the training script, then running the following command:
<p>
  <b>python traininscript.py language fontname</b>
</p>
</p>
<p>Code licensed under <a href="http://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License v2.0</a></p>
