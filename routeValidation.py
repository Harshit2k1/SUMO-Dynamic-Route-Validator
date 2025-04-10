import sys
import xml.etree.ElementTree as ET
import traci
import traci.constants as tc

# Define Map and Route Files at the top of the script.
MAP_FILE = "map.net.xml"        # Network file for the simulation.
ROUTES_FILE = "routes.rou.xml"    # Routes file containing the routes definitions.

def extract_route_ids(routes_file):
    """
    Parse the routes file (XML) and extract all the route ids.
    This function assumes that the routes file contains elements like:
    <route id="route_X" .../>
    """
    try:
        tree = ET.parse(routes_file)
        root = tree.getroot()
        # Find all <route> elements and extract their 'id' attribute.
        route_ids = [elem.attrib['id'] for elem in root.findall("route") if 'id' in elem.attrib]
        print(f"Found routes: {route_ids}")
        return route_ids
    except Exception as e:
        print(f"Error parsing routes file: {e}")
        return []

# Dictionary to store vehicle information: route and stall counter.
vehicle_info = {}

def add_vehicle_for_route(route_id, veh_id):
    """
    Add a vehicle with the specified route from the routes file.
    The vehicle is scheduled to depart at simulation time 0.
    """
    try:
        traci.vehicle.add(veh_id, route_id, depart="0")
        vehicle_info[veh_id] = {"route": route_id, "stall_count": 0}
        print(f"Added vehicle {veh_id} for route {route_id}")
    except Exception as e:
        print(f"Error adding vehicle for route {route_id}: {e}")

def run_simulation(max_steps=1000, stall_threshold=50):
    """
    Run the simulation for a fixed number of steps.
    Monitors each vehicle’s speed to detect if it stalls for too long,
    which may indicate an error in the route (e.g., disconnected network segments).
    """
    step = 0
    error_routes = {}       # Dictionary to store error messages for problematic routes.
    successful_routes = []  # List to store routes that complete successfully.

    while step < max_steps and vehicle_info:
        traci.simulationStep()
        current_vehicles = traci.vehicle.getIDList()

        # Iterate over a snapshot of vehicle_info keys.
        for veh_id in list(vehicle_info.keys()):
            if veh_id in current_vehicles:
                # Check vehicle's speed; consider near-zero speed as stalled.
                speed = traci.vehicle.getSpeed(veh_id)
                if speed < 0.1:
                    vehicle_info[veh_id]["stall_count"] += 1
                else:
                    vehicle_info[veh_id]["stall_count"] = 0

                # If vehicle stalls for too long, flag the route.
                if vehicle_info[veh_id]["stall_count"] >= stall_threshold:
                    route = vehicle_info[veh_id]["route"]
                    error_routes[route] = f"Vehicle {veh_id} stalled for {stall_threshold} consecutive steps."
                    traci.vehicle.remove(veh_id)
                    del vehicle_info[veh_id]
            else:
                # Vehicle left the simulation (arrived at destination successfully).
                route = vehicle_info[veh_id]["route"]
                successful_routes.append(route)
                del vehicle_info[veh_id]
        step += 1

    # Any vehicle still tracked after simulation ends is flagged as an error.
    for veh_id, info in vehicle_info.items():
        error_routes[info["route"]] = "Vehicle did not complete the route within the simulation time."

    return error_routes, successful_routes

def main():
    # Extract route IDs from the routes file.
    routes = extract_route_ids(ROUTES_FILE)
    if not routes:
        print("No routes were found in the routes file. Exiting...")
        return

    # For each extracted route, add a vehicle to the simulation.
    for route in routes:
        veh_id = f"veh_{route}"
        add_vehicle_for_route(route, veh_id)

    # Run the simulation and gather results.
    error_routes, successful_routes = run_simulation()

    print("\n--- Route Check Results ---")
    if error_routes:
        print("Routes with errors:")
        for route, error in error_routes.items():
            print(f" - {route}: {error}")
    else:
        print("No route errors found.")

    if successful_routes:
        print("\nSuccessful Routes:")
        for route in successful_routes:
            print(f" - {route}")

if __name__ == "__main__":
    # Define the command for starting SUMO using the file paths defined at the top.
    sumoCmd = ["sumo", "-n", MAP_FILE, "-r", ROUTES_FILE]
    try:
        traci.start(sumoCmd)
    except Exception as e:
        print("Error starting SUMO:", e)
        sys.exit(1)

    try:
        main()
    except Exception as e:
        print("Error during simulation:", e)
    finally:
        traci.close()
