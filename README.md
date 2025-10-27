# Activity-Classification
**Overview**
This Python script processes an OCEL (Object-Centric Event Log) to extract and analyze event-to-object relationships. The script works as follows:
- It reads the OCEL log and displays a list of object types present in the log.
- The user selects a pair of object types (t1, t2).
- The system iterates through all combinations of objects from both types (t1 and t2), and retrieves events and associated activities where both object types are involved.
- The result will consist of multiple lists for multiple object pairs (o1, o2), showing event and associated activities for each pair of objects.

The script also:
- Classifies activities as `CREATE`, `DELETE`, or `MAINTAIN` based on their occurrence in event sequences.
- Tracks and displays the execution time of the script.
Prerequisites
To run this script, ensure you have the following dependencies installed:
- Python 3.x
- pm4py (for reading and processing OCEL logs)
- pandas (for handling data manipulation)

You can install the dependencies using pip:
```bash
pip install pm4py pandas
```
Usage
### 1. Input File
The script expects an OCEL log in XML format. The default file is `ContainerLogistics.xml`, but you can modify the `filename` variable in the script to use a different file.

### 2. Running the Script
To run the script, execute it from the command line:
```bash
python activityClasification.py
```

### 3. User Input
The system will prompt you to select a pair of object types from the list of available object types found in the OCEL log. You will then input the selected pair, and the system will analyze the events and activities related to those object types.

Example output:
```
Available Object Types in OCEL: ['Container', 'Truck', 'Vehicle']
Enter the first object type: Container
Enter the second object type: Truck
```

### 4. Output
The script will output the following:
- A list of events and activities involving the two specified object types.
- A classification of activities as `CREATE`, `DELETE`, or `MAINTAIN` based on their occurrence in the event sequence.
- The total execution time of the script.

### 5. Customization
You can modify the `filename` variable to point to your desired OCEL XML file.
Functions
### `load_ocel_log(filename)`
- Loads the OCEL log from the specified XML file.

### `get_activities_and_object_types(ocel)`
- Extracts and prints the unique activities and object types from the OCEL log.

### `get_object_type_pair()`
- Prompts the user to input two object types for analysis, selected from the list of available object types in the OCEL log.

### `process_event_object_relations(ocel)`
- Processes the event-to-object relationships and returns a DataFrame containing the relationship data.

### `get_events_for_object_pair(object_id1, object_id2, relations, ocel)`
- Finds events and associated activities involving a given pair of object IDs.

### `get_events_for_object_type_pair(object_type1, object_type2, relations, ocel)`
- Finds events and activities involving pairs of objects from two given object types.

### `classify_activities(events_activities)`
- Classifies activities as `CREATE`, `DELETE`, or `MAINTAIN` based on their occurrence in event sequences.
Example Output
```
Available Object Types in OCEL: ['Container', 'Truck', 'Vehicle']
Enter the first object type: Container
Enter the second object type: Truck

Events and activities involving both object types 'Container' and 'Truck':
[('e1', 'Load', 'Truck', 'Container'), ('e2', 'Transport', 'Truck', 'Container')]

Activity Labels:
Activity: Load, Labels: {'CREATE'}
Activity: Transport, Labels: {'MAINTAIN'}
Activity: Unload, Labels: {'DELETE'}

Time taken for execution: 2.45 seconds
```
License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
Acknowledgments
- This project uses the [PM4Py](https://pm4py.fit.fraunhofer.de/) library for working with OCEL logs.
- Pandas is used for data manipulation and processing.
