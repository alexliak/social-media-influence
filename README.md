# Social Network Analysis Project
This case study ideally is the discussion of a custom unit tested algorithm to calculate the influence and the engagement rate of each member of a simplified social network giving two formulas. The social networks calculate engagement rate using this formula: (total likes + total comments) / followers * 100. The influence of a member A to a member B is calculated by: (likes A to B + comments A to B) / total engagement rate of A. In this network members can follow other members without the requirement of following back. The primary objective is to represent a social network with suitable data structures. Finally, it must be identified the shortest and the highest engagement path between any given pair of members noting that there is not always a path from a member A to a member B.  
## Description
This project analyzes social network interactions using various algorithms to calculate engagement rates, influence, and paths within the network.

## Installation
IDE Visual Studio code

### Prerequisites
- Python 3.x

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/alexliak/social-media-influence.git
2. cd code-influence
3. python -m venv venv 
4. .\venv\Scripts\activate
5. pip install -r requirements.txt

### Usage
1. python src/main.py

line 267 in main.py # Adding members range

### Testing
1. pytest src/tests/
