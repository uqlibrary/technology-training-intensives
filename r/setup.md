---
title: R with Positron
---

## Overview

Welcome to our three-day R training intensive! This runs twice a year and the next intensive will be in late January.

By the end of the three days, you'll have learnt the R skills to manipulate, visualise and present data. We'll spend roughly half the time learning content, and half the time working on a project in groups.

As we set up, there's a few things to do, if you haven't already:

1. [Install the software](https://uqlibrary.github.io/technology-training/R/installation.html)
2. Introduce yourself to your table
3. [Join our Teams channel](https://forms.office.com/Pages/ResponsePage.aspx?id=z3fjtrOdy0aRovrZYFuxXEzmI13TctBBiWhneXZv-1lUQ1MwQ0JUM0ZBS0hXV1NJSU04TEZEUFg2Si4u)
4. Register your attendance (QR code on screen or printed attendance sheet)

## R + Positron

The [R programming language](https://cran.r-project.org/) is a language
used for calculations, statistics, visualisations and many more data
science tasks.

[Positron](https://positron.posit.co/) is an open source
Integrated Development Environment (IDE) for R and Python, which means it provides
many features on top of R to make it easier to write and run code.

R’s main strong points are:

- **Open Source**: you can install it anywhere and adapt it to your
  needs;
- **Reproducibility**: makes an analysis repeatable by detailing the
  process in a script;
- **Customisable**: being a programming language, you can create your
  own custom tools;
- **Large datasets**: it can handle very large datasets (certainly well
  beyond the row limitations of Excel, and even further using
  [HPCs](https://rcc.uq.edu.au/high-performance-computing) and [other
  tricks](https://rviews.rstudio.com/2019/07/17/3-big-data-strategies-for-r/));
- **Diverse ecosystem**: packages allow you to extend R for thousands of
  different analyses.

The learning curve will be steeper than point-and-click tools, but as
far as programming languages go, R is more user-friendly than others.

### Installation

For this course, you need to have both R and Positron installed
([installation
instructions](https://uqlibrary.github.io/technology-training/R/installation.html)).

## R Projects

Let’s first create a new project:

- Click the "Folder Selector" menu button (top right corner), then “New Folder from Template..."
- Click "R Project" and "Next"
- In Folder name”, type the name of your project, for example
  “YYYY-MM-DD_rstudio-intro”
- For "Location", browse and select a folder where to locate your project (otherwise, the default will be your home directory)
- Click "Next"
- In "Project Configuration", keep the defaults, click "Create" and finally "Current window"
- 

> R Projects make your work with R more straight forward, as they allow
> you to segregate your different projects in separate folders. You can
> create a project in a new directory, or an existing directory that
> already has the files you need (e.g. data files). Everything then happens by default in
> this directory. Positron remembers which project you were working in last, and gives you the recent projects in the "Folder Selector" menu.

## Workshops

Over these three days we'll cover six sessions of content:

| Session | Description |
| --- | --- |
| [The Fundamentals](./Essentials/1-Fundamentals.qmd) | The basics of R. Variables, functions and packages.
| [Data processing](./Essentials/2-Data_processing.md) | Importing, manipulating and analysing data with `dplyr` |
| [Visualisation](./Essentials/3-Visualisation.qmd) | Creating visualisations of our data with `ggplot2` |
| [Sharing and Publishing](./Essentials/4-Sharing_and_Publishing.qmd) | Using GitHub for sharing and version control, as well as quarto for publishing dashboards and websites. |
| [Statistics](./Advanced%20topics/5-Statistics.qmd) | Descriptive and inferential statistics, with some regressions and hypothesis testing. |
| [Programming Essentials](./Advanced%20topics/6-Programming.qmd) | R tools everyone should know. Conditionals, loops and functions. |

These content sessions are pretty packed, and we won't have too much time to deviate. That's why we'll also have five project sessions - see [Project Overview](../project/details.qmd) for details. You're welcome to ask lengthier questions and play around there!