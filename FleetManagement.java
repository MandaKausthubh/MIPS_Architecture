import java.util.*;

// Class to manage vehicles and customers
class VehicleManagement{
    // Lists to store vehicles and customers
    private ArrayList<Vehicle>vehicles = new ArrayList<>();
    private ArrayList<Customer>customers = new ArrayList<>();

    // Method to add a vehicle to the list
    public void add_vehicle(Vehicle vehicle){
        vehicles.add(vehicle);
    }

    // Method to add a customer to the list
    public void add_customer(Customer customer){
        customers.add(customer);
    }//yo
    
    // Method to display fleet statistics
    public void fleet_statistics(){
        double total_value=0;
        double total_CargoCapacity=0;

        // Loop through each vehicle to calculate total value and CargoCapacity capacity for trucks
        for(Vehicle vehicle:vehicles){
            if(vehicle instanceof Truck){
                Truck truck = (Truck)vehicle;
                total_CargoCapacity+=truck.getCargoCapacity_capacity();
            }
            total_value+=vehicle.getVehiclePrice();
        }

        // Format and display the results
        String formattedValue = String.format("%.2f", total_value);
        String formattedCargoCapacity = String.format("%.2f", total_CargoCapacity);
        System.out.println("Total Value of All Vehicles: "+formattedValue);
        System.out.println("Total CargoCapacity Capacity of Trucks: "+formattedCargoCapacity+" kg");
    }

    // Method for vehicle rental
    public void vehicle_rental(int custom_id, int veh_id, int duration){
        // Loop through customers to Get the specific customer
        for(Customer customer:customers){
            if(customer.getCustomerID()==custom_id){
                // Loop through vehicles to Get the specific vehicle
                for(Vehicle vehicle:vehicles){
                    if(vehicle.getVehicleID()==veh_id){
                        String brand=vehicle.getBrand();
                        int rental_cost=(int)vehicle.getRental_cost();
                        rental_cost=rental_cost*duration;
                        // Create a rental transaction and add it to the customer's transactions
                        RentalTransaction transaction = new RentalTransaction(veh_id, duration,brand,rental_cost);
                        customer.add_transaction(transaction);
                        System.out.println("Vehicle "+veh_id+" Rented for "+duration+" days by customer "+custom_id+". Rental Cost: "+rental_cost);
                        break;
                    }
                }
                break;
            }
        }
    }

    // Method to display rental history for a customer
    public void customer_history(int id){
        for(Customer customer:customers){
            if(customer.getCustomerID()==id){
                customer.rental_history();
                break;
            }
        }
    }
}

// Class to represent a rental transaction
class RentalTransaction{
    public int veh_id;
    public int duration;
    public String brand;
    public int rental_cost;

    // Constructor for the rental transaction
    public RentalTransaction(int veh_id, int duration,String brand,int rental_cost) {
        this.brand = brand;
        this.veh_id = veh_id;
        this.duration = duration;
        this.rental_cost=rental_cost;
    }

    // Getter methods for transaction details
    public String getBrand() {
        return brand;
    }
    public int getVeh_id() {
        return veh_id;
    }
    public int getDuration() {
        return duration;
    }
    public int getRentalCost() {
        return rental_cost;
    }
}

// Base class representing a vehicle
class Vehicle{
    protected int vehicleID;
    protected String brand;
    protected double VehiclePrice;
    protected double rental_cost;

    // Constructor for the vehicle
    public Vehicle(int id,String b,double pr,double rental){
        vehicleID=id;
        brand=b;
        VehiclePrice=pr;
        rental_cost=rental;
    }

    // Getter methods for vehicle details
    public int getVehicleID() {
        return vehicleID;
    }
    public String getBrand() {
        return brand;
    }
    public double getVehiclePrice() {
        return VehiclePrice;
    }
    public double getRental_cost() {
        return rental_cost;
    }

    // Display method to print vehicle details
    public void display(){
        String formattedValue = String.format("%.2f", VehiclePrice);
        System.out.print("ID: "+vehicleID+", Brand: "+brand+", VehiclePrice: "+formattedValue+", Rental Cost: "+(int)rental_cost+"/day, ");
    }
}

// Class representing a car, inherits from Vehicle
class Car extends Vehicle{
    private String Type;
    private String fuel;
    private String transmStringStreamion;

    // Constructor for the car
    public Car( int id,String b,double pr,double rental,String ty,String fu,String tr){
        super(id,b,pr,rental);
        Type=ty;
        fuel=fu;
        transmStringStreamion=tr;
    }

