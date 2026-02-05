from common.protocol import mcp_request
from server.mcp_server import handle_request

def run():
    city = input("Enter city (delhi/mumbai/bangalore): ")

    request = mcp_request(
        tool="weather",
        params={"city": city}
    )

    response = handle_request(request)

    if response["status"] == "success":
        print("\n🌤 Weather Report")
        print("City:", response["data"]["city"])
        print("Temperature:", response["data"]["temperature"], "°C")

        if response["data"]["alert"]:
            print("ALERT:", response["data"]["alert"])
    else:
        print("Error:", response["data"])


if __name__ == "__main__":
    run()
