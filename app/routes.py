"""
This module contains the FastAPI routes for the car booking API.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import check_car_availability
from app.services import create_booking
from app.services import list_cars

router = APIRouter()


class BookingRequest(BaseModel):
    """Pydantic model for the booking request."""

    car_id: int
    start_date: str
    end_date: str
    pickup_time: str
    dropoff_time: str


@router.get("/cars/")
def get_all_cars() -> dict:
    """
    Endpoint to list the company's car fleet.

    **Request Body:**
    - None

    **Returns:**
    A dictionary containing the list of all cars in the company's fleet

    **Example Request:**
    ```
    {
        "cars":[
            {
                "id":1,
                "name":"SEAT Ibiza"
            }
        ]
    }
    ```

    **Raises:**
    - `HTTPException`: If an error occurs while retrieving the car fleet, an HTTPException
        is raised with status code 500 and the error message.
    """
    try:
        cars = list_cars()
        return {"cars": cars}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/check_car_availability")
def check_availability(
    start_date: str, end_date: str, car_model: Optional[str] = None
) -> dict:
    """
    Endpoint to check the availability of cars for a given date range and optional car model.

    This endpoint checks the availability of cars based on the provided start and end dates.
    Optionally, a specific car model can be provided to filter the results.

    - `start_date` (str): The start date for the booking (in "YYYY-MM-DD" format). \n
    - `end_date` (str): The end date for the booking (in "YYYY-MM-DD" format).
    - `car_model` Optional[str]: The optional car model to check for availability. If not provided,
                                    all car models will be considered.

    **Returns:**
    - `available_cars`: A dictionary containing a list of available cars for the
    given date range and model. The list is provided under the key "available_cars".

    **Example Request:**
    - If the car is available:
    ```
    {
        "available_cars": [
            {
                "id":2,
                "name":"Volkswagen Polo"
            }
        ]
    }
    ```

    or

    - If the car is not available:
    ```
    {
        "detail":"No available cars found for the given dates and model."
    }
    ```

    **Raises:**
    - `HTTPException`: If no cars are available for the given dates and model, a 404 error is raised
                       with the message "No available cars found for the given dates and model."
    """
    available_cars = check_car_availability(start_date, end_date, car_model)

    if not available_cars:
        raise HTTPException(
            status_code=404,
            detail="No available cars found for the given dates and model.",
        )

    return {"available_cars": available_cars}


@router.post("/booking/")
def post_booking(booking: BookingRequest) -> dict:
    """
    Create a car booking for a specified date and time range.

    **Request Body:**
    - `booking` (BookingRequest): The booking details including
    car_id, start_date, end_date, pickup_time, and dropoff_time.

    **Returns:**
    A message indicating the success or failure of the booking process.

    **Raises:**
    - `HTTPException` if the car is already booked for the given time range or
    there is an error.
    """
    try:
        success = create_booking(
            booking.car_id,
            booking.start_date,
            booking.end_date,
            booking.pickup_time,
            booking.dropoff_time,
        )
        if success:
            return {"message": "Booking successfully created!"}

        raise HTTPException(
            status_code=400, detail="Car already booked for the given time range."
        )
    except Exception as e:
        raise e
