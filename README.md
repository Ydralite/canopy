![image](https://github.com/Ydralite/canopy/assets/64652785/bf50b34d-9c1a-48fa-a25f-24537824223d)# Canopy

> A canopy is a majestic natural roof created by the interlocking branches of towering trees, sheltering a vibrant world of choices

This repo is a proposed solution to the challenge of generating view hierarchies from a description.
Please refer to the [presentation](docs/20240114_canopy_presentation.pdf) for a detailed understanding of the repo.

Refer to the [demo](output/demo.mp4) to see the app that generates a View Hierarchy from a description 

# Relevant Instructions
- Notebooks 
   - 1000-explore-hierarchy: Has the data exploration
   - 1010-generate-high-performing-vs: has the code to generate a High-Performing Vector Store
   - 1020-sample-ui-from-description: has the proposed solution to display sample UIs (from an existing database) that match a Description (open text field)
   - 1030-generate-new-ui-from-description: has the code to generate a new UI from a description **which is deployed in streamlit (below)**
 
 - Streamlit
   - Create a venv based on the requirements.txt file
   - Activate the environment
   - Run `python -m streamlit run main.py`
   - **Note**: you will need a open-ai key written in a .env file in the root environment

- utils: has cutom made functions and metadata relevant to run the notebooks and application
- output: includes the demo and some processed json files from the original view hierarchies + metadata

Any question feel free to reach out!
