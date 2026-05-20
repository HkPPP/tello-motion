from djitellopy import Tello

def main():
    print("Hello from tello-motion!")

    tello = Tello()

    tello.connect()
    tello.takeoff()

    tello.rotate_clockwise(360)

    tello.land()


if __name__ == "__main__":
    main()
