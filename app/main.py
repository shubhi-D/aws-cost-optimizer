import json
from app.analyzers.idle_ec2_analyzer import find_idle_instances

def main():

    idle = find_idle_instances()

    print("\nIdle Instances Found:", len(idle))

    for i in idle:
        print(i)

    with open("output/idle_instances.json", "w") as f:
        json.dump(idle, f, indent=4)


if __name__ == "__main__":
    main()