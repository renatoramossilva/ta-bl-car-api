""" This module contains the service functions for the car booking API. """
from typing import Optional
import json
import pathlib
from datetime import datetime


def get_file_path(filename: str) -> pathlib.Path:
    """Return the absolute file path based on the filename."""
    return pathlib.Path(__file__).parent.parent / "app" / "db" / filename


def save_data(file_path: pathlib.Path, data: dict) -> None:
    """
    Save data to a JSON file.

    :param file_path: Path to the file where data will be saved.
    :param data: Data to be saved in the JSON format.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_data(file_path: pathlib.Path) -> dict:
    """
    Load data from a JSON file.

    :param file_path: Path to the JSON file to load data from.
    :return: Data loaded from the JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def list_cars() -> list:
    """
    Retrieve the list of cars from the data file.

    This function loads the car data from a JSON file and returns the list of cars.
    If the 'cars' key is not found, an empty list is returned.
    If an error occurs while loading the data, an exception is raised.

    :return: A list of cars, or an empty list if no cars are found.
    :raises:
        RuntimeError: If there is an error loading the car data from the file.
    """
    try:
        data = load_data(get_file_path("cars.json"))
        return data.get(
            "cars", []
        )  # Return the list of cars or an empty list if 'cars' key is not found
    except Exception as e:
        raise RuntimeError(f"Error loading the cars: {e}") from e


def create_booking(
    car_id: int, start_date: str, end_date: str, pickup_time: str, dropoff_time: str
) -> bool:
    """
    Creates a booking for a car within a specified date range and time.

    This function checks if the car is available for the provided date range and creates a booking
    if the car is not already booked. The booking is saved in the `bookings.json` file.

    :param car_id: The ID of the car to be reserved.
    :param start_date: The start date of the booking in 'YYYY-MM-DD' format.
    :param end_date: The end date of the booking in 'YYYY-MM-DD' format.
    :param pickup_time: The time the car will be picked up in 'HH:MM' format.
    :param dropoff_time: The time the car will be dropped off in 'HH:MM' format.

    :return: True if the booking is successfully created, False if the car is already booked for
              the specified time range.

    :raises:
        ValueError: If the car with the specified ID is not found.
    """
    # Load data from files
    cars = load_data(get_file_path("cars.json")).get("cars", [])
    bookings_data = load_data(get_file_path("bookings.json"))
    bookings = bookings_data.get("bookings", [])

    print("bookings")
    print(bookings)
    # Check if car exists
    car = next((car for car in cars if car["id"] == car_id), None)
    if not car:
        raise ValueError("Car not found.")

    # Convert the start and end dates to datetime objects
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    # Check for overlapping bookings
    if any(
        booking["car_id"] == car_id
        and not (
            end_date_obj < datetime.strptime(booking["startDate"], "%Y-%m-%d")
            or start_date_obj > datetime.strptime(booking["endDate"], "%Y-%m-%d")
        )
        for booking in bookings
    ):
        return False

    # Create and save new booking
    new_booking = {
        "car_id": car_id,
        "startDate": start_date,
        "endDate": end_date,
        "pickupTime": pickup_time,
        "dropoffTime": dropoff_time,
    }
    bookings.append(new_booking)
    bookings_data["bookings"] = bookings
    save_data(get_file_path("bookings.json"), bookings_data)

    return True


def is_car_available(car_id: int, start_date: str, end_date: str) -> bool:
    """
    Checks if a car is available for a given date range.

    :param car_id: The ID of the car to check availability for.
    :param start_date: The start date of the reservation in 'YYYY-MM-DD' format.
    :param end_date: The end date of the reservation in 'YYYY-MM-DD' format.
    :return: `True` if the car is available, `False` if it is already booked.
    """
    with open(get_file_path("bookings.json"), "r", encoding="utf-8") as file:
        bookings_data = json.load(file).get("bookings", [])

    # Iterate through all bookings
    for booking in bookings_data:
        if booking["car_id"] == car_id:
            # Convert dates to datetime objects
            booking_start = datetime.strptime(booking["startDate"], "%Y-%m-%d")
            booking_end = datetime.strptime(booking["endDate"], "%Y-%m-%d")
            requested_start = datetime.strptime(start_date, "%Y-%m-%d")
            requested_end = datetime.strptime(end_date, "%Y-%m-%d")

            # Check for overlapping dates
            if requested_start <= booking_end and requested_end >= booking_start:
                return False  # The car is booked, not available

    return True  # The car is available


def check_car_availability(
    start_date: str, end_date: str, car_model: Optional[str] = None
) -> list:
    """
    Checks the availability of cars for a given date range, optionally filtering by car model.

    :param start_date: The start date of the reservation ('YYYY-MM-DD').
    :param end_date: The end date of the reservation ('YYYY-MM-DD').
    :param car_model: The model of the car to check for availability (optional).
    :return: A list of available cars, each represented as a dictionary.
    """
    with open(get_file_path("cars.json"), "r", encoding="utf-8") as file:
        cars_data = json.load(file)

    available_cars = []

    if car_model:
        for car in cars_data["cars"]:
            if car["name"].lower() == car_model.lower():
                car_id = car["id"]
                if is_car_available(car_id, start_date, end_date):
                    available_cars.append(car)
    else:
        for car in cars_data["cars"]:
            car_id = car["id"]
            if is_car_available(car_id, start_date, end_date):
                available_cars.append(car)

    return available_cars
