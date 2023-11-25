import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Vehicle {
    protected int vehicleID;
    protected double vehiclePrice, rentalPricing;
    protected String brand;

    public Vehicle(int vehicleID, String brand, double vehiclePrice, double rentalPricing) {
        this.vehicleID = vehicleID;
        this.brand = brand;
        this.vehiclePrice = vehiclePrice;
        this.rentalPricing = rentalPricing;
    }

    // Getters:
    public int getVehicleID() {
        return vehicleID;
    }

    public String getBrand() {
        return brand;
    }

    public double getVehiclePrice() {
        return vehiclePrice;
    }

    public double getRentalPricing() {
        return rentalPricing;
    }
}

class Car extends Vehicle {
    protected String type, fuel, transmission;

    public Car(int vehicleID, String brand, double vehiclePrice, double rentalPricing, String type, String fuel, String transmission) {
        super(vehicleID, brand, vehiclePrice, rentalPricing);
        this.type = type;
        this.fuel = fuel;
        this.transmission = transmission;
    }
}

class Truck extends Vehicle {
    protected int numberOfAxels;
    protected double cargoCapacity, bedLength, fuelEfficiency;

    public Truck(int vehicleID, String brand, double vehiclePrice, double rentalPricing, int numberOfAxels, double cargoCapacity, double bedLength, double fuelEfficiency) {
        super(vehicleID, brand, vehiclePrice, rentalPricing);
        this.numberOfAxels = numberOfAxels;
        this.cargoCapacity = cargoCapacity;
        this.bedLength = bedLength;
        this.fuelEfficiency = fuelEfficiency;
    }
}

class Bicycle extends Vehicle {
    protected int numberOfGears;
    protected String type, frame;

    public Bicycle(int vehicleID, String brand, double vehiclePrice, double rentalPricing, String type, String frame) {
        super(vehicleID, brand, vehiclePrice, rentalPricing);
        this.type = type;
        this.frame = frame;
    }
}

class Drone extends Vehicle {
    protected int cameraResolution;
    protected double flyTime, maxAltitude;

    public Drone(int vehicleID, String brand, double vehiclePrice, double rentalPricing, int cameraResolution, double flyTime, double maxAltitude) {
        super(vehicleID, brand, vehiclePrice, rentalPricing);
        this.cameraResolution = cameraResolution;
        this.flyTime = flyTime;
        this.maxAltitude = maxAltitude;
    }
}

class VehicleFleetManager {
    private List<Vehicle> vehicles = new ArrayList<>();
    private double totalValue = 0;
    private double totalCapacity = 0;

    public void addVehicle(Vehicle vehicle) {
        vehicles.add(vehicle);
        totalValue += vehicle.getVehiclePrice();
    }

    public void updateCapacity(double cargoCapacity) {
        totalCapacity += cargoCapacity;
    }

    public String vehicleFleetManagerStatistics() {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("Total Value of All Vehicles: %.2f\n", totalValue));
        sb.append(String.format("Total Cargo Capacity of Trucks: %.2f kg\n", totalCapacity));
        return sb.toString();
    }

    public List<Vehicle> getListOfVehicles() {
        return vehicles;
    }
}

class Customer {
    private static int idCounter = 1;
    private int customerID;
    private List<Rent> rentalHistory = new ArrayList<>();

    public Customer() {
        this.customerID = idCounter++;
    }

    public int getID() {
        return customerID;
    }

    public void rentingRent(Rent obj) {
        rentalHistory.add(obj);
    }

    public List<Rent> getRentalLog() {
        return rentalHistory;
    }
}

class Rent {
    private Customer customer;
    private Vehicle vehicle;
    private int duration;
    private double rentalFare;

    public Rent(Customer custid, Vehicle vehicleid, int duration) {
        this.customer = custid;
        this.vehicle = vehicleid;
        this.duration = duration;
        this.rentalFare = duration * vehicle.getRentalPricing();
    }

    public int getVehicleID() {
        return vehicle.getVehicleID();
    }

    public int getCustomerID() {
        return customer.getID();
    }

    public int getDuration() {
        return duration;
    }

    public double getRentalFare() {
        return rentalFare;
    }

    public String getResponse() {
        return String.format("Vehicle %d Rented for %d days by customer %d. Rental Cost: %d\n",
                this.getVehicleID(), this.getDuration(), this.getCustomerID(), (int) (this.getRentalFare()));
    }
}

class CustomerManager {
    private List<Customer> list = new ArrayList<>();

    public String addCustomer() {
        Customer obj = new Customer();
        list.add(obj);
        return "Customer " + obj.getID() + " added\n";
    }

    public Customer getCustomer(int customerID) {
        for (Customer x : list) {
            if (x.getID() == customerID) return x;
        }
        return null;
    }

    public Vehicle getVehicle(int vehicleID, VehicleFleetManager vehicleFleetManager) {
        for (Vehicle x : vehicleFleetManager.getListOfVehicles()) {
            if (x.getVehicleID() == vehicleID)
                return x;
        }
        return null;
    }

    public String rentingVehicle(int customerID, int vehicleID, int duration, VehicleFleetManager vehicleFleetManager) {
        Customer custObj = getCustomer(customerID);
        Vehicle vehicleObj = getVehicle(vehicleID, vehicleFleetManager);
        if (custObj != null && vehicleObj != null) {
            Rent rentObj = new Rent(custObj, vehicleObj, duration);
            custObj.rentingRent(rentObj);
            return rentObj.getResponse();
        }
        return "";
    }

