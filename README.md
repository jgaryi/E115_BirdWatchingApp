## Project Milestone 4 - E115 - Birdwatching App
   
#### Project Milestone 4 Organization

```
├── Readme.md
├── images 
├── notebooks
│   ├── BirdWatchingApp.ipynb
│   ├── Acoustic_Monitoring_EDA.ipynb
│   ├── Interactive_Map_Biodiversity.ipynb
│   ├── Interactive_Map_Bird_Locations.ipynb
│   ├── Interactive_Map_Deforestation.ipynb
│   ├── SemanticScholar.py
│   ├── cli.py
│   └── preprocess_cv.py
│   
├── references
├── reports
│   ├── BirdWatchingAppMidterm.pdf
│   └── Statement of Work_Sample.pdf 
│
└── src  
    ├── api-service
    │    ├── api
    │    │   ├── routers
    │    │   ├── utils
    │    │   ├── service.py
    │    ├── docker-entrypoint.sh
    │    ├── docker-shell.sh
    │    ├── Dockerfile
    │    ├── Pipfile
    │    ├── Pipfile.lock
    ├── frontend-react
    │    ├── public
    │    ├── src
    │    ├── Dockerfile
    │    ├── docker-shell.sh
    └── vector-db        

```

# E115 - Milestone4 - Birdwatching App

**Team Members:** Jaqueline Garcia-Yi, Susan Urban, Yong Li, and Victoria Okereke

**Group Name:** Birdwatching App

**Project:**  
This project aims to develop an AI-powered bird identification and knowledge application, using the Yanachaga Chemillen National Park in Peru as a case study. The app will offer two primary methods for bird recognition: (1) users can upload a sound file for automatic identification, powered by an acoustic AI model, or (2) manually search for a bird by its scientific name using a dropdown menu to select from one of nine species.<br>

If the identified bird is one of the 500 species found in the national park but not listed in the dropdown menu, the app will display only the species name and return to the initial page when clicked again. If the bird is one of the nine pre-selected species—whose populations are vulnerable and decreasing—the app will provide detailed information about the species, its migratory path, and an image for visual reference. <br>

Interactive maps will show the bird's previously identified locations within the national park, habitat details, and changes over time that help explain why these species are vulnerable or endangered. Another map will also highlight other areas where the bird is likely to be found, based on predictions from a geo-referenced model using remote sensing data. Additionally, a built-in chatbot will allow users to ask bird-related questions and receive answers powered by a Large Language Model with Retrieval-Augmented Generation (LLM-RAG).<br>

The statement of work and lastest version of the project wireframe are available here: [`reports/`](reports/)  
<br><br>

----

## Milestone4 ##

In this milestone, we have the components for frontend, API service, also components from previous milestones for data management, including versioning, as well as the interactive maps, and acoustic and language models.

After completions of building a robust ML Pipeline in our previous milestone we have built a backend api service and frontend app. This will be our user-facing application that ties together the various components built in previous milestones.

### 1. Application Design ###

Before we start implementing the app we built a detailed design document outlining the application’s architecture. We built a Solution Architecture and Technical Architecture to ensure all our components work together.

Here is our Solution Architecture:

<img src="images/solution-arch.png"  width="800">

Here is our Technical Architecture:

<img src="images/technical-arch.png"  width="800">

The architectures follow a state of the art design using enterprise COTS and open source products. A Google Earth API is added in support of the several maps used in the app. 

<<<<<<< HEAD
<<<<<<< HEAD

**Backend API**
=======
=======

>>>>>>> bd1f5cc3af336ff388b60770c88bb8e530c3ad53
### 2. Backend API ###
>>>>>>> a60db3e4c99205c015520f1ad3e40bd4c2b3ac47

We built backend api service using fast API to expose model functionality to the frontend. We also added apis that will help the frontend display some key information about the model and data. 

<img src="images/api-list.png"  width="800">

**2.1. Acoustic Model for Bird Species Identification**
Bioacoustic analysis of bird songs, is a novel and non-invasive technology which provides a rich windlow into biodiversity and ecosystem health for national park protection and convervation. There are several deep learning model developed for the biacoustic identification of birds, BirdNET is one of the most popular models which was trained with EfficientNet architecture, and a broader training set of more than 6000 bird species and some non-avian species. To enable a range of downstream use-cases, BirdNET trades off some accuracy for efficient computation. The BirdNET code is available on GitHub§, and includes support for training small classifiers on embeddings by using transfer learning (see Section 5.3). In the selected 11 speices, 9 of them are in the list of training data set. Those species can be directly identified and monitored by the BirdNET model, and for the other 2 species, we will apply transfer leaning to process it. 

**2.2. Bird Knowledge Expert (LLM-Agent Chatbot)**

### 3. Frontend React ###

A user friendly React app was built to identify various species of mushrooms in the wild using computer vision models from the backend. Using the app a user can take a picture of a mushroom and upload it. The app will send the image to the backend api to get prediction results on weather the mushroom is poisonous or not. 

Here are some screenshots of our app:

```Add screenshots here```

<<<<<<< HEAD

## Running Dockerfile
=======
**3.1 Interactive Maps**

**3.2 **

### 4. Running Dockerfile ###




### 5. Notebooks/Reports ####
This folder contains code that is not part of container - for e.g: Application mockup, EDA, any 🔍 🕵️‍♀️ 🕵️‍♂️ crucial insights, reports or visualizations.

**5.1 Web Scrapping and Data Versioning**

**5.2 Acoustid Model for Bird Identification**

**5.3 Transfer Learning for Identification of Rare Bird Species**

**5.4. Interactive Maps**


### 6. Work in Progress ####
**6.1 Transfer learning**

**6.2 Other Topics**

The team identified the following future tasks for development and testing:

1. Update internal code baseline from using cheese to bird naming conventions
2. Problem resolution of an intermittent error for the chat input resulting in an Axios error
3. Implement CI for multiple containers once we complete the lectures on this topic


