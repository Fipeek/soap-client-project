from zeep import Client, Plugin
from lxml import etree


# URL to the WSDL
wsdl_url = 'http://localhost:1000/flight?wsdl'

# Create a client with the custom plugin
client = Client(wsdl=wsdl_url)

def format_flight(flight):
    return (f"Flight Number: {flight.flightNumber}, Departure: {flight.departure}, "
            f"Destination: {flight.destination}, Departure Time: {flight.departureTime}, "
            f"Arrival Time: {flight.arrivalTime}, Price: {flight.price}, Date: {flight.date} ")

def format_ticket(ticket):
    flight_details = format_flight(ticket.flight)
    return f"Ticket Number: {ticket.ticketNumber}, Flight Details: [{flight_details}]"

def get_flights():
    flights = client.service.getFlights()
    return "\n".join([format_flight(flight) for flight in flights])

def get_flights_by_departure(departure):
    flights = client.service.getFlightsByDeparture(departure)
    return "\n".join([format_flight(flight) for flight in flights])

def get_flights_by_destination(destination):
    flights = client.service.getFlightsByDestination(destination)
    return "\n".join([format_flight(flight) for flight in flights])

def get_flights_by_departure_and_destination(departure, destination):
    flights = client.service.getFlightsByDepartureAndDestination(departure, destination)
    return "\n".join([format_flight(flight) for flight in flights])

def get_ticket_by_number(ticket_number):
    ticket = client.service.getTicketByNumber(ticket_number)
    if ticket:
        return format_ticket(ticket)
    else:
        return "No ticket found with that number."


def buy_ticket_and_download_pdf(flight_number):
    try:
        response = client.service.buyTicket(flight_number)

        if not response:
            print("No ticket was issued or flight not found. Please check the flight number and try again.")
        else:
            print(f"Ticket purchased successfully!")

            with open(f"{flight_number}.pdf", "wb") as pdf_file:
                pdf_file.write(response)  # Write the bytes directly
            print(f"PDF ticket saved as {flight_number}.pdf")
    except Exception as e:
        print(f"An error occurred: {e}")


def display_menu():
    while True:
        print("\nFlight Web Service Client")
        print("1. List all flights")
        print("2. Get flights by departure city")
        print("3. Get flights by destination city")
        print("4. Get flights by departure and destination cities")
        print("5. Buy a ticket")
        print("6. Get ticket details by ticket number")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Flights:\n", get_flights())
        elif choice == '2':
            departure = input("Enter departure city: ")
            print(f"Flights from {departure}:\n", get_flights_by_departure(departure))
        elif choice == '3':
            destination = input("Enter destination city: ")
            print(f"Flights to {destination}:\n", get_flights_by_destination(destination))
        elif choice == '4':
            departure = input("Enter departure city: ")
            destination = input("Enter destination city: ")
            print(f"Flights from {departure} to {destination}:\n", get_flights_by_departure_and_destination(departure, destination))
        elif choice == '5':
            flight_number = input("Enter flight number: ")
            buy_ticket_and_download_pdf(flight_number)
        elif choice == '6':
            ticket_number = input("Enter ticket number: ")
            print("Ticket Details:\n", get_ticket_by_number(ticket_number))
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again!")

# Run the menu
if __name__ == "__main__":
    display_menu()
