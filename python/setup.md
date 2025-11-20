---
title: Introduction and setup
---

:::{.callout-tip}
Registrations available for our next intensive!

**[Book for 3rd-5th Feb 2026](https://studenthub.uq.edu.au/students/events/detail/5909456)**
:::

## Overview
Welcome to our three-day Python training intensive! This runs twice a year and the next intensive will be in early February.

By the end of the three days, you'll have learnt the Python skills to manipulate, visualise and present data. We'll spend roughly half the time learning content, and half the time working on a project in groups.

As we set up, there's a few things to do, if you haven't already

1. [Install the software](#software)
2. Introduce yourself to your table
3. [Join our Teams channel](https://forms.office.com/Pages/ResponsePage.aspx?id=z3fjtrOdy0aRovrZYFuxXEzmI13TctBBiWhneXZv-1lUQ1MwQ0JUM0ZBS0hXV1NJSU04TEZEUFg2Si4u)
4. [Register your attendance]()

## Software

We are going to use Spyder for writing and running Python. This is a friendly interactive development environment (IDE) aimed at researchers. **However, you are more than welcome to use your own!**

We recommend [installing the Anaconda distribution](https://www.anaconda.com/download/success), which comes with Spyder and Python. You're welcome to use your own IDE if you'd prefer.

Once you have Anaconda installed, **launch Spyder**, either by searching for "Spyder" on your computer or opening the Anaconda Navigator.

We'll also be using the rendering and publishing tool Quarto from day 2. You're welcome to try set this up, the easiest way is 

1. Open an "Anaconda prompt" from the navigator
2. Run `conda install conda-forge::quarto`

You can also install it directly from the [Quarto website](https://quarto.org/docs/download/).

### Google Colab

If you aren't able to install Python and a suitable IDE on your device (e.g. if you do not have permission) then we can find an online alternative for you, likely in the form of [Google Colab](https://colab.google/). Let us know and we'll help you get set up!

## Creating a Project

If you're using Spyder, we recommend you create a **project**. Projects are just fancy folders, and they make it easier to access files (i.e. data) and export images (i.e. visualisations) all in the one place.

1. Open Spyder
2. In the *Projects* menu, click *New Project...*
3. Choose *New Directory*, give your project a name and find an appropriate place on your computer for it.
4. Press *Create*

Done! We'll work in this project for the duration of the intensives.

## Workshops

Over these three days we'll cover six sessions of content:

| Session | Description |
| --- | --- |
| [The Fundamentals](./Essentials/1%20-%20Fundamentals.qmd) | The basics of Python. Variables, functions and modules.
| [Data processing](./Essentials/2%20-%20Data%20processing.qmd) | Importing, manipulating and analysing data with `pandas` |
| [Visualisation](./Essentials/3%20-%20Visualisation.qmd) | Creating visualisations of our data with `seaborn`, `matplotlib` and `plotly`
| [Sharing and Publishing](./Essentials/4%20-%20Sharing%20and%20Publishing.qmd) | Using GitHub for sharing and version control, as well as quarto for publishing dashboards and websites. |
| [Statistics](./Advanced%20topics/5%20-%20Statistics.qmd) | Descriptive and inferential statistics, with some regressions and hypothesis testing, using `scipy.stats` and `statsmodels` |
| [Programming Essentials](./Advanced%20topics/6%20-%20Programming.qmd) | Python tools everyone should know. Conditionals, loops, functions and importing scripts. |

These content sessions are pretty packed, and we won't have too much time to deviate. That's why we'll also have five project sessions - see [The Project](../project/details.qmd) for details. You're welcome to ask lengthier questions and play around there!