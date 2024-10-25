import pandas as pd
import os

TRIP_ID = 0
TRIP_DURATION = 1
START_STATION_ID = 2
END_STATION_ID = 5

def count_monthly_trips(year="2024"):
    """
    Count the total number of trips for each month in the specified year.
    
    Parameters:
    year (str): Year folder to analyze (default: "2024")
    
    Returns:
    pandas.Series: Monthly trip counts indexed by filename
    """
    # Construct the folder path
    folder_path = os.path.join(".", "data", year)
    
    # Verify the path exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Could not find directory: {folder_path}")
    
    # Dictionary to store results
    monthly_counts = {}
    
    # Debug: Print the full folder path
    print(f"Looking for CSV files in: {os.path.abspath(folder_path)}")
    
    # Loop through all files in the folder
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.csv'):
            # Create full file path
            file_path = os.path.join(folder_path, filename)
            
            try:
                # First try reading with utf-8
                try:
                    df = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    # If utf-8 fails, try with cp1252 (Windows-1252)
                    df = pd.read_csv(file_path, encoding='cp1252')
                
                trip_count = len(df)
                
                # Extract month number from filename
                month = filename.split('-')[1].split('.')[0]
                
                # Store the count with a cleaned up month name
                monthly_counts[f"Month {month} Year {year}"] = trip_count
                print(f"Successfully read month {month}: {trip_count:,} trips")
                
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
    
    if not monthly_counts:
        print("No CSV files were found or could be read.")
        return pd.Series()
    
    # Convert to pandas Series and sort by month
    return pd.Series(monthly_counts).sort_index()


def count_single_month(file_name = "./data/2024/Bike share ridership 2024-01.csv"):
    df = pd.read_csv(file_name)
    trip_count = len(df)
    series_to_return = {}
    series_to_return[file_name] = trip_count
    return pd.Series(series_to_return)

def count_trips_from_specific_station(station_id: str) -> int:
    """Counts the number of trips which either end 
    or start at the specified station
    """
    #This sets the file to look at
    file_path = './data/2024/Bike share ridership 2024-09.csv'
    df = ''
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        # If utf-8 fails, try with cp1252 (Windows-1252)
        df = pd.read_csv(file_path, encoding='cp1252')

    starts_at_station = df['Start Station Id'] == station_id
    ends_at_station = df['End Station Id'] == station_id

    stats = {
        'total_trips': (starts_at_station | ends_at_station).sum(),
        'trips_starting': starts_at_station.sum(),
        'trips_ending': ends_at_station.sum()
    }

    station_name = df[starts_at_station | ends_at_station]['Start Station Name'].iloc[0] if starts_at_station.any() else "Unknown"
    
    print(f"\nAnalysis for Station {station_id} ({station_name}):")
    print(f"Total trips: {stats['total_trips']:,}")
    print(f"Trips starting at station: {stats['trips_starting']:,}")
    print(f"Trips ending at station: {stats['trips_ending']:,}")
    
    # Most common destinations for trips starting at this station
    if starts_at_station.any():
        print("\nTop 5 destinations from this station:")
        top_destinations = (df[starts_at_station]
                          .groupby('End Station Name')
                          .size()
                          .sort_values(ascending=False)
                          .head())
        for station, count in top_destinations.items():
            print(f"{station}: {count:,} trips")
    
    return stats

    
    


# folder_path = "data/2024"  # Replace with your actual folder path
# print(count_monthly_trips())
# print(count_single_month())
if __name__ == "__main__":

    # full_df = {}

    # for i in range(2019, 2025):
    #     full_df[i] = count_monthly_trips(str(i))
    #     # print(count_monthly_trips(str(i)))
    # print(full_df)
    print(count_trips_from_specific_station(7041))