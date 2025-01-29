import os
import sys
import optparse
import pandas as pd
import traceback
from sumolib import checkBinary
import traci

# Check if SUMO_HOME environment variable is set
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

def get_options():
    """Handles options when running the script (e.g., with or without GUI)."""
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False,
                          help="Run the commandline version of SUMO (no GUI)")
    options, _ = opt_parser.parse_args()
    return options

def reroute_vehicles_on_closed_lanes(lanes_to_close):
    """Reroute vehicles that are on closed lanes."""
    for veh_id in traci.vehicle.getIDList():
        lane_id = traci.vehicle.getLaneID(veh_id)
        if lane_id in lanes_to_close:
            # Check if the current lane has more than one lane available
            num_lanes = traci.edge.getLaneNumber(lane_id.split("_")[0])
            if num_lanes > 1:
                traci.vehicle.changeLane(veh_id, 1, 10)  # Move vehicle to the adjacent lane in 10 seconds
            else:
                print(f"No adjacent lane available for vehicle {veh_id} on lane {lane_id}.")

def read_osmids_from_csv(file_path):
    """Reads osmids from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
        print(f"Successfully read CSV file: {file_path}")
        return df['osmids'].astype(str).tolist()  # Change to match the column name in your CSV
    except Exception as e:
        print(f"Error reading CSV file: {file_path}")
        print(f"Exception: {e}")
        return []

def get_lane_ids_from_osmids(osmids):
    """Finds all lane IDs in SUMO corresponding to the given osmids, handling forward, reverse, and internal lanes."""
    lane_ids_to_close = []

    for osmid in osmids:
        forward_edge = osmid
        reverse_edge = f"-{osmid}"  # Reverse edge ID is prefixed with '-'

        # Check and add forward lanes
        if forward_edge in traci.edge.getIDList():
            num_lanes = traci.edge.getLaneNumber(forward_edge)
            for lane_index in range(num_lanes):
                lane_id = f"{forward_edge}_{lane_index}"
                lane_ids_to_close.append(lane_id)

        # Check and add reverse lanes
        if reverse_edge in traci.edge.getIDList():
            num_lanes = traci.edge.getLaneNumber(reverse_edge)
            for lane_index in range(num_lanes):
                lane_id = f"{reverse_edge}_{lane_index}"
                lane_ids_to_close.append(lane_id)

        # Check for internal edges related to this OSM ID (both forward and reverse)
        for edge in traci.edge.getIDList():
            if forward_edge in edge or reverse_edge in edge:
                num_lanes = traci.edge.getLaneNumber(edge)
                for lane_index in range(num_lanes):
                    lane_id = f"{edge}_{lane_index}"
                    lane_ids_to_close.append(lane_id)

    return lane_ids_to_close

def parse_tripinfo(tripinfo_file, output_csv_path):
    """Parse the tripinfo.xml file and save the data to a CSV."""
    import xml.etree.ElementTree as ET

    tree = ET.parse(tripinfo_file)
    root = tree.getroot()

    data = []
    for trip in root.findall('tripinfo'):
        vehicle_id = trip.attrib['id']
        duration = float(trip.attrib['duration'])
        departure_time = float(trip.attrib['depart'])
        arrival_time = departure_time + duration  # Calculate arrival time

        data.append({
            'vehicle_id': vehicle_id,
            'duration': duration,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False)
    print(f"Trip information saved to {output_csv_path}")

def run():
    step = 0
    closure_step = 1000  # Close lanes after 1000 steps
    max_simulation_time = 1500  # Set maximum simulation time (in steps)
    trip_data_before_closure = []  # Store trip data before closure

    # Read osmids from the CSV file
    osmids_from_csv = read_osmids_from_csv("Wilmington_drive_flood_status_flooded_threshold_2.csv")

    # Check if the osmids list is empty
    if not osmids_from_csv:
        print("No osmids found in the CSV file. Exiting simulation.")
        return

    # Get lane IDs from OSM IDs found in the CSV
    lanes_to_close = get_lane_ids_from_osmids(osmids_from_csv)

    print(f"Lanes to close: {lanes_to_close}")

    while traci.simulation.getMinExpectedNumber() > 0 and step < max_simulation_time:
        traci.simulationStep()  # Advance the simulation by one step

        # Collect trip data before lane closure
        if step < closure_step:
            for veh_id in traci.vehicle.getIDList():
                vehicle_info = {
                    'vehicle_id': veh_id,
                    'departure_time': traci.vehicle.getDeparture(veh_id),  # Get departure time
                    'waiting_time': traci.vehicle.getAccumulatedWaitingTime(veh_id)  # Get accumulated waiting time
                }
                trip_data_before_closure.append(vehicle_info)

        # Print the current number of vehicles and step
        print(f"Step {step}: {traci.simulation.getMinExpectedNumber()} vehicles left in the simulation.")

        # Close lanes after 'closure_step' simulation steps
        if step == closure_step:
            for lane in lanes_to_close:
                traci.lane.setAllowed(lane, [])  # Disallow vehicles from these lanes
                print(f"Closed lane: {lane} at step {step}")

            # Reroute vehicles already on the closed lanes
            reroute_vehicles_on_closed_lanes(lanes_to_close)

        # Continue rerouting vehicles on closed lanes in subsequent steps
        if step > closure_step:
            reroute_vehicles_on_closed_lanes(lanes_to_close)

        step += 1

    # Save trip data before closure to CSV
    before_closure_df = pd.DataFrame(trip_data_before_closure)
    before_closure_output_path = os.path.join(os.getcwd(), 'tripinfo_before_closure.csv')
    before_closure_df.to_csv(before_closure_output_path, index=False)
    print(f"Trip information before lane closure saved to {before_closure_output_path}")
    
    
    traci.close()  # Close the simulation
    #sys.stdout.flush()

if __name__ == "__main__":
    options = get_options()

    # Use SUMO GUI if not running in command-line mode
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # Path to your SUMO configuration file
    config_file = r"C:\Users\tasni\2024-09-05-12-40-58\TASNIA1.sumocfg"

    # Check if the config file exists
    if not os.path.exists(config_file):
        print(f"Configuration file path: {config_file}")
        sys.exit(f"Error: Configuration file '{config_file}' not found!")

    print(f"Starting SUMO with config file: {config_file}")

    try:
        # Start the SUMO simulation with the given config file
        traci.start([sumoBinary, "-c", config_file,
                     "--step-length", "0.5",  # Increase step length for faster simulation
                     "--tripinfo-output", "tripinfo.xml",
                     "--statistic-output", "vehStatistic.xml"])
        print("SUMO started successfully!")
        run()
        # Parse tripinfo.xml after simulation ends
        parse_tripinfo("tripinfo.xml", os.path.join(os.getcwd(), 'tripinfo_after_closure.csv'))
        print(f"Trip information after lane closure saved to {'tripinfo_after_closure.csv'}")
    

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Traceback:", traceback.format_exc())
