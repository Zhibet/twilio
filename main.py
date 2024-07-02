import pandas as pd
from twilio.rest import Client

# Load the CSV file
excel_file = pd.read_csv('50_states.csv')
states = excel_file.state
len_of_states = len(states)
score = 0
guess_container = []
missed_container = []

game_on = True

while game_on and score < len_of_states:
    print('Type "exit" to end the game')
    user_guess = str(input('Enter a state: ')).title()

    if user_guess == 'Exit':
        game_on = False
        print('Game ended.')
        break

    if user_guess in guess_container:
        print(f'You have already guessed {user_guess}. Try another state.')
        continue

    if user_guess in states.values:
        score += 1
        guess_container.append(user_guess)
        print(f'Correct! You have guessed: {guess_container}')
    else:
        print(f'Incorrect guess.')

    print(f'Your score is {score}/{len_of_states}')

    if score == len_of_states:
        print('Congratulations! You have guessed all the states.')
        game_on = False

# Determine missed states
missed_container = [state for state in states if state not in guess_container]

if missed_container:
    print('You missed the following states:')
    print(missed_container)
else:
    print('You guessed all the states!')

print(f'Your final score is {score}/{len_of_states}')

# Write missed states to a file
with open('missed_states.txt', mode='w') as file:
    file.write(','.join(missed_container))

# Twilio configuration
account_sid = 'AC08828de4b5871bc411867e94f7f187c6'  # Replace with your Twilio Account SID
auth_token = '3fee7361753be88a44fe6eed3ae2a302'  # Replace with your Twilio Auth Token
twilio_phone_number = '+1-855-589-5208'  # Replace with your Twilio phone number
recipient_phone_number = '+1-929-329-9057'  # Replace with the recipient's phone number

# Create a Twilio client
client = Client(account_sid, auth_token)

# Create the message body
message_body = f"You missed the following states: {', '.join(missed_container)}"

# Send the message
message = client.messages.create(
    body=message_body,
    from_=twilio_phone_number,
    to=recipient_phone_number
)

print(f"Message sent: {message.date_sent}, {message.date_created}")
