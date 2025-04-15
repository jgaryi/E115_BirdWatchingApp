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
│   └── Interactive_Map_Deforestation.ipynb
├── references
├── reports
|   ├── BirdWatchingAppMidterm.pdf
│   └── Statement of Work_Sample.pdf 
└── src
    ├── datapipeline
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── dataloader.py
    │   ├── docker-shell.sh
    │   ├── preprocess_cv.py
    │   └── preprocess_rag.py
    ├── api-service 
    ├── frontend
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

### Milestone4 ###

In this milestone, we have the components for frontend, API service, also components from previous milestones for data management, including versioning, as well as the computer vision and language models.

After completions of building a robust ML Pipeline in our previous milestone we have built a backend api service and frontend app. This will be our user-facing application that ties together the various components built in previous milestones.

**Application Design**

Before we start implementing the app we built a detailed design document outlining the application’s architecture. We built a Solution Architecture and Technical Architecture to ensure all our components work together.

Here is our Solution Architecture:

<img src="images/solution-arch.png"  width="800">

Here is our Technical Architecture:

<img src="images/technical-arch.png"  width="800">


**Backend API**

We built backend api service using fast API to expose model functionality to the frontend. We also added apis that will help the frontend display some key information about the model and data. 

<img src="images/api-list.png"  width="800">

**Frontend**

A user friendly React app was built to identify various species of mushrooms in the wild using computer vision models from the backend. Using the app a user can take a picture of a mushroom and upload it. The app will send the image to the backend api to get prediction results on weather the mushroom is poisonous or not. 

Here are some screenshots of our app:

```Add screenshots here```

## Running Dockerfile
Instructions for running the Dockerfile can be added here.
To run Dockerfile - `Instructions here`


**Notebooks/Reports**
This folder contains code that is not part of container - for e.g: Application mockup, EDA, any 🔍 🕵️‍♀️ 🕵️‍♂️ crucial insights, reports or visualizations.

----
You may adjust this template as appropriate for your project.
