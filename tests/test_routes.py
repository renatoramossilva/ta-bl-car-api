import json
import pathlib

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes import router

client = TestClient(app)


@pytest.fixture
def mock_list_cars(mocker):
    mocker.patch(
        "app.services.list_cars",
        return_value=[
            {"id": 1, "name": "SEAT Ibiza"},
            {"id": 2, "name": "Volkswagen Polo"},
        ],
    )


@pytest.fixture
def mock_check_availability(mocker):
    mocker.patch(
        "app.services.check_car_availability",
        return_value=[{"id": 2, "name": "Volkswagen Polo"}],
    )


@pytest.fixture
def mock_create_booking(mocker):
    mocker.patch("app.services.create_booking", return_value=True)


def get_mockfile_path(filename: str) -> pathlib.Path:
    """Return the absolute file path based on the filename."""
    return pathlib.Path(__file__).parent.parent / "tests" / "db" / f"mock_{filename}"


@pytest.fixture
def cleanup_bookings():
    file_path = get_mockfile_path("bookings.json")

    yield  # Run the test

    # After the test, clean up the mock_bookings.json file
    with open(file_path, "w") as f:
        json.dump({"bookings": []}, f, indent=4)


def test_get_all_cars(mocker, mock_list_cars):
    def mock_get_file_path(filename):
        return (
            pathlib.Path(__file__).parent.parent / "tests" / "db" / f"mock_{filename}"
        )

    mocker.patch("app.services.get_file_path", side_effect=mock_get_file_path)
    response = client.get("/cars/")
    assert response.status_code == 200

    with open(get_mockfile_path("cars.json")) as file:
        expected_cars = json.load(file)["cars"]

    assert response.json() == {"cars": expected_cars}


@pytest.mark.parametrize(
    ("params", "reponse_code", "response_json"),
    [
        (
            {
                "start_date": "2024-12-01",
                "end_date": "2024-12-10",
                "car_model": "Volkswagen Polo",
            },
            200,
            {"available_cars": [{"id": 2, "name": "Volkswagen Polo"}]},
        ),
        (
            {
                "start_date": "2024-12-01",
                "end_date": "2024-12-10",
                "car_model": "Nonexistent",
            },
            404,
            {"detail": "No available cars found for the given dates and model."},
        ),
        (
            {"start_date": "2024-12-01", "end_date": "2024-12-10"},
            200,
            {
                "available_cars": [
                    {"id": 1, "name": "SEAT Ibiza"},
                    {"id": 2, "name": "Volkswagen Polo"},
                ]
            },
        ),
    ],
)
def test_check_car_availability(
    params, reponse_code, response_json, mocker, mock_check_availability
):
    def mock_get_file_path(filename):
        return (
            pathlib.Path(__file__).parent.parent / "tests" / "db" / f"mock_{filename}"
        )

    mocker.patch("app.services.get_file_path", side_effect=mock_get_file_path)
    response = client.get("/check_car_availability", params=params)

    assert response.status_code == reponse_code
    assert response.json() == response_json


def test_post_booking_success(mocker, mock_create_booking):
    def mock_get_file_path(filename):
        return (
            pathlib.Path(__file__).parent.parent / "tests" / "db" / f"mock_{filename}"
        )

    mocker.patch("app.services.get_file_path", side_effect=mock_get_file_path)

    payload = {
        "car_id": 1,
        "start_date": "2024-12-01",
        "end_date": "2024-12-10",
        "pickup_time": "08:00",
        "dropoff_time": "18:00",
    }
    response = client.post("/booking/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Booking successfully created!"}


@pytest.mark.usefixtures("cleanup_bookings")
def test_post_booking_conflict(mocker):
    def mock_get_file_path(filename):
        return (
            pathlib.Path(__file__).parent.parent / "tests" / "db" / f"mock_{filename}"
        )

    mocker.patch("app.services.get_file_path", side_effect=mock_get_file_path)
    mocker.patch("app.services.create_booking", return_value=False)

    # Payload to create a booking
    payload = {
        "car_id": 1,
        "start_date": "2024-12-01",
        "end_date": "2024-12-10",
        "pickup_time": "08:00",
        "dropoff_time": "18:00",
    }

    # Send a POST request to create a new booking
    response = client.post("/booking/", json=payload)
    # Check if the response status code is 400
    assert response.status_code == 400
    assert response.json() == {"detail": "Car already booked for the given time range."}
