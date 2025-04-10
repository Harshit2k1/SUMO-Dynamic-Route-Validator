# SUMO-Dynamic-Route-Validator

This tool is designed to ensure that routes defined for passenger vehicles in SUMO are fully traversable and free of connectivity issues.

## Advantages

- Runs a live simulation using the TraCI API, injecting a vehicle for each route to verify that the paths are operational.
  
- After simulation, the tool outputs which routes were completed successfully and which experienced stalls, providing clear insights for troubleshooting route issues.

- It parses an XML routes file to extract all route identifiers dynamically and then deploys a vehicle for each one. This minimizes the need for manual intervention and helps keep the validation process in sync with the latest route definitions.


- Designed to integrate seamlessly into existing SUMO workflows, ensuring routes intended for passenger vehicles are validated with minimal setup.

- By simulating actual vehicle behavior, the tool verifies that routes are not only adequately defined but also effective in real operating conditions, leading to greater confidence in route reliability for passenger service.

## How It Works

1. **Route Extraction:**  
   Reads an XML file containing route definitions and extracts all route identifiers.

2. **Vehicle Deployment:**  
   Inserts a passenger vehicle into the simulation for each route, starting at a preset departure time to mimic real-world conditions.

3. **Simulation Monitoring:**  
   Continuously monitors each vehicle's speed. If a vehicle’s speed falls below a defined threshold for a set number of simulation steps, it signals a potential issue with the route.

4. **Diagnostic Reporting:**  
   At the end of the simulation, the tool outputs detailed information, listing valid routes and flagging any routes where vehicles experienced issues.

## Getting Started

### Prerequisites

- **SUMO:**  
  Ensure that SUMO is installed and configured adequately with its TraCI interface.
  
- **Python 3+:**  
  The tool is compatible with Python 3 and above.

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Harshit2k1/SUMO-Dynamic-Route-Validator.git
   ```
2. **Configure Environment:**
   Make sure your `SUMO_HOME` environment variable is set correctly.


### Usage

1. **Prepare Your Files:**  
   Place your network file (e.g., `map.net.xml`) and routes file (e.g., `routes.rou.xml`) in the working directory.
   
2. **Run the Validator:**
   ```bash
   python routeValidation.py
   ```
   
3. **Review the Output:**  
   Examine the console output for detailed diagnostics. The report will indicate which routes are valid and identify those causing vehicles to stall.

## Contributing

Contributions and suggestions are welcome! To propose improvements or additional features, please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---
