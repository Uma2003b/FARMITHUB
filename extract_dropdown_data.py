import pandas as pd
import json

# Load the dataset
df = pd.read_csv('Crop_Yield_Prediction/Datasets/crop_yield.csv')

# Extract unique values
unique_crops = sorted(df['Crop'].unique().tolist())
unique_seasons = sorted(df['Season'].str.strip().unique().tolist())
unique_states = sorted(df['State'].unique().tolist())

print("Unique Crops:")
print(json.dumps(unique_crops, indent=2))
print(f"\nTotal Crops: {len(unique_crops)}")

print("\nUnique Seasons:")
print(json.dumps(unique_seasons, indent=2))
print(f"\nTotal Seasons: {len(unique_seasons)}")

print("\nUnique States:")
print(json.dumps(unique_states, indent=2))
print(f"\nTotal States: {len(unique_states)}")

# Save to files for easy access
with open('crops_list.json', 'w') as f:
    json.dump(unique_crops, f, indent=2)

with open('seasons_list.json', 'w') as f:
    json.dump(unique_seasons, f, indent=2)

with open('states_list.json', 'w') as f:
    json.dump(unique_states, f, indent=2)

print("\nData saved to JSON files!")