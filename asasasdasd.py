import re
import cmd

class TimeCalculator(cmd.Cmd):
    intro = "Welcome to the Time Calculator. Enter time in hh.mm format or 'q' to quit."
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.total_hours = 0
        self.total_minutes = 0

    def do_q(self, arg):
        """Quit the program"""
        return True

    def validate_time_format(self, time_input):
        # Allow both '.' and ',' as decimal separators
        return re.match(r'^\d{1,2}([.,]\d{2})?$', time_input)

    def do_time(self, time_input):
        """Add time in hh.mm format"""
        if self.validate_time_format(time_input):
            # Replace comma (,) with a dot (.) for parsing
            time_input = time_input.replace(',', '.')
            hours, minutes = map(float, time_input.split('.'))
            self.total_hours += hours
            self.total_minutes += minutes
            self.total_hours += self.total_minutes // 60
            self.total_minutes %= 60
            print(f"Total time: {int(self.total_hours)} hours and {int(self.total_minutes)} minutes")
        else:
            print("Invalid input format. Please use hh.mm format.")

if __name__ == "__main__":
    TimeCalculator().cmdloop()
