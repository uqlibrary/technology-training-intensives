# UQ Library Technology Training Intensives

Source code for the [UQ Library Technology Training Intensives Website](https://uqlibrary.github.io/technology-training-intensives/). These intensives are three-day in-person training events held at The University of Queensland's St Lucia campus, and are run twice-yearly. The next intensives are scheduled for Jan-Feb 2026 and fully booked.

We currently run three intensives:

* R with RStudio
* Python for Data Analysis
* QGIS

The website is rendered using [quarto](https://quarto.org/) and published with [GitHub pages](https://docs.github.com/en/pages).

## Format of this repository

As the website is produced with [quarto](https://quarto.org/), the majority of source files are Quarto-markdown files (`.qmd`). These follow typical markdown conventions and enable code execution in-place.

### Workshops

The source material for each intensive can be found in the `r/`, `python/` and `qgis/` directories respectively. To view the content, we recommend visiting the [live website](https://uqlibrary.github.io/technology-training-intensives/).

### Projects

The intensives involve the development of a significant project during the three days, supplementing the content sessions. Past project submissions can be viewed [in the gallery](https://uqlibrary.github.io/technology-training-intensives/gallery/project_gallery.html), and their source code in the `gallery/` directory. General project guidelines live in `project/`.

### Data

Both the project and content sessions make use of open source data. Details on the datasets, which live in `data/`, can be found on the project's [Getting Started](https://uqlibrary.github.io/technology-training-intensives/project/scaffold.html) page.

### Automation

The `_processing/` directory contains various scripts which run before rendering. These serve two main purposes:

* Checking project submissions will render (or removing them before breaking the website)
* Checking and updating the main content's links and tabsets

In the unlikely event that automation is breaking your render, you can disable the scripts by removing the line `pre-render: _processing/pre_render.py` from `_quarto.yml`.

## Licence

All of the information on this repository (https://github.com/uqlibrary/technology-training) is freely available under the [Creative Commons - Attribution 4.0 International Licence](https://creativecommons.org/licenses/by/4.0/). You may re-use and re-mix the material in any way you wish, without asking permission, provided you cite the original source. However, we'd love to hear about what you do with it!

If you would like to develop on top of this, please cite the source as mentioned above, and conserve the git history if possible (so authors are credited).

## Contributing

You're welcome to [raise an issue](https://github.com/uqlibrary/technology-training-intensives/issues) or submit a change in this repository if you spot something that needs fixing. If you'd like to propose more substantial changes, feel free to contact us at [training@library.uq.edu.au](mailto:training@library.uq.edu.au).

This repository uses [renv](https://rstudio.github.io/renv/articles/renv.html) for R dependency management and `requirements.txt` (via [venv](https://docs.python.org/3/library/venv.html) or your preferred alternative) for Python dependencies. Please familiarise yourself with virtual environment management before submitting changes to dependencies.

If you have previously submitted a project and would like it removed or anonymised, please let us know and we will update the website accordingly. 

## Contact

If you are part of the UQ community, you can contact the technology trainers for a 1-on-1 consultation, an enquiry about sessions, or any question about the software supported by the UQ Library: [training@library.uq.edu.au](mailto:training@library.uq.edu.au)