    public String getCustomerHistory(int customerID, VehicleFleetManager vehicleFleetManager) {
        Customer custObj = getCustomer(customerID);
        if (custObj != null) {
            StringBuilder sb = new StringBuilder();
            sb.append(String.format("Customer %d Rental History:\n", customerID));
            for (Rent x : custObj.getRentalLog()) {
                sb.append(String.format("- Vehicle ID: %d, Brand: %s, Rental Duration: %d days, Rental Cost: %d\n",
                        x.getVehicleID(), getVehicle(x.getVehicleID(), vehicleFleetManager).getBrand(),
                        x.getDuration(), (int) (x.getRentalFare())));
            }
            return sb.toString();
        }
        return "";
    }
}

public class FleetSystem {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        StringBuilder sb = new StringBuilder();
        //sb.append("Enter commands (type 'E' to exit):\n");

        VehicleFleetManager vehicleFleetManager = new VehicleFleetManager();
        CustomerManager customerManager = new CustomerManager();

        while (true) {
            String line = scanner.nextLine();
            if (line.charAt(0) == 'E') {
                break;
            }

            Scanner stringStream = new Scanner(line);
            String command = stringStream.next();

            if (command.equals("ADD_VEHICLE")) {
                Vehicle obj = null;
                String vehicleCode = stringStream.next();
                int vehicleID = stringStream.nextInt();
                String brand = stringStream.next();
                double vehiclePrice = stringStream.nextDouble();
                double rentalPricing = stringStream.nextDouble();

                if (vehicleCode.equals("c")) {
                    String type = stringStream.next();
                    String fuel = stringStream.next();
                    String transmission = stringStream.next();
                    obj = new Car(vehicleID, brand, vehiclePrice, rentalPricing, type, fuel, transmission);
                    sb.append(String.format("Car - ID: %d, Brand: %s, Price: %.2f, Rental Cost: %d/day, Type: %s, Fuel: %s, Transmission: %s\n",
                            vehicleID, brand, vehiclePrice, (int) (rentalPricing), type, fuel, transmission));
                } else if (vehicleCode.equals("t")) {
                    double cargoCapacity = stringStream.nextDouble();
                    double bedLength = stringStream.nextDouble();
                    int numberOfAxels = stringStream.nextInt();
                    double fuelEfficiency = stringStream.nextDouble();
                    obj = new Truck(vehicleID, brand, vehiclePrice, rentalPricing, numberOfAxels, cargoCapacity, bedLength, fuelEfficiency);
                    sb.append(String.format("Truck - ID: %d, Brand: %s, Price: %.2f, Rental Cost: %d/day, Cargo Capacity: %.2f kg, Bed Length: %.2f m, Axles: %d, Mileage: %.2f miles/gallon\n",
                            vehicleID, brand, vehiclePrice, (int) (rentalPricing), cargoCapacity, bedLength, numberOfAxels, fuelEfficiency));
                    vehicleFleetManager.updateCapacity(cargoCapacity);
                } else if (vehicleCode.equals("b")) {
                    String type = stringStream.next();
                    String frame = stringStream.next();
                    if(frame.equals("Carbon")){frame = "Carbon Fibre";}
                    String temp = stringStream.next();
                    int numberOfGears = stringStream.nextInt();
                    obj = new Bicycle(vehicleID, brand, vehiclePrice, rentalPricing, type, frame);
                    sb.append(String.format("Bicycle - ID: %d, Brand: %s, Price: %.2f, Rental Cost: %d/day, Type: %s, Frame: %s, Gears: %d\n",
                            vehicleID, brand, vehiclePrice, (int) (rentalPricing), type, frame, numberOfGears));
                } else if (vehicleCode.equals("d")) {
                    double maxAltitude = stringStream.nextDouble();
                    double flyTime = stringStream.nextDouble();
                    int cameraResolution = stringStream.nextInt();
                    obj = new Drone(vehicleID, brand, vehiclePrice, rentalPricing, cameraResolution, flyTime, maxAltitude);
                    sb.append(String.format("Drone - ID: %d, Brand: %s, Price: %.2f, Rental Cost: %d/day, Max Altitude: %.2f m, Flight time: %.2f min, Camera Resolution: %d MP\n",
                            vehicleID, brand, vehiclePrice, (int) (rentalPricing), maxAltitude, flyTime, cameraResolution));
                }
                vehicleFleetManager.addVehicle(obj);
            } else if (command.equals("ADD_CUSTOMER")) {
                sb.append(customerManager.addCustomer());
            } else if (command.equals("RENT")) {
                int customerID = stringStream.nextInt();
                int vehicleID = stringStream.nextInt();
                int duration = stringStream.nextInt();
                String resp = customerManager.rentingVehicle(customerID, vehicleID, duration, vehicleFleetManager);
                if (!resp.isEmpty())
                    sb.append(resp);
            } else if (command.equals("FLEET_STATISTICS")) {
                sb.append(vehicleFleetManager.vehicleFleetManagerStatistics());
            } else if (command.equals("CUSTOMER_HISTORY")) {
                int customerID = stringStream.nextInt();
                sb.append(customerManager.getCustomerHistory(customerID, vehicleFleetManager));
            }
        }
        System.out.print(sb.toString());
        scanner.close();
    }
}
