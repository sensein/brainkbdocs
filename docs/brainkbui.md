# User Interface Overview 
This section offers a detailed overview of the UI, including its layout, design elements, and functionality. It provides insights into how users can navigate the interface, interact with various components, and utilize its features effectively to achieve their goals.
Additionally, it highlights key elements that enhance user experience, such as responsiveness, accessibility, and ease of use.
## Overview

The BrainKB UI (user interface), accessible at [beta.brainkb.org](https://beta.brainkb.org), is a user-centric interface designed to interact with the BrainKB knowledge graph infrastructure. It enables neuroscientists, researchers, and practitioners to explore, search, analyze, and visualize neuroscience knowledge effectively. The platform integrates a range of tools and features that facilitate evidence-based decision-making, making it an essential resource for advancing neuroscience research.
 
**Key Features:**
- **Search**: Allows users to filter and refine queries based on criteria like species, data type, and file size.
- **Interactive Visualizations**: Offers dynamic visual representations of knowledge graphs to enhance understanding and exploration.
- **Collaboration Support**: Facilitates shared exploration and collaboration, such as contributing assertions and evidence.

This beta release, currently in the development stage, highlights the evolving capabilities (also note that all features are not yet available) of BrainKB and actively invites user feedback to further enhance its functionality and usability.

## Rapid Release
The sequence diagram below illustrates the steps involved in the rapid release process. Currently, the workflow is semi-automated, particularly in the stages of fetching data from the graph database (Oxigraph) and uploading it to an AWS S3 bucket.
The data from AWS S3 is automatically retrieved, processed, and displayed in the UI, allowing users to download it seamlessly. {numref}`brainkb_data_release` presents the visualization of the data retrieved from the AWS S3 bucket and displayed in the UI.

Data in AWS is organized hierarchically by release, adhering to a structured directory pattern that must be followed when uploading data ({numref}`brainkb_data_release_aws_s3_directory_structure`). {numref}`brainkb_data_release_aws_s3_ui_mapping` demonstrates how this AWS directory structure is mapped to the user interface.

```{mermaid} 
sequenceDiagram
    actor User
    participant UI as User Interface
    participant DB as Graph Database
    participant S3 as AWS S3 Bucket

    rect rgba(230, 210, 231, 0.5)
    note right of User: Manual Steps
    User ->> DB: Fetch Data from Graph Database
    DB -->> User: Data Retrieved
    User ->> S3: Upload Data to S3
    S3 -->> User: Confirm Upload
    end

    rect rgba(200, 255, 200, 0.5)
    note right of UI: Automated Steps
    UI ->> S3: Fetch Data from S3
    S3 -->> UI: Data Retrieved
    UI ->> UI: Process and Visualize Data
    UI ->> User: Display Data for Download
    end
```

```{figure} images/data-release.png
:name: brainkb_data_release
BrainKB rapid release page.
```


```{figure} images/brainkb_rapid_release.png
:name: brainkb_data_release_aws_s3_directory_structure
BrainKB rapid release: Organized AWS S3 bucket directory structure for efficient data management.
```
```{figure} images/data_release_aws_s3_ui_mapping.png
:name: brainkb_data_release_aws_s3_ui_mapping
Mapping BrainKB's AWS S3 bucket directory structure to the user interface for streamlined data access and visualization.
```
## Snapshots of UI

```{figure} images/home.png
:name: brainkb_uihome_figure
BrainKB UI home page.
```

```{figure} images/login.png
:name: brainkb_uilogin_figure
BrainKB UI login page.
```

