#include <bits/stdc++.h>
using namespace std;

#define MAX_SIZE 1000 // size of the character array i am using to manipulate the strings while using sprintf

class Vehicle
{
    protected:
        int vehicleID;
        double VehiclePrice, RentalPricing;
        string brand;

    public:
        Vehicle(int vehicleID, string brand, double VehiclePrice, double RentalPricing) : vehicleID(vehicleID), brand(brand), VehiclePrice(VehiclePrice), RentalPricing(RentalPricing) {}
        
        // Getters:
        int getVehicleID() {return vehicleID;}
        string getBrand() {return brand;}
        double getVehiclePrice() {return VehiclePrice;}
        double getRentalPricing() {return RentalPricing;}

};

class Car : public Vehicle
{
    protected:
        string Type, fuel, transmStringStreamion;

    public:
    // Constructor
    Car(int vehicleID, string brand, double VehiclePrice, double RentalPricing, string Type, string fuel, string transmStringStreamion)
        : Vehicle(vehicleID, brand, VehiclePrice, RentalPricing), Type(Type), fuel(fuel), transmStringStreamion(transmStringStreamion) {}
};

class Truck : public Vehicle
{
    protected:
        int NumberOfAxels;
        double CargoCapacity, BedLegth, FuelEfficiency;

    public:
        Truck(int vehicleID, string brand, double VehiclePrice, double RentalPricing, int NumberOfAxels, double CargoCapacity, double BedLegth, double FuelEfficiency)
            : Vehicle(vehicleID, brand, VehiclePrice, RentalPricing),
            NumberOfAxels(NumberOfAxels), CargoCapacity(CargoCapacity),
             BedLegth(BedLegth), FuelEfficiency(FuelEfficiency) {}
};

class Bicycle : public Vehicle
{
    protected:
        int NumberOfGears;
        string Type, frame;

    public:
        Bicycle(int vehicleID, string brand, double VehiclePrice, double RentalPricing, string Type, string frame)
            : Vehicle(vehicleID, brand, VehiclePrice, RentalPricing), Type(Type), frame(frame) {}
};

class Drone : public Vehicle
{
    protected:
        int CameraResolution;
        double FlyTime, maxAlt;

    public:
        Drone(int vehicleID, string brand, double VehiclePrice, double RentalPricing, int CameraResolution, double FlyTime, double maxAlt)
            : Vehicle(vehicleID, brand, VehiclePrice, RentalPricing), CameraResolution(CameraResolution), FlyTime(FlyTime), maxAlt(maxAlt) {}
};

class VehicleFleetManager // keeps track of the vehicles in VehicleFleetManager
{
    private:
        vector<Vehicle *> vehicles; // list of vehicles
        double totalValue = 0;
        double totalCapacity = 0;

    public:
        void addVehicle(Vehicle *vehicle)
        {
            vehicles.push_back(vehicle);
            totalValue += vehicle->getVehiclePrice(); // updating total value in VehicleFleetManager
        }

        void updateCapacity(double CargoCapacity) {totalCapacity += CargoCapacity;}

        string VehicleFleetManagerStatistics()
        {
            char Buffer[MAX_SIZE]; // Adjust the Buffer size accordingly

            sprintf(Buffer, "Total Value of All Vehicles: %.2f\n", totalValue);
            string ret(Buffer);

            sprintf(Buffer, "Total Cargo Capacity of Trucks: %.2f kg\n", totalCapacity);
            ret += Buffer;

            return ret;
        }
        vector<Vehicle *> getListOfVehicles(){return vehicles;}
    
};

class Rent;

class Customer
{
    private:
        static int i;
        int customerID;
        vector<Rent *> rentalHistory;

