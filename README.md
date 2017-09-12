# CDtool: Developer's Guide

## What is CDtool for?

CDtool is a tool for processing circular dichroism files. Its inputs are data files that represent circular dichroism experiments. It parses these and combines them where necessary. And its outputs are visualisations of the files in the form of charts, and processed data files that reflect any changes or actions performed on the file.

## What technologies does CDtool use?

### Django

CDtool is an example of a Django web application, and as such relies on HTTP and Python.

All websites work on the HTTP request/response cycle. In its simplest form, you make a request to a web server, telling it the URL of the resource you want. The server then finds the file on disk using the URL you gave, and returns it to the user using a HTTP response. So, a request for the URL `/about/contact.html` will cause the web server to look in the `about` directory of its local files and return the file `contact.html` to the browser that asked for it, which will then render the file as a web page.

This is a bit limited, as the server can only send files that exist on the server - it cannot generate files dynamically, or refer to databases, or do any of the things that most websites built since the late 90s are going to need to do.

PHP and JSP are examples of simple solutions to this problem. The server can still only return files that are saved on disk, but these files can have blocks of dynamically generated contact in them, which can make queries to databases, and all kinds of other things.

Web frameworks, of which Django is an example, are a more powerful (but more complex) solution. With web frameworks, when the server receives a request, it simply passes it to another program on the server, and waits for *that* program to spit out a response. In this case, the program is a Django program wirtten in Python.

Django programs take the URL of the request, and instead of matching it to a file on disk, match it to a Python function (called a **view**) using regex. This Python function then dynamically generates a response, which is returned to the server, and then to the user.

So, when a user requests of CDtool the page `/help/`, the request goes to the server, which passes it to the instance of the cdtool Django program that is running, which looks at the url, passes the request to the `help_page()` function, which produces a response. This is then passed back along the same route.

There's obviously a lot more to it than that, but that is the basic principle of how Django works. It allows for dynamically generated content, with clean speration of code into logic and page structure. And you get to write in Python, and not suffer the misery of writing in PHP or Java.

### inferi

inferi is a Python library for data processing. It is pure-Python and does not require compiling C libraries, like NumPy and Pandas. It is used to represent the data files that are given to Django.

### HighCharts

HighCharts is a JavaScript library for creating beautiful charts that are responsive, animated, and saveable as images. It is very powerful, has excellent documentation, and is used to render the visualsiation of the circular dichroism data.

## CDtool Terminology

### Scans

Circular Dichroism works by taking a bit of liquid, loading it into a small cell, loading the cell into a big machine, and shining circularly polarised light through it. It will shine light of one wavelength through it, and measure the difference in absorbance between the left and right handed light at that wavelength. Then light of a slightly different wavelength is used, and the absorbance difference measured there. And so on, until it reaches the last wavelength it has been told to look at.

It may record other things at each wavelength, such as the degree of 'tension' (a measure of how difficult it is for the light to get through the liquid), and uncertainty values associated with the measured circular dichroism.

So, at the end, you will have data that is a list of wavelengths, and for each wavelength there will be measurements associated. This data is referred to here as a **scan**. An example of a scan might be:

    Wavelength (nm)   CD    Error    HT
    270               0.04  0.00021  0.124
    269               0.03  0.00065  0.127
    268               0.07  0.00009  0.140
    ...

Often multiple scans are taken back to back. That is, the last measurement is made, and then the machine goes back to the original wavelength and goes through them all again. The idea being that the scans will be averaged to get a more reliable picture.

### Samples

The fundamental unit of CDtool is the **sample**. This is the bit of liquid that was loaded into the Circular Dichroism machine in the first place, and any associated bits of liquid, under a single condition.

For example, if you purify a protein and scan it with a CD machine, that is a sample as far as CDtool is concerned. If the scan was done in triplicate, so that there are three scans for it, which must be averaged - those three scans are all part of the same sample. If you put the flowthrough of the experiment into the CD machine, to get a baseline that will be subtracted from the scans of the protein, those baseline scans are also part of the sample.

If you scan two bits of liquid which contain different proteins, then they are obviously two different samples. But the same protein under different conditions will also produce multiple samples. For example, scanning a protein at 20 °C, raising the temperature to 25 °C, and then scanning again, will produce two samples as far as CDtool is concerned.

So, a sample is a colection of scans which form a unit. It can just be one scan, in which case that scan represents the sample. It can be multiple scans, in which case the average of those scans represents the sample. Or it can multiple scans dividied into regular scans and baseline scans, in which case the sample is represented by the average of the baseline scans subtracted from the average of the regular scans.

Currently CDtool can only handle one sample at a time.

## How does CDtool work?

### Inputs

The tool itself lives at the root URL, `\`. When a ``GET`` request is sent to this URL, the page will have the input section only.

This is a form that allows you to upload as many scans as the user wishes for a single sample. You can upload a single file with multiple scans in it, or upload multiple files, with zero or more scans in them. The sample can be given a name in this same section.

At the bottom of the form are the configuration options. Here you can set a name for the entire experiment.

### Processing

Submitting this form will send a `POST` request to the `\` URL, with a field for the various scan files, and fields for the sample name and experiment name.

Because the `\` URL is so heavily used, the view that it maps to simply passes the request on to different views depending on the nature of he request that is sent to it. For example, the root view will pass the request on to either the `root_get` view or the `root_post` view depending on the method used, with `root_get` being the view that returns the page described above.

`root_post` in this case will see that scans are being uploaded and so will forward the request on to the `process_scans` view.
