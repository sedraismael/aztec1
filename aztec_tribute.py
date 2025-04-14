import random

class CityState:
    def __init__(self, name, resources):
        self.name = name
        self.resources = resources  # Dictionary of resources and their amounts
        self.tribute_obligation = {} # Dictionary of resources and amounts owed
        self.tribute_paid = {}

    def set_tribute(self, tribute_demands):
        """Sets the tribute obligation for this city-state."""
        self.tribute_obligation = tribute_demands
        self.tribute_paid = {resource: 0 for resource in tribute_demands}
        print(f"\n{self.name} has been ordered to pay:")
        for resource, amount in self.tribute_obligation.items():
            print(f"- {amount} units of {resource}")

    def pay_tribute(self, payment):
        """Attempts to pay tribute. Returns True if successful, False otherwise."""
        for resource, amount in payment.items():
            if resource in self.resources and self.resources[resource] >= amount and resource in self.tribute_obligation:
                self.resources[resource] -= amount
                self.tribute_paid[resource] = self.tribute_paid.get(resource, 0) + amount
            elif resource not in self.tribute_obligation:
                print(f"Warning: {resource} is not part of the tribute obligation for {self.name}.")
            elif resource not in self.resources:
                print(f"Error: {self.name} does not possess {resource}.")
                return False
            elif self.resources[resource] < amount:
                print(f"Error: {self.name} does not have enough {resource} to pay the required amount.")
                return False
        print(f"\n{self.name} has paid:")
        for resource, amount in payment.items():
            print(f"- {amount} units of {resource}")
        return True

    def get_resource_report(self):
        """Returns a report of the city-state's current resources."""
        report = f"\n--- {self.name} Resources ---"
        for resource, amount in self.resources.items():
            report += f"\n- {resource}: {amount}"
        return report

    def get_tribute_status(self):
        """Returns the current tribute status of the city-state."""
        report = f"\n--- {self.name} Tribute Status ---"
        for resource, owed in self.tribute_obligation.items():
            paid = self.tribute_paid.get(resource, 0)
            remaining = owed - paid
            report += f"\n- {resource}: Owed - {owed}, Paid - {paid}, Remaining - {remaining}"
        return report

def generate_initial_resources():
    """Generates a dictionary of initial resources with random amounts."""
    resources = {
        "maize": random.randint(50, 200),
        "beans": random.randint(30, 100),
        "squash": random.randint(40, 150),
        "cotton": random.randint(20, 80),
        "obsidian": random.randint(10, 50),
        "pottery": random.randint(15, 60),
        "feathers": random.randint(5, 30)
    }
    return resources

def generate_tribute_demands(city_states):
    """Generates random tribute demands for each subject city-state."""
    tribute_demands = {}
    resources = ["maize", "beans", "cotton", "obsidian", "pottery", "feathers"] # Common tribute items
    for state in city_states:
        demands = {}
        num_demands = random.randint(1, 3)
        sampled_resources = random.sample(resources, min(num_demands, len(resources)))
        for resource in sampled_resources:
            demands[resource] = random.randint(10, 40)
        tribute_demands[state.name] = demands
    return tribute_demands

def main():
    """Main function to run the Aztec tribute system simulation."""
    print("--- Welcome to the Aztec Tribute System Simulation ---")

    # Initialize city-states
    tenochtitlan = CityState("Tenochtitlan", generate_initial_resources())
    texcoco = CityState("Texcoco", generate_initial_resources())
    tlacopan = CityState("Tlacopan", generate_initial_resources())
    subject_states = [
        CityState("Xochimilco", generate_initial_resources()),
        CityState("Chalco", generate_initial_resources()),
        CityState("Tlacopan", generate_initial_resources()) # Another Tlacopan for demonstration
    ]

    all_states = [tenochtitlan, texcoco, tlacopan] + subject_states

    print("\nInitial state of the Triple Alliance:")
    for state in all_states:
        print(f"- {state.name}")

    input("\nPress Enter to begin the tribute cycle.")

    while True:
        print("\n--- New Tribute Cycle ---")

        # Generate tribute demands for subject states
        tribute_demands = generate_tribute_demands(subject_states)
        for state in subject_states:
            state.set_tribute(tribute_demands[state.name])

        # Subject states attempt to pay tribute
        for state in subject_states:
            print(f"\n--- {state.name}'s Turn to Pay Tribute ---")
            print(state.get_resource_report())
            while True:
                payment_input = input(f"Enter tribute payment for {state.name} (e.g., maize:10,cotton:5, or 'skip' to pay all, or 'status' to see tribute status): ").lower()
                if payment_input == 'skip':
                    payment = state.tribute_obligation.copy()
                    state.pay_tribute(payment)
                    break
                elif payment_input == 'status':
                    print(state.get_tribute_status())
                    continue
                else:
                    payment = {}
                    items = payment_input.split(',')
                    try:
                        for item in items:
                            resource, amount_str = item.split(':')
                            payment[resource.strip()] = int(amount_str.strip())
                        if state.pay_tribute(payment):
                            break
                    except ValueError:
                        print("Invalid input format. Please use 'resource:amount' separated by commas.")

        # Report on tribute received by the Triple Alliance (simplified)
        print("\n--- Tribute Received by the Triple Alliance ---")
        for state in subject_states:
            print(f"- {state.name} paid:")
            for resource, amount in state.tribute_paid.items():
                print(f"  - {amount} units of {resource}")

        # Offer options for the next cycle
        action = input("\nWhat would you like to do? (next cycle/resources/status/quit): ").lower()
        if action == 'next cycle':
            continue
        elif action == 'resources':
            for state in all_states:
                print(state.get_resource_report())
        elif action == 'status':
            for state in subject_states:
                print(state.get_tribute_status())
        elif action == 'quit':
            break
        else:
            print("Invalid action. Please choose from the options.")

if __name__ == "__main__":
    main()