    public:
        Customer() {this->customerID = i++;}
        int getID() {return customerID;}
        void RentingRent(Rent *obj) {rentalHistory.push_back(obj);}
        vector<Rent *> getRentalLog() {return rentalHistory;}
    };
    int Customer::i = 1;

    class Rent
    {
    private:
        Customer *c;
        Vehicle *v;
        int duration;
        double rentalFare;

    public:
        // Constructors:
        Rent(Customer *custid, Vehicle *vehicleid, int duration)
        {
            this->c = custid;
            this->v = vehicleid;
            this->duration = duration;
            this->rentalFare = (duration * v->getRentalPricing());
        }

        // Getters
        int getVehicleID() {return v->getVehicleID();}
        int getCustomerID() {return c->getID();}
        int getDuration() {return duration;}
        double getRentalFare(){return rentalFare;}
        string getResponse()
        {
            char Buffer[200];

            //formating the string
            sprintf(Buffer, "Vehicle %d Rented for %d days by customer %d. Rental Cost: %d\n",
                    this->getVehicleID(), this->getDuration(), this->getCustomerID(), (int)(this->getRentalFare()));
            string resp(Buffer);
            return resp;
        }
};

class CustomerManager
{
    private:
        vector<Customer *> list; // list of customers

    public:

        // Method to Add Customer
        string addCustomer()
        {
            Customer *obj = new Customer();
            list.push_back(obj);
            return ("Customer " + to_string(obj->getID()) + " added\n");
        }

        Customer *GetCustomer(int customerID)
        {
            for (auto x : list){ if (x->getID() == customerID) return x; };
            return NULL;
        }

        Vehicle *GetVehicle(int vehicleID, VehicleFleetManager &VehicleFleetManager)
        {
            for (auto x : VehicleFleetManager.getListOfVehicles())
            {
                if (x->getVehicleID() == vehicleID)
                    return x;
            };
            return NULL;
        }

        string RentingVehicle(int customerID, int vehicleID, int duration, VehicleFleetManager &VehicleFleetManager) 
        {
            Customer *custObj = GetCustomer(customerID);
            Vehicle *vehicleObj = GetVehicle(vehicleID, VehicleFleetManager);
            if (custObj != NULL && vehicleObj != NULL )
            {
                Rent *rentObj = new Rent(custObj, vehicleObj, duration);
                custObj->RentingRent(rentObj);
                return rentObj->getResponse(); // return the renting info
            } 
            return "";
        }

        // Getters:
        string getCustomerHistory(int customerID, VehicleFleetManager &VehicleFleetManager)
        {
            Customer *custObj = GetCustomer(customerID);
            if (custObj != NULL)
            {
                char Buffer[MAX_SIZE];

                //formating the string
                sprintf(Buffer, "Customer %d Rental History:\n", customerID);
                string returned(Buffer);
                // Iterating through the array to get Each Vehicle.
                for (auto x : custObj->getRentalLog())
                {
                    sprintf(Buffer, "- Vehicle ID: %d, Brand: %s, Rental Duration: %d days, Rental Cost: %d\n",
                            x->getVehicleID(), GetVehicle(x->getVehicleID(), VehicleFleetManager)->getBrand().c_str(),
                            x->getDuration(), (int)(x->getRentalFare()));
                    returned += Buffer;
                }
                return returned;
            }
            return "";
        }
};

void showResponses(vector <string> &AnswerArray){
     for (auto x: AnswerArray) cout << x;
}

