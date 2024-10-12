# Car-loan-calculator
<img src="https://github.com/user-attachments/assets/af6f0dac-3ef7-4f55-9888-1dd70bdf223a" alt="Car Loan Calculation Interface" width="400" height="400">


## Table of Contents

1. [Overview](#overview)
2. [Skills](#skills)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

## Overview

This project which is written in Python will ask you the data of 2 cars you're interested in and in the end, it will compare them. After using this program, it will be easier for you to make your final decision about the car. This program is designed to be run in the command line and it will visualize the data in the end.

- **Version:** 1.0
- **Language:** Python
- **Libraries Used:** 
    - `pandas`
    - `numpy`
    - `matplotlib`
    - `selenium`
    - `Beautiful soup`
      
## 🛠 Skills
Python, web Scrapping, APIs

## Features

List the key features of your project, for example:

- Takes user input for car details and calculates loan payments.
- Provides insurance rate estimates.
- Visualizes data with graphs.

## Installation

Before installation, make sure your system meets the following requirements:
    -Python 3.x
Furthermore, you will need to have an API Token Key. In order to do so
1. sign up in:
   <a href="https://collectapi.com/"> Collect API </a>
2. Head to your account and then choose Profile
3. Click on the API Token tab
4. Copy your API Token
   ![Screenshot 2024-10-12 164243](https://github.com/user-attachments/assets/68f61df6-3011-49bd-a25c-3587523f3eec)
5. click on the following link
   <a href="https://collectapi.com/api/gasPrice/gas-prices-api?tab=pricing"> Gas Price API </a>
6. Choose Free Trial
This will be the JSON result we'll get
![Screenshot 2024-10-12 164612](https://github.com/user-attachments/assets/255952fb-3bc1-4835-a7a8-739830fcec3f)
After getting your api key and set it in the Calculation.py
7. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/yourprojectname.git
8. Navigate to the project directory:
     ```bash
   cd yourprojectname
9. (Optional) Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
10.Install dependencies
    ```bash
    pip install -r requirements.txt



## API Reference

#### Get all states

```http
  GET /stateUsaPrice
```

| Field    | Description                |Type | API Key
| :--------  | :------------------------- |:-------|:-------|
| `api_key`  | Your API key, Enter state code AK, AL, WA... |`string` | **Required** |

#### Get item

```http
 curl --request GET \
  --url 'https://api.collectapi.com/gasPrice/stateUsaPrice?state=WA' \
  --header 'authorization: apikey 2mEOtOkfOYQkkzpImIkoVB:0A45VXobnK5s425B50CbJp' \
  --header 'content-type: application/json'

```


## Usage
1. Run the main script:
   ```bash
   python main.py
2. Follow the prompts to enter the required inputs(e.g., car model, year, your state, etc).
   
### Example
    ```bash
    What is your car brand? Toyota
    What is your car model? Corolla
    Enter the year of your car: 2021
    In which state of United States do you live? California
    What is your credit score? 720

## Contributing
If you like to contribute to this project please follow the guideline:
- Fork the repository
- Create a new branch (git checkout -b feature/your-feature)
- Commit your changes (git commit -am 'Add your feature')
- Push to the branch (git push origin feature/your-feature)
- Create a new Pull Request

## Visualize
![Untitled design (1)](https://github.com/user-attachments/assets/a08e659d-6560-45ce-8a7c-a6974c59e031)


## Contact
  - Kimiya Shabani @kimiyashabani
  - <a href="https://github.com/kimiyashabani/Car-loan-calculator"> Project link </a>

    

