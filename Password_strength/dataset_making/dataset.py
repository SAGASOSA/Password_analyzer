import pandas as pd
from zxcvbn import zxcvbn
from faker import Faker
import random
import string

fake = Faker()

def generate_passwords(num_samples):
    data = []
    
    for i in range(num_samples):
        # --- NEW LOGIC: Add admin1 and user1, user2... ---
        if i == 0:
            username = "admin1"
            role = "admin"
        else:
            username = f"user{i}"
            role = "user"
            
        # 50% chance of generating a "weak" human-like password, 50% "strong" random
        if random.choice([True, False]):
            # Weak/Medium: Combine random words and numbers
            pwd = fake.word() + str(random.randint(1, 999)) + random.choice(['!', '@', '#', ''])
        else:
            # Strong: Completely random characters (length 8 to 20)
            length = random.randint(8, 20)
            pwd = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
            
        # Analyze with zxcvbn
        analysis = zxcvbn(pwd)
        
        # Get estimated crack time in seconds (offline attack speed)
        crack_time = analysis['crack_times_seconds']['offline_fast_hashing_1e10_per_second']
        
        # Assign label based on zxcvbn score (0-2: weak, 3: medium, 4: strong)
        score = analysis['score']
        if score <= 2:
            label = 'weak'
        elif score == 3:
            label = 'medium'
        else:
            label = 'strong'
            
        # Append the new columns to the dataset
        data.append({
            'username': username,
            'role': role,
            'password': pwd,
            'strength_label': label,
            'crack_time_seconds': crack_time
        })
        
    return pd.DataFrame(data)

# Generate 10,000 rows
df = generate_passwords(10000)

# Save to CSV
df.to_csv('password_dataset_with_users.csv', index=False)
print("Successfully generated dataset with users/admin and saved to 'password_dataset_with_users.csv'")