    // Getter methods for car details
    public String getType() {
        return Type;
    }
    public String getFuel() {
        return fuel;
    }
    public String getTransmStringStreamion() {
        return transmStringStreamion;
    }

    // Display method to print car details
    public void display(){
        System.out.print("Car - ");
        super.display();
        System.out.print("Type: "+Type+", Fuel: "+fuel+", ");
        System.out.println("TransmStringStreamion: "+transmStringStreamion);
    }
}

// Class representing a truck, inherits from Vehicle
class Truck extends Vehicle{
    private double CargoCapacity_capacity;
    private double bed_length;
    private int num_axles;
    private double fuel_efficiency;

    // Constructor for the truck
    public Truck( int id,String b,double pr,double rental,double ca,double bed,int num,double fuel){
        super(id,b,pr,rental);
        CargoCapacity_capacity=ca;
        bed_length=bed;
        num_axles=num;
        fuel_efficiency=fuel;
    }

    // Getter methods for truck details
    public double getCargoCapacity_capacity() {
        return CargoCapacity_capacity;
    }
    public double getBed_length() {
        return bed_length;
    }
    public int getNum_axles() {
        return num_axles;
    }
    public double getFuel_efficiency() {
        return fuel_efficiency;
    }

    // Display method to print truck details
    public void display(){
        System.out.print("Truck - ");
        super.display();
        String formattedVal = String.format("%.2f", CargoCapacity_capacity);
        String formattedBedLength = String.format("%.2f", bed_length);
        String formattedMileage = String.format("%.2f", fuel_efficiency);
        System.out.print("CargoCapacity capacity: "+formattedVal+" kg, Bed ");
        System.out.println("Length: "+formattedBedLength+" m, Axles: "+num_axles+", Mileage: "+formattedMileage+" miles/gallon");
    }
}

// Class representing a bicycle, inherits from Vehicle
class Bicycle extends Vehicle{
    private String Type;
    private String frame;
    private int num_gears;

    // Constructor for the bicycle
    public Bicycle( int id,String b,double pr,double rental,String ty,String fr,int num){
        super(id,b,pr,rental);
        Type=ty;
        frame=fr;
        num_gears=num;
    }

    // Getter methods for bicycle details
    public String getType() {
        return Type;
    }
    public String getFrame() {
        return frame;
    }
    public int getNum_gears() {
        return num_gears;
    }

    // Display method to print bicycle details
    public void display(){
        System.out.print("Bicycle - ");
        super.display();
        System.out.print("Type: "+Type+", Frame: "+frame+", ");
        System.out.println("Gears: "+num_gears);
    }
}

// Class representing a drone, inherits from Vehicle
class Drone extends Vehicle{
    private double max_altitude;
    private double flying_time;
    private int cam_resolution;

    // Constructor for the drone
    public Drone( int id,String b,double pr,double rental,double max,double fly,int cam){
        super(id,b,pr,rental);
        max_altitude=max;
        flying_time=fly;
        cam_resolution=cam;
    }

    // Getter methods for drone details
    public double getMax_altitude() {
        return max_altitude;
    }
    public double getFlying_time() {
        return flying_time;
    }
    public int getCam_resolution() {
        return cam_resolution;
    }

    // Display method to print drone details
    public void display(){
        System.out.print("Drone - ");
        super.display();
        String formattedMaxAlt = String.format("%.2f", max_altitude);
        String formattedFtime = String.format("%.2f", flying_time);
        System.out.print("Max Altitude: "+formattedMaxAlt+" m, Flight time: ");
        System.out.println(formattedFtime+" min, Camera Resolution: "+cam_resolution+" MP");
    }
}

// Class representing a customer
class Customer{
    private int customerID;
    private ArrayList<RentalTransaction>rented_vehicles = new ArrayList<>();
    
    // Constructor for the customer
    public Customer(int custID) {
        customerID = custID;
    }

    // Getter method for customer ID
    public int getCustomerID() {
        return customerID;
    }
    
    // Display method to print customer addition
    public void display(){
        System.out.println("Customer "+customerID+" added");
    }

    // Method to add a rental transaction to the customer's history
    public void add_transaction(RentalTransaction transaction){
        rented_vehicles.add(transaction);
    }

    // Method to display rental history for a customer
    public void rental_history(){
        System.out.println("Customer "+customerID+" Rental History:");
        for(RentalTransaction transaction:rented_vehicles){
            System.out.println("- Vehicle ID: "+transaction.getVeh_id()+", Brand: "+transaction.getBrand()+", Rental Duration: "+transaction.getDuration()+" days, Rental Cost: "+transaction.getRentalCost());
        }
    }
}

