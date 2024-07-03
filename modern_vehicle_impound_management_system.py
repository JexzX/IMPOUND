import json
from datetime import datetime, timedelta

class Vehicle:
    def __init__(self, vehicle_type, plate_number, reason, impound_duration, timestamp=None, expiry_date=None):
        self.vehicle_type = vehicle_type
        self.plate_number = plate_number
        self.reason = reason
        self.impound_duration = impound_duration
        self.timestamp = timestamp if timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.expiry_date = expiry_date
        self.calculate_expiry_date()

    def calculate_expiry_date(self):
        if 'd' in self.impound_duration:
            days = int(self.impound_duration.split()[0])
            self.expiry_date = (datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S") + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        elif 'w' in self.impound_duration:
            weeks = int(self.impound_duration.split()[0])
            self.expiry_date = (datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S") + timedelta(weeks=weeks)).strftime("%Y-%m-%d %H:%M:%S")
        elif 'm' in self.impound_duration:
            months = int(self.impound_duration.split()[0])
            self.expiry_date = (datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S") + timedelta(days=30*months)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.expiry_date = None

    def is_expired(self):
        now = datetime.now()
        return now > datetime.strptime(self.expiry_date, "%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return (f"\nVehicle Type    : {self.vehicle_type}\n"
                f"Plate Number    : {self.plate_number}\n"
                f"Reason          : {self.reason}\n"
                f"Impound Duration: {self.impound_duration}\n"
                f"Timestamp       : {self.timestamp}\n"
                f"Expiry Date     : {self.expiry_date}\n"
                f"Expired         : {'Yes' if self.is_expired() else 'No'}\n"
                f"{'-'*40}")

    def to_dict(self):
        return {
            "vehicle_type": self.vehicle_type,
            "plate_number": self.plate_number,
            "reason": self.reason,
            "impound_duration": self.impound_duration,
            "timestamp": self.timestamp,
            "expiry_date": self.expiry_date
        }

class ImpoundSystem:
    def __init__(self):
        self.vehicles = []
        self.load_vehicles()

    def load_vehicles(self):
        try:
            with open('vehicles.json', 'r') as file:
                data = json.load(file)
                self.vehicles = [Vehicle(**v) for v in data["vehicles"]]
        except FileNotFoundError:
            print("File 'vehicles.json' not found. Initializing with an empty list of vehicles.")
            self.vehicles = []

    def save_vehicles(self):
        with open('vehicles.json', 'w') as file:
            json.dump({"vehicles": [v.to_dict() for v in self.vehicles]}, file, indent=4)

    def add_vehicle(self, vehicle_type, plate_number, reason, impound_duration):
        vehicle = Vehicle(vehicle_type, plate_number, reason, impound_duration)
        self.vehicles.append(vehicle)
        print(f"\nVehicle added to the impound system:")
        print(vehicle)
        self.save_vehicles()

    def list_vehicles(self):
        if not self.vehicles:
            print("\nNo vehicles in the impound system.")
        else:
            print("\nList of Vehicles in the Impound System:")
            for vehicle in self.vehicles:
                print(vehicle)

    def remove_vehicle(self, plate_number):
        removed = False
        for vehicle in self.vehicles:
            if vehicle.plate_number == plate_number:
                self.vehicles.remove(vehicle)
                print("\nVehicle removed from the impound system.")
                removed = True
                break
        if not removed:
            print("\nVehicle not found in the impound system.")
        self.save_vehicles()

    def search_vehicle(self, plate_number):
        found = False
        for vehicle in self.vehicles:
            if vehicle.plate_number == plate_number:
                print(f"\nFound Vehicle:")
                print(vehicle)
                found = True
                break
        if not found:
            print("\nVehicle not found in the impound system.")

    def search_vehicle_by_reason(self, reason):
        found = False
        for vehicle in self.vehicles:
            if vehicle.reason.lower() == reason.lower():
                if not found:
                    print("\nVehicles with Reason:")
                print(vehicle)
                found = True
        if not found:
            print(f"\nNo vehicles found with reason '{reason}'.")

    def check_expirations(self):
        expired_vehicles = [vehicle for vehicle in self.vehicles if vehicle.is_expired()]
        if expired_vehicles:
            print("\nExpired Vehicles:")
            for vehicle in expired_vehicles:
                print(vehicle)
        else:
            print("\nNo vehicles have expired.")

def main():
    system = ImpoundSystem()
    while True:
        print("\nImpound System Menu")
        print("1. List Vehicles")
        print("2. Add Vehicle")
        print("3. Remove Vehicle")
        print("4. Search Vehicle by Plate Number")
        print("5. Search Vehicle by Reason")
        print("6. Check Expired Vehicles")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            system.list_vehicles()
        
        elif choice == '2':
            vehicle_type = input("\nEnter vehicle type: ")
            plate_number = input("Enter plate number: ")
            reason = input("Enter reason for impound: ")
            impound_duration = input("Enter impound duration (e.g., 3 days, 1 week, 2 months): ")
            system.add_vehicle(vehicle_type, plate_number, reason, impound_duration)
        
        elif choice == '3':
            plate_number = input("\nEnter plate number to remove: ")
            system.remove_vehicle(plate_number)
        
        elif choice == '4':
            plate_number = input("\nEnter plate number to search: ")
            system.search_vehicle(plate_number)
        
        elif choice == '5':
            reason = input("\nEnter reason to search: ")
            system.search_vehicle_by_reason(reason)
        
        elif choice == '6':
            system.check_expirations()
        
        elif choice == '7':
            print("\nExiting the system. Goodbye!")
            break
        
        else:
            print("\nInvalid choice, please try again.")

if __name__ == "__main__":
    main()