int main()
{
    string temp; // to handle random strings that I Get difficult to name
    vector<string> AnswerArray;
    setprecision(2);

    VehicleFleetManager VehicleFleetManager;
    CustomerManager cm;

    string line;

    while (true)
    {
        getline(cin >> ws, line);

        if (line[0] == 'E'){break;}
        
        istringstream StringStream(line);  // Parsing
        string command;
        StringStream >> command;

        if (command == "ADD_VEHICLE")
        {
            Vehicle *obj;
            string vehicleCode; StringStream >> vehicleCode; StringStream >> temp; int vehicleID = stoi(temp);
            string brand; StringStream >> brand; StringStream >> temp;
            double VehiclePrice = stod(temp); StringStream >> temp; double RentalPricing = stod(temp);
            if (vehicleCode == "c")
            {
                string Type, fuel, transmStringStreamion;
                StringStream >> Type >> fuel >> transmStringStreamion;
                obj = new Car(vehicleID, brand, VehiclePrice, RentalPricing, Type, fuel, transmStringStreamion);
                char Buffer[MAX_SIZE]; // Adjust the Buffer size accordingly
                sprintf(Buffer, "Car - ID: %d, Brand: %s, Price: %.2f, Rental Cost: %d/day, Type: %s, Fuel: %s, Transmission: %s\n",
                        vehicleID, brand.c_str(), VehiclePrice, (int)(RentalPricing), Type.c_str(), fuel.c_str(), transmStringStreamion.c_str());
                AnswerArray.push_back(Buffer);
            }
            else if (vehicleCode == "t")
            {
                double CargoCapacity, BedLegth, FuelEfficiency;
                int NumberOfAxels; StringStream >> temp; 
                CargoCapacity = stod(temp); StringStream >> temp; 
                BedLegth = stod(temp); StringStream >> temp; 
                NumberOfAxels = stoi(temp); StringStream >> temp; 
                FuelEfficiency = stod(temp);
                obj = new Truck(vehicleID, brand, VehiclePrice, RentalPricing, NumberOfAxels, CargoCapacity, BedLegth, FuelEfficiency);
                char Buffer[MAX_SIZE];
                sprintf(Buffer, "Truck - ID: %d, Brand: %s, Price: %.2f, Rental Cost: %d/day, Cargo  Capacity: %.2f kg, Bed Length: %.2f m, Axles: %d, Mileage: %.2f miles/gallon\n",
                        vehicleID, brand.c_str(), VehiclePrice, (int)(RentalPricing), CargoCapacity, BedLegth, NumberOfAxels, FuelEfficiency);
                AnswerArray.push_back(Buffer);
                VehicleFleetManager.updateCapacity(CargoCapacity); // update the CargoCapacity capacity in VehicleFleetManager
            }
            else if (vehicleCode == "b")
            {
                string Type, frame;
                int NumberOfGears;
                StringStream >> Type;
                StringStream >> frame;
                StringStream >> temp;
                if (temp == "Fibre")
                    frame += (" " + temp);
                StringStream >> temp;
                NumberOfGears = stoi(temp);
                obj = new Bicycle(vehicleID, brand, VehiclePrice, RentalPricing, Type, frame);
                char Buffer[MAX_SIZE];
                sprintf(Buffer, "Bicycle - ID: %d, Brand: %s, Price: %.2f, Rental Cost: %d/day, Type: %s, Frame: %s, Gears: %d\n",
                        vehicleID, brand.c_str(), VehiclePrice, (int)(RentalPricing), Type.c_str(), frame.c_str(), NumberOfGears);
                AnswerArray.push_back(Buffer);
            }

            else if (vehicleCode == "d")
            {
                double maxAlt, FlyTime;
                int CameraResolutionolution; StringStream >> temp;
                maxAlt = stod(temp); StringStream >> temp;
                FlyTime = stod(temp); StringStream >> temp;
                CameraResolutionolution = stoi(temp);
                obj = new Drone(vehicleID, brand, VehiclePrice, RentalPricing, CameraResolutionolution, FlyTime, maxAlt);
                char Buffer[MAX_SIZE]; 

                // Using sprintf to format the string
                sprintf(Buffer, "Drone - ID: %d, Brand: %s, Price: %.2f, Rental Cost: %d/day, Max Altitude: %.2f m, Flight time: %.2f min, Camera Resolution: %d MP\n",
                        vehicleID, brand.c_str(), VehiclePrice, (int)(RentalPricing), maxAlt, FlyTime, CameraResolutionolution);

                
                AnswerArray.push_back(Buffer);
            }

            VehicleFleetManager.addVehicle(obj);
        }
        else if (command == "ADD_CUSTOMER")
        {
            AnswerArray.push_back(cm.addCustomer());
        }
        else if (command == "RENT")
        {
            int customerID, vehicleID, duration; // duration in days
            StringStream >> temp;
            customerID = stoi(temp);
            StringStream >> temp;
            vehicleID = stoi(temp);
            StringStream >> temp;
            duration = stoi(temp);
            string resp = cm.RentingVehicle(customerID, vehicleID, duration, VehicleFleetManager);
            if (resp != "")
                AnswerArray.push_back(resp);
        }
        else if (command == "FLEET_STATISTICS")
        {
            AnswerArray.push_back(VehicleFleetManager.VehicleFleetManagerStatistics());
        }
        else if (command == "CUSTOMER_HISTORY")
        {
            StringStream >> temp;
            int customerID = stoi(temp);
            AnswerArray.push_back(cm.getCustomerHistory(customerID, VehicleFleetManager));
        }
    }
    showResponses(AnswerArray);

    return 0;
}
