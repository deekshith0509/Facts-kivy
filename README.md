# Awesome Facts App

Awesome Facts is a KivyMD application that fetches random facts from an API and displays them along with their categories. Users can fetch facts, view their history, and clear it if desired.

## Features

- Fetch random facts or tech facts.
- View a history of fetched facts.
- Clear history of facts.
- Light and dark theme toggle.

## Installation

### Prerequisites

- Python 3.6 or higher
- Kivy 2.0 or higher
- KivyMD 0.104.2 or higher
- Requests library

### Setup

1. Clone this repository:

   ```bash
git clone https://github.com/deekshith0509/MetroNavigator-WebApp.git
cd MetroNavigator-WebApp
```
2. Install the required dependencies:
```
pip install kivy kivymd requests
```

3. Run the application:
```
python main.py
```

## Usage

- Click on "Fetch Random Fact" to get a random fact.
- Click on "Tech Fact" to retrieve a tech-related fact.
- The history of facts can be accessed by clicking on the history icon in the app bar.
- Clear the history if you want to reset it.

## API

This application fetches facts from the following API:
- Endpoint: https://facts7878.glitch.me/{category}
- Categories:
  - random - Fetch a random fact.
  - tech - Fetch a tech-related fact.

## Contributing

Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create your feature branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a pull request.