// Main class for Fleet Management
public class FleetManagement{
    public static void main(String args[]){
        Scanner scanner = new Scanner(System.in);
        int cust_id=1;
        VehicleManagement vehicle_management = new VehicleManagement();

        // Loop to take input commands until "END" is entered
        while(true){
            String[] str = scanner.nextLine().split(" ");
            if(str[0].equals("END")){
                break;
            }

            //  add a vehicle
            if(str[0].equals("ADD_VEHICLE")){
                // Check the Type of vehicle and create an object accordingly
                if(str[1].equals("c")){
                    int id=Integer.parseInt(str[2]);
                    String brand=str[3];
                    double VehiclePrice=Double.parseDouble(str[4]);
                    double rental_cost=Double.parseDouble(str[5]);
                    String Type=str[6];
                    String fuel=str[7];
                    String transmStringStreamion=str[8];
                    Vehicle car = new Car(id, brand, VehiclePrice, rental_cost, Type, fuel, transmStringStreamion);
                    Car car1 = (Car)car;
                    car1.display();
                    vehicle_management.add_vehicle(car);
                
                } else if(str[1].equals("t")){
                    int id=Integer.parseInt(str[2]);
                    String brand=str[3];
                    double VehiclePrice=Double.parseDouble(str[4]);
                    double rental_cost=Double.parseDouble(str[5]);
                    double CargoCapacity_capacity=Double.parseDouble(str[6]);
                    double bed_length=Double.parseDouble(str[7]);
                    int num_axles=Integer.parseInt(str[8]);
                    double fuel_efficiency=Double.parseDouble(str[9]);
                    Vehicle truck= new Truck(id, brand, VehiclePrice, rental_cost, CargoCapacity_capacity, bed_length, num_axles, fuel_efficiency);
                    vehicle_management.add_vehicle(truck);
                    Truck truck1 = (Truck)truck;
                    truck1.display();

                } else if(str[1].equals("b")){
                    int id=Integer.parseInt(str[2]);
                    String brand=str[3];
                    double VehiclePrice=Double.parseDouble(str[4]);
                    double rental_cost=Double.parseDouble(str[5]);
                    String Type=str[6];
                    String frame;
                    int num_gears;
                    // Check the frame Type and create an object accordingly
                    if(str[7].equals("Carbon")){
                        frame=str[7]+" "+str[8];
                        num_gears=Integer.parseInt(str[9]);
                    } else {
                        frame=str[7];
                        num_gears=Integer.parseInt(str[8]);
                    }
                    
                    Vehicle bicycle = new Bicycle(id, brand, VehiclePrice, rental_cost, Type, frame, num_gears);
                    vehicle_management.add_vehicle(bicycle);
                    Bicycle bicycle1 = (Bicycle)bicycle;
                    bicycle1.display();
                } else if(str[1].equals("d")){
                    int id=Integer.parseInt(str[2]);
                    String brand=str[3];
                    double VehiclePrice=Double.parseDouble(str[4]);
                    double rental_cost=Double.parseDouble(str[5]);
                    double max_altitude=Double.parseDouble(str[6]);
                    double flying_time=Double.parseDouble(str[7]);
                    int cam_resolution=Integer.parseInt(str[8]);
                    Vehicle drone = new Drone(id, brand, VehiclePrice, rental_cost, max_altitude, flying_time, cam_resolution);
                    vehicle_management.add_vehicle(drone);
                    Drone drone1 = (Drone)drone;
                    drone1.display();
                }
            } 
            //  display fleet statistics
            else if(str[0].equals("FLEET_STATISTICS")){
                vehicle_management.fleet_statistics();
            } 
            //  add a customer
            else if(str[0].equals("ADD_CUSTOMER")){
                Customer customer= new Customer(cust_id);
                vehicle_management.add_customer(customer);
                customer.display();
                cust_id++;
            } 
            //  display rental history for a customer
            else if(str[0].equals("CUSTOMER_HISTORY")){
                int id=Integer.parseInt(str[1]);
                vehicle_management.customer_history(id);
            } 
            // rent a vehicle
            else if(str[0].equals("RENT")){
                int customer_id=Integer.parseInt(str[1]);
                int veh_id=Integer.parseInt(str[2]);
                int duration=Integer.parseInt(str[3]);
                vehicle_management.vehicle_rental(customer_id, veh_id, duration);
            }
        }
    }
}
