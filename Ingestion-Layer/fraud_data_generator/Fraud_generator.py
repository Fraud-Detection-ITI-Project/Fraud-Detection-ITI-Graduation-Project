import json
import time
import uuid
import random
import math
import os
import csv
import hashlib
from datetime import datetime, timedelta, timezone
from faker import Faker
import numpy as np

# --- Configuration ---
OUTPUT_CSV_FILE = 'transactions_egypt_centric_final_v3.csv'
NUM_TRANSACTIONS = 500000 
FRAUD_PERSONA_RATE = 0.11
NUM_INITIAL_MERCHANTS = 300
NUM_FRAUD_MERCHANTS = 5
START_DATE = datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
END_DATE = datetime(2023, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

# --- EGYPT-CENTRIC DATA ---
EGYPTIAN_BANKS = ["National Bank of Egypt (NBE)", "Banque Misr", "Commercial International Bank (CIB)", "QNB Alahli", "Alexbank", "Banque du Caire", "HSBC Bank Egypt", "Arab African International Bank (AAIB)", "Faisal Islamic Bank of Egypt", "Credit Agricole Egypt", "EG Bank", "Suez Canal Bank", "SAIB Bank", "Attijariwafa Bank Egypt", "United Bank of Egypt", "Abu Dhabi Islamic Bank (ADIB) Egypt", "Al Baraka Bank Egypt", "Housing and Development Bank (HDB)"]
EGYPTIAN_MERCHANTS = [ {'name': 'Carrefour Hypermarket', 'category': 'Grocery'}, {'name': 'Spinneys', 'category': 'Grocery'}, {'name': 'Metro Market', 'category': 'Grocery'}, {'name': 'Seoudi Supermarket', 'category': 'Grocery'}, {'name': 'Kheir Zaman', 'category': 'Grocery'}, {'name': 'Kazyon', 'category': 'Grocery'}, {'name': 'Gourmet Egypt', 'category': 'Grocery'}, {'name': 'Awlad Ragab', 'category': 'Grocery'}, {'name': 'Hyper One', 'category': 'Grocery'}, {'name': 'B.Tech', 'category': 'Electronics'}, {'name': 'Raya Shop', 'category': 'Electronics'}, {'name': 'Tradeline', 'category': 'Electronics'}, {'name': '2B Computer', 'category': 'Electronics'}, {'name': 'Virgin Megastore', 'category': 'Electronics'}, {'name': 'iShop Egypt', 'category': 'Electronics'}, {'name': 'Abou Tarek', 'category': 'Restaurants'}, {'name': 'Gad Restaurants', 'category': 'Restaurants'}, {'name': "McDonald's", 'category': 'Restaurants'}, {'name': 'KFC', 'category': 'Restaurants'}, {'name': 'Cilantro Cafe', 'category': 'Restaurants'}, {'name': 'Starbucks', 'category': 'Restaurants'}, {'name': 'Cook Door', 'category': 'Restaurants'}, {'name': "Mo'men", 'category': 'Restaurants'}, {'name': 'El Abd Patisserie', 'category': 'Restaurants'}, {'name': 'Tseppas', 'category': 'Restaurants'}, {'name': 'Zooba', 'category': 'Restaurants'}, {'name': 'WE', 'category': 'Services'}, {'name': 'Orange Egypt', 'category': 'Services'}, {'name': 'Vodafone Egypt', 'category': 'Services'}, {'name': 'Etisalat Misr', 'category': 'Services'}, {'name': 'Fawry', 'category': 'Services'}, {'name': 'Bee', 'category': 'Services'}, {'name': 'El Ezaby Pharmacy', 'category': 'Health'}, {'name': 'Seif Pharmacy', 'category': 'Health'}, {'name': 'Roshdy Pharmacy', 'category': 'Health'}, {'name': '19011 Pharmacy', 'category': 'Health'}, {'name': 'TotalEnergies Station', 'category': 'Fuel'}, {'name': 'Chillout Station', 'category': 'Fuel'}, {'name': 'Wataniya Petroleum', 'category': 'Fuel'}, {'name': 'Misr Petroleum', 'category': 'Fuel'}, {'name': 'On the Run', 'category': 'Retail'}, {'name': 'Diwan Bookstore', 'category': 'Retail'}, {'name': 'Alef Bookstores', 'category': 'Retail'}, {'name': 'LC Waikiki', 'category': 'Retail'}, {'name': 'Carina', 'category': 'Retail'}, {'name': 'Mobaco Cottons', 'category': 'Fashion'}, {'name': 'Town Team', 'category': 'Fashion'}, {'name': 'Concrete', 'category': 'Fashion'}, {'name': 'Oranges & Lemons', 'category': 'Fashion'}, {'name': 'ZARA Egypt', 'category': 'Fashion'}, {'name': 'IKEA', 'category': 'Furniture'}, {'name': 'In & Out Furniture', 'category': 'Furniture'}, {'name': 'Home Centre Egypt', 'category': 'Furniture'} ]

# NEW: Geographically consistent coordinate mapping (THE GEOFIAX)
EGYPTIAN_LOCATION_COORDS = {
    "Maadi": {"lat": (29.95, 29.97), "lon": (31.24, 31.26)},
    "Zamalek": {"lat": (30.05, 30.07), "lon": (31.21, 31.23)},
    "Heliopolis": {"lat": (30.08, 30.12), "lon": (31.32, 31.36)},
    "Nasr City": {"lat": (30.04, 30.07), "lon": (31.32, 31.36)},
    "New Cairo": {"lat": (30.00, 30.03), "lon": (31.40, 31.50)},
    "6th of October": {"lat": (29.94, 29.97), "lon": (30.90, 30.95)},
    "Sheikh Zayed": {"lat": (30.00, 30.05), "lon": (30.95, 31.00)},
    "Alexandria": {"lat": (31.18, 31.22), "lon": (29.90, 29.95)},
    "Aswan": {"lat": (24.08, 24.10), "lon": (32.88, 32.92)},
    "Luxor": {"lat": (25.68, 25.70), "lon": (32.63, 32.65)},
    "Hurghada": {"lat": (27.24, 27.27), "lon": (33.80, 33.84)},
    "Sharm El Sheikh": {"lat": (27.89, 27.93), "lon": (34.30, 34.35)},
    "Mansoura": {"lat": (31.03, 31.05), "lon": (31.37, 31.39)},
    "Tanta": {"lat": (30.78, 30.80), "lon": (30.99, 31.01)},
    "Suez": {"lat": (29.96, 29.98), "lon": (32.53, 32.55)},
    "Asyut": {"lat": (27.17, 27.19), "lon": (31.17, 31.19)}
}
EGYPTIAN_LOCATIONS = list(EGYPTIAN_LOCATION_COORDS.keys())
arabic_first_names = [ "Ahmed", "Mohamed", "Omar", "Youssef", "Mostafa", "Mahmoud", "Khaled", "Tamer", "Hossam", "Karim", "Hussein", "Abdelrahman", "Ali", "Amr", "Ibrahim", "Tarek", "Ayman", "Rami", "Walid", "Sherif", "Adel", "Sameh", "Ehab", "Fady", "Mina", "Ziad", "Hany", "Islam", "Bassel", "Karem", "Maged", "Gamal", "Yassin", "Sami", "Nader", "Nabil", "Ashraf", "Waleed", "Alaa", "Bahaa", "Fouad", "Ramadan", "Hatem", "Reda", "Galal", "Hazem", "Basem", "Sherban", "Sayed", "Anas", "Abdallah", "Shady", "Ihab", "Nashaat", "Khalil", "Emad", "Tawfik", "Fathi", "Fekry", "Montasser", "Lotfy", "Mohsen", "Sabry", "Barakat", "Moataz", "Abanoub", "Beshoy", "Refaat", "Farouk", "Nour", "Ezzat", "Izz", "Ragab", "Saber", "Gerges", "Helmy", "Atef", "Khalifa", "Yehia", "Abdelrahim", "Ezzeldin", "Sayyed", "Raafat", "Hani", "Soly", "Tawheed", "Ameen", "Hafez", "Latif", "Azzam", "Makram", "Hegazy", "Salah", "Nasr", "Eid", "Shehata", "Haggag", "Faris", "Rabea", "Fatma", "Mariam", "Sara", "Salma", "Heba", "Dina", "Yasmin", "Reem", "Laila", "Hager", "Hana", "Farah", "Nadine", "Rania", "Riham", "Mai", "Aya", "Shaimaa", "Marwa", "Menna", "Doaa", "Rowan", "Zeina", "Amani", "Noha", "Eman", "Samar", "Omneya", "Hoda", "Mona", "Engy", "Raghda", "Ghada", "Jana", "Habiba", "Nahla", "Asmaa", "Nermine", "Yara", "Jumana", "Sherine", "Maha", "Dalal", "Rokaya", "Sally", "Amira", "Basma", "Lina", "Mayar", "Tasneem", "Maiada", "Nourhan", "Esraa", "Shahed", "Sondos", "Iman", "Gehad", "Walaa", "Azza", "Nadia", "Afaf", "Sahar", "Souad", "Mervat", "Hend", "Rabab", "Maysa", "Samira", "Elham", "Rafif", "Ahlam", "Manal", "Lubna", "Marina", "Basant", "Naglaa", "Thuraya", "Wafaa", "Magda", "Hekmat", "Nabila", "Khadija", "Zahra", "Samah", "Latifa", "Safaa", "Nahed", "Azhar", "Misk", "Ritaj", "Rehab", "Shaima", "Bushra" ]
arabic_last_names = [ "El-Sayed", "Hassan", "Ibrahim", "Ali", "Mahmoud", "Taha", "Fathy", "Adel", "Kamel", "Gaber", "Hegazy", "Abdelrahman", "Khalil", "Salah", "Lotfy", "Zaki", "Hamdy", "Saad", "Yassin", "Ghoneim", "Farouk", "Ashour", "Khaled", "Amin", "Anwar", "Shaaban", "Hussein", "Saleh", "Barakat", "Radi", "Morsi", "Fouad", "Badr", "Nasr", "Montasser", "Arafa", "Shehata", "Zahran", "Ezzat", "Mekky", "El-Shenawy", "Sobhy", "El-Baz", "Azab", "Shaker", "Darwish", "Qandil", "Eid", "Awad", "Wahba", "Ragab", "Hamza", "Mansour", "Khattab", "Younis", "Helmy", "Samir", "Refaat", "Selim", "Reda", "Bakr", "Farid", "Sami", "Gad", "Sarhan", "Hilal", "Nabil", "Amer", "Tawfik", "Fahmy", "Rashed", "El-Khouly", "Badawy", "Ismail", "Abdelaziz", "Tawfiq", "Sabry", "El-Masry", "Marzouk", "Nour", "Ramy", "Emam", "Mekhael", "Awadallah", "Shaat", "Galal", "Zidan", "Hamouda", "Bayoumi", "Bahgat", "Roushdy", "Ashraf", "Helal", "Serry", "El-Naggar", "Sakr", "Nassar", "Attia", "Mostafa", "Bakry", "Zein", "Khairy", "Mahgoub", "Radwan", "Haggag", "Azzam", "Khodary", "Shahin", "Yehia", "Hendy", "Abaza", "Omran", "Fekry", "Aly", "Mounir", "El-Nemr", "Sherif", "Izzat", "Gharib", "Shalaby", "Ramzy", "Khater", "El-Meligy", "Abdelhafiz", "Abdelmeguid", "Zaghloul", "Khalifa", "Zohdy", "Shaheen", "Ezzeldin", "Sayyed", "Tawhed", "Bishr", "Hassanein", "Seif", "Qassem", "Moawad", "Saafan", "Nashaat", "Atef", "Hendi", "Mahran", "El-Guindy", "Hamada", "Ashmawy", "Shalash", "El-Gendy", "Soliman", "El-Haddad", "Tantawy", "Halim", "Basyouny", "Madkour", "Roshdy", "Shokry", "Makhlouf", "Shaarawy", "Hammouda", "Baghdady", "El-Gazzar", "Hashem", "Shalabi", "Tammam", "Khalouda", "Labib", "Younan", "Ragheb", "Ghattas", "Mikhael", "Barsoum", "Botros", "Mounes", "El-Batrawy", "El-Ashry", "Bassiouny", "El-Kady", "El-Attar", "El-Nahas", "Khirfan", "El-Kotby", "El-Kholy", "Bayomi", "Zeineldin", "Shobokshi", "Bedeir", "Hamid", "Barghash", "Mobarak", "El-Qadi"]
HIGH_RISK_DOMAINS = ["yopmail.com", "temp-mail.org", "mail.ru", "10minutemail.com"]
EGYPTIAN_EMAIL_DOMAINS = ["gmail.com", "outlook.com", "hotmail.com", "tedata.net.eg", "orange.com.eg", "vodafone.com.eg", "link.net"]
DOMAIN_WEIGHTS = [50, 20, 15, 5, 5, 4, 1]
fake = Faker('ar_EG')
FRAUDULENT_DEVICE_POOL = [str(uuid.uuid4()) for _ in range(50)]
FRAUDULENT_IP_POOL = [fake.ipv4() for _ in range(50)]
def haversine_distance(lat1, lon1, lat2, lon2): R = 6371; phi1, phi2, delta_phi, delta_lambda = map(math.radians, [lat1, lat2, lat2 - lat1, lon2 - lon1]); a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2; return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
def sha256_hash(data): return hashlib.sha256(data.encode()).hexdigest()

def get_coords(location_name=None):
    if location_name and location_name in EGYPTIAN_LOCATION_COORDS:
        bounds = EGYPTIAN_LOCATION_COORDS[location_name]
        lat = random.uniform(bounds["lat"][0], bounds["lat"][1])
        lon = random.uniform(bounds["lon"][0], bounds["lon"][1])
    else: 
        lat = random.uniform(24.0, 31.5)
        lon = random.uniform(25.5, 34.5)
    return {'lat': lat, 'lon': lon}

def create_realistic_email(name, domains=None, weights=None):
    if domains is None: domains, weights = EGYPTIAN_EMAIL_DOMAINS, DOMAIN_WEIGHTS
    name_parts = name.lower().replace(" ", random.choice([".", "_", ""]))
    suffix = random.choice(["", str(random.randint(1980, 2005))])
    domain = random.choices(domains, weights=weights, k=1)[0]
    return f"{name_parts}{suffix}@{domain}"

# --- Persona Base Class ---
class Persona:
    def __init__(self):
        self.customer_id = str(uuid.uuid4()); self.customer_name = f"{random.choice(arabic_first_names)} {random.choice(arabic_last_names)}"; self.customer_tenure_days = random.randint(30, 2000)
        self.customer_email = create_realistic_email(self.customer_name); self.customer_email_domain = self.customer_email.split('@')[1]
        self.customer_address_change_days = random.randint(30, self.customer_tenure_days) if self.customer_tenure_days > 30 else self.customer_tenure_days
        self.home_location_name = random.choice(EGYPTIAN_LOCATIONS); self.home_location = get_coords(self.home_location_name)
        self.card_number_hash = sha256_hash(fake.credit_card_number()); self.card_issuing_country = 'EG' if random.random() > 0.05 else random.choice(['US', 'SA', 'AE']); self.current_device = str(uuid.uuid4()); self.device_os = random.choice(['Android', 'iOS', 'Windows', 'MacOS']); self.avg_txn_amount = random.uniform(200, 2000)
        self.last_txn_timestamp = START_DATE - timedelta(days=random.randint(1, 30)); self.last_txn_location = self.home_location; self.merchant_history = {}; self.is_fraudulent_persona = False;
        self.typical_categories = random.sample([m['category'] for m in EGYPTIAN_MERCHANTS if m['category'] != 'Services'], k=random.randint(2, 3))
        self.preferred_channel = 'POS' if random.random() > 0.5 else 'ONL'

    def _generate_base_transaction(self, current_timestamp, merchant):
        time_since_last = (current_timestamp - self.last_txn_timestamp).total_seconds()
        transaction_types = ['POS', 'ONL', 'MOB', 'ATM', 'QR']; type_weights = [0.45, 0.35, 0.1, 0.05, 0.05]
        if not self.is_fraudulent_persona and random.random() < 0.85: txn_type = self.preferred_channel
        else: txn_type = random.choices(transaction_types, weights=type_weights, k=1)[0]
        
        if txn_type == 'ATM':
            bank_name = random.choice(EGYPTIAN_BANKS)
            merchant_coords = get_coords(self.home_location_name)
            merchant = {'merchant_id': sha256_hash(bank_name)[:16], 'merchant_name': f"{bank_name} ATM - {self.home_location_name}",'merchant_category': 'Financial Services', 'lat': merchant_coords['lat'], 'lon': merchant_coords['lon'], 'risk_score': 0.1, 'country': 'EG', 'location_name': self.home_location_name}
        
        entry_method_map = {'POS': ['chip', 'swiped', 'contactless_card'],'ONL': ['online', 'manual_keyed'],'MOB': ['contactless_mobile', 'qr_code'],'ATM': ['chip_atm'],'QR': ['qr_code']}
        entry_method = random.choice(entry_method_map[txn_type])
        status_choices = ['approved', 'declined', 'pending']; status_weights = [0.95, 0.04, 0.01]; status = random.choices(status_choices, weights=status_weights, k=1)[0]
        
        is_first_time = merchant['merchant_id'] not in self.merchant_history
        if is_first_time: self.merchant_history[merchant['merchant_id']] = 0
        self.merchant_history[merchant['merchant_id']] += 1
        
        return {'transaction_id': str(uuid.uuid4()),'transaction_timestamp': current_timestamp.isoformat().replace('+00:00', 'Z'),'transaction_amount': 0.0, 'currency': 'EGP', 
                'transaction_type': txn_type,'transaction_status': status, 'transaction_hour_of_day': current_timestamp.hour,
                'customer_id': self.customer_id, 'customer_name': self.customer_name, 'customer_email': self.customer_email, 'customer_email_domain': self.customer_email_domain,
                'customer_tenure_days': self.customer_tenure_days, 'customer_address_change_days': self.customer_address_change_days, 
                'customer_latitude': 0.0, 'customer_longitude': 0.0,
                'card_number_hash': self.card_number_hash, 'card_type': random.choice(['Visa', 'MasterCard', 'Meeza']), 'issuing_bank_name': random.choice(EGYPTIAN_BANKS),
                'card_entry_method': entry_method, 'cvv_match_result': 'match','merchant_id': merchant['merchant_id'], 
                'merchant_name': merchant['merchant_name'],'merchant_category': merchant['merchant_category'], 'merchant_latitude': merchant['lat'],
                'merchant_longitude': merchant['lon'], 'merchant_risk_score': merchant['risk_score'],'ip_address': fake.ipv4(), 'ip_proxy_type': 'none', 
                'device_id': self.current_device,'device_os': self.device_os, 'user_agent': fake.user_agent(),
                'is_international': self.card_issuing_country != merchant['country'],'distance_from_home_km': 0.0, 'distance_from_last_txn_km': 0.0,
                'time_since_last_txn_sec': int(time_since_last) if time_since_last > 0 else 0, 'is_first_time_customer_merchant': is_first_time,'is_fraud': False}
    def generate_transaction(self, current_timestamp, merchant_pool): raise NotImplementedError

# --- Normal Persona ---
class NormalPersona(Persona):
    def generate_transaction(self, current_timestamp, merchant_pool):
        if random.random() < 0.8: merchant = random.choice([m for m in merchant_pool if m.get('location_name') == self.home_location_name] or merchant_pool)
        else: merchant = random.choice(merchant_pool)
        base_txn = self._generate_base_transaction(current_timestamp, merchant)
        
        if base_txn['transaction_type'] in ['POS', 'MOB', 'QR', 'ATM']:
            base_txn['customer_latitude'] = base_txn['merchant_latitude'] + random.uniform(-0.0001, 0.0001); base_txn['customer_longitude'] = base_txn['merchant_longitude'] + random.uniform(-0.0001, 0.0001)
        else: base_txn['customer_latitude'] = self.home_location['lat'] + random.uniform(-0.05, 0.05); base_txn['customer_longitude'] = self.home_location['lon'] + random.uniform(-0.05, 0.05)
        
        base_txn.update({'transaction_amount': max(10.0, round(np.random.normal(loc=self.avg_txn_amount, scale=self.avg_txn_amount * 0.2), 2)),
                         'distance_from_home_km': round(haversine_distance(self.home_location['lat'], self.home_location['lon'], base_txn['customer_latitude'], base_txn['customer_longitude']), 4),
                         'distance_from_last_txn_km': round(haversine_distance(self.last_txn_location['lat'], self.last_txn_location['lon'], base_txn['customer_latitude'], base_txn['customer_longitude']), 4)})
        self.last_txn_timestamp = current_timestamp; self.last_txn_location = {'lat': base_txn['customer_latitude'], 'lon': base_txn['customer_longitude']}; return [base_txn]

# --- ALL 10 FRAUD PERSONAS ---
class FraudPersona_AccountTakeover(Persona):
    def __init__(self): super().__init__(); self.is_fraudulent_persona = True; self.attack_executed = False
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.attack_executed: return []
        merchant = random.choice(merchant_pool); base_txn = self._generate_base_transaction(current_timestamp, merchant)
        fraud_location = get_coords(); base_txn['customer_latitude'] = fraud_location['lat']; base_txn['customer_longitude'] = fraud_location['lon']
        base_txn.update({'transaction_amount': round(self.avg_txn_amount * random.uniform(5, 15), 2),'ip_address': random.choice(FRAUDULENT_IP_POOL), 'ip_proxy_type': 'vpn','device_id': random.choice(FRAUDULENT_DEVICE_POOL), 'is_fraud': True, 'transaction_status': 'approved'}); self.attack_executed = True; return [base_txn]

class FraudPersona_CardTesting(Persona):
    def __init__(self): super().__init__(); self.is_fraudulent_persona = True; self.burst_count = random.randint(4, 10)
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.burst_count <= 0: return []
        merchant = random.choice(merchant_pool); txns, fraud_ip, fraud_device = [], random.choice(FRAUDULENT_IP_POOL), self.current_device
        fraud_location = get_coords()
        for i in range(self.burst_count):
            base_txn = self._generate_base_transaction(current_timestamp, merchant); status = 'declined' if i > 1 and random.random() > 0.3 else 'approved'
            base_txn['customer_latitude'] = fraud_location['lat']; base_txn['customer_longitude'] = fraud_location['lon']
            base_txn.update({'transaction_id': str(uuid.uuid4()), 'transaction_timestamp': (current_timestamp + timedelta(seconds=i*15)).isoformat().replace('+00:00', 'Z'),'transaction_amount': round(random.uniform(10.00, 50.00), 2), 'transaction_status': status,'cvv_match_result': 'no_match' if status == 'declined' else 'match','distance_from_last_txn_km': 0.0, 'ip_address': fraud_ip, 'ip_proxy_type': 'tor','device_id': fraud_device, 'is_fraud': True,}); txns.append(base_txn)
        self.burst_count = 0; return txns

class FraudPersona_VelocityAttack(Persona):
    def __init__(self): super().__init__(); self.customer_tenure_days = random.randint(1, 30); self.is_fraudulent_persona = True; self.burst_count = random.randint(3, 7)
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.burst_count <= 0: return []
        txns, fraud_ip, fraud_device = [], random.choice(FRAUDULENT_IP_POOL), random.choice(FRAUDULENT_DEVICE_POOL)
        for i in range(self.burst_count):
            merchant = random.choice(merchant_pool); base_txn = self._generate_base_transaction(current_timestamp, merchant)
            fraud_location = get_coords(); base_txn['customer_latitude'] = fraud_location['lat']; base_txn['customer_longitude'] = fraud_location['lon']
            base_txn.update({'transaction_id': str(uuid.uuid4()), 'transaction_timestamp': (current_timestamp + timedelta(minutes=i*10)).isoformat().replace('+00:00', 'Z'),'transaction_amount': round(random.uniform(3000, 15000), 2), 'ip_address': fraud_ip, 'ip_proxy_type': 'proxy','device_id': fraud_device, 'is_fraud': True, 'transaction_status': 'approved'}); txns.append(base_txn)
        self.burst_count = 0; return txns

class FraudPersona_ImpossibleTravel(Persona):
    def __init__(self): super().__init__(); self.is_fraudulent_persona = True; self.attack_executed = False
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.attack_executed: return []
        merchant = random.choice([m for m in merchant_pool if m.get('location_name') == self.home_location_name] or merchant_pool); txns = []; 
        first_txn = self._generate_base_transaction(current_timestamp, merchant)
        first_txn['customer_latitude'] = merchant['lat'] + random.uniform(-0.0001, 0.0001); first_txn['customer_longitude'] = merchant['lon'] + random.uniform(-0.0001, 0.0001)
        first_txn.update({'transaction_amount': max(10.0, round(np.random.normal(loc=self.avg_txn_amount, scale=self.avg_txn_amount * 0.2), 2)),'is_fraud': False}); txns.append(first_txn)
        distant_merchant = merchant
        for _ in range(100):
            candidate_merchant = random.choice(merchant_pool)
            if haversine_distance(merchant['lat'], merchant['lon'], candidate_merchant['lat'], candidate_merchant['lon']) >= 450: distant_merchant = candidate_merchant; break
        else: return []
        impossible_timestamp = current_timestamp + timedelta(minutes=random.randint(5, 20)); second_txn = self._generate_base_transaction(impossible_timestamp, distant_merchant)
        second_txn['customer_latitude'] = distant_merchant['lat']; second_txn['customer_longitude'] = distant_merchant['lon']
        second_txn.update({'transaction_amount': round(self.avg_txn_amount * random.uniform(2, 6), 2),'ip_address': random.choice(FRAUDULENT_IP_POOL), 'ip_proxy_type': 'vpn','device_id': random.choice(FRAUDULENT_DEVICE_POOL),
                           'distance_from_last_txn_km': round(haversine_distance(first_txn['customer_latitude'], first_txn['customer_longitude'], second_txn['customer_latitude'], second_txn['customer_longitude']), 4),
                           'time_since_last_txn_sec': (impossible_timestamp - current_timestamp).total_seconds(),'is_fraud': True,}); txns.append(second_txn)
        self.attack_executed = True; return txns

class FraudPersona_MerchantBustOut(Persona):
    def __init__(self, fraudulent_merchant): super().__init__(); self.is_fraudulent_persona = True; self.customer_tenure_days = random.randint(1, 90); self.burst_count = random.randint(2, 5); self.fraudulent_merchant = fraudulent_merchant
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.burst_count <= 0: return []
        txns, fraud_ip, fraud_device = [], fake.ipv4(), str(uuid.uuid4()); fraud_location = get_coords()
        for i in range(self.burst_count):
            base_txn = self._generate_base_transaction(current_timestamp, self.fraudulent_merchant)
            base_txn['customer_latitude'] = fraud_location['lat']; base_txn['customer_longitude'] = fraud_location['lon']
            base_txn.update({'transaction_id': str(uuid.uuid4()), 'transaction_timestamp': (current_timestamp + timedelta(minutes=i*30)).isoformat().replace('+00:00', 'Z'),'transaction_amount': round(random.uniform(2000, 10000), 2), 'ip_address': fraud_ip, 'ip_proxy_type': 'proxy','device_id': fraud_device, 'is_fraud': True, 'transaction_status': 'approved'}); txns.append(base_txn)
        self.burst_count = 0; return txns

class FraudPersona_SpendingAnomaly(Persona):
    def __init__(self): super().__init__(); self.is_fraudulent_persona = True; self.attack_executed = False
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.attack_executed: return []
        unusual_categories = [cat for cat in {m['category'] for m in merchant_pool} if cat not in self.typical_categories];
        if not unusual_categories: return []
        target_category = random.choice(unusual_categories); merchant = random.choice([m for m in merchant_pool if m['category'] == target_category])
        base_txn = self._generate_base_transaction(current_timestamp, merchant)
        fraud_location = get_coords(); base_txn['customer_latitude'] = fraud_location['lat']; base_txn['customer_longitude'] = fraud_location['lon']
        base_txn.update({'transaction_amount': round(self.avg_txn_amount * random.uniform(10, 30), 2),'ip_address': random.choice(FRAUDULENT_IP_POOL), 'ip_proxy_type': 'vpn','device_id': random.choice(FRAUDULENT_DEVICE_POOL),'is_fraud': True, 'transaction_status': 'approved'}); self.attack_executed = True; return [base_txn]

class FraudPersona_SyntheticIdentity(Persona):
    def __init__(self):
        super().__init__(); self.is_fraudulent_persona = True; self.customer_tenure_days = random.randint(1, 15); self.customer_email = create_realistic_email(self.customer_name, domains=HIGH_RISK_DOMAINS); self.customer_email_domain = self.customer_email.split('@')[1]; self.customer_address_change_days = self.customer_tenure_days; self.warmup_txns = random.randint(2, 4); self.cashout_executed = False
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.cashout_executed: return []
        if self.warmup_txns > 0:
            self.warmup_txns -= 1
            return NormalPersona.generate_transaction(self, current_timestamp, merchant_pool)
        else:
            merchant = random.choice([m for m in merchant_pool if m['category'] in ['Electronics', 'Fashion']] or merchant_pool); base_txn = self._generate_base_transaction(current_timestamp, merchant)
            fraud_location = get_coords(); base_txn['customer_latitude'] = fraud_location['lat']; base_txn['customer_longitude'] = fraud_location['lon']
            base_txn.update({'transaction_amount': round(random.uniform(10000, 25000), 2), 'is_fraud': True, 'transaction_status': 'approved'}); self.cashout_executed = True; return [base_txn]

class FraudPersona_AnomalousHour(Persona):
    def __init__(self): super().__init__(); self.is_fraudulent_persona = True; self.attack_executed = False
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.attack_executed: return []
        fraud_hour = random.randint(2, 5); fraud_time = current_timestamp.replace(hour=fraud_hour, minute=random.randint(0, 59)) if current_timestamp.hour not in range(2, 6) else current_timestamp
        merchant = random.choice(merchant_pool); base_txn = self._generate_base_transaction(fraud_time, merchant)
        fraud_location = get_coords(); base_txn['customer_latitude'] = fraud_location['lat']; base_txn['customer_longitude'] = fraud_location['lon']
        base_txn.update({'transaction_amount': round(self.avg_txn_amount * random.uniform(3, 8), 2),'ip_address': random.choice(FRAUDULENT_IP_POOL), 'ip_proxy_type': 'proxy','is_fraud': True, 'transaction_status': 'approved'}); self.attack_executed = True; return [base_txn]

class FraudPersona_AddressChange(Persona):
    def __init__(self):
        super().__init__(); self.is_fraudulent_persona = True; self.customer_address_change_days = random.randint(0, 1); self.attack_executed = False
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.attack_executed: return []
        merchant = random.choice([m for m in merchant_pool if m['category'] == 'Electronics'] or merchant_pool); base_txn = self._generate_base_transaction(current_timestamp, merchant)
        base_txn['transaction_type'] = 'ONL'; base_txn['card_entry_method'] = 'online'
        fraud_location = get_coords(); base_txn['customer_latitude'] = fraud_location['lat']; base_txn['customer_longitude'] = fraud_location['lon']
        base_txn.update({'transaction_amount': round(self.avg_txn_amount * random.uniform(8, 20), 2),'ip_address': random.choice(FRAUDULENT_IP_POOL),'ip_proxy_type': 'vpn','is_fraud': True, 'transaction_status': 'approved'}); self.attack_executed = True; return [base_txn]

class FraudPersona_ChannelPivot(Persona):
    def __init__(self):
        super().__init__(); self.is_fraudulent_persona = True; self.preferred_channel = 'POS'; self.attack_executed = False
    def generate_transaction(self, current_timestamp, merchant_pool):
        if self.attack_executed: return []
        merchant = random.choice(merchant_pool); base_txn = self._generate_base_transaction(current_timestamp, merchant)
        base_txn['transaction_type'] = 'ONL'; base_txn['card_entry_method'] = 'online'
        fraud_location = get_coords(); base_txn['customer_latitude'] = fraud_location['lat']; base_txn['customer_longitude'] = fraud_location['lon']
        base_txn.update({'transaction_amount': round(self.avg_txn_amount * random.uniform(5, 15), 2),'device_id': random.choice(FRAUDULENT_DEVICE_POOL),'is_fraud': True, 'transaction_status': 'approved'}); self.attack_executed = True; return [base_txn]

# --- Simulator Class ---
class Simulator:
    def __init__(self):
        self.personas = {}; self.merchant_pool = self._create_merchant_pool(NUM_INITIAL_MERCHANTS, is_fraud=False); self.fraud_merchant_pool = self._create_merchant_pool(NUM_FRAUD_MERCHANTS, is_fraud=True)
        self.schema_header = ['transaction_id', 'transaction_timestamp', 'transaction_amount', 'currency', 'transaction_type', 'transaction_status', 'transaction_hour_of_day',
                              'customer_id', 'customer_name', 'customer_email', 'customer_email_domain', 'customer_tenure_days', 'customer_address_change_days',
                              'customer_latitude', 'customer_longitude',
                              'card_number_hash', 'card_type', 'issuing_bank_name', 'card_entry_method', 'cvv_match_result',
                              'merchant_id', 'merchant_name', 'merchant_category', 'merchant_latitude', 'merchant_longitude', 'merchant_risk_score',
                              'ip_address', 'ip_proxy_type', 'device_id', 'device_os', 'user_agent','is_international', 
                              'distance_from_home_km', 'distance_from_last_txn_km', 'time_since_last_txn_sec', 'is_first_time_customer_merchant','is_fraud']
        with open(OUTPUT_CSV_FILE, mode='w', newline='', encoding='utf-8') as file: writer = csv.DictWriter(file, fieldnames=self.schema_header); writer.writeheader()
        print(f"Initialized '{OUTPUT_CSV_FILE}'.")

    def _create_merchant_pool(self, num_merchants, is_fraud=False):
        pool = [];
        for _ in range(num_merchants):
            location_name = random.choice(EGYPTIAN_LOCATIONS)
            coords = get_coords(location_name)
            if is_fraud:
                merchant_template = {'name': 'Fraudulent Web Services', 'category': 'Services'}
                merchant_name = f"{merchant_template['name']} {random.randint(100,999)}"
            else:
                merchant_template = random.choice(EGYPTIAN_MERCHANTS)
                merchant_name = f"{merchant_template['name']} - {location_name}"

            pool.append({'merchant_id': str(uuid.uuid4()), 'merchant_name': merchant_name,
                         'merchant_category': merchant_template['category'], 'lat': coords['lat'], 'lon': coords['lon'],
                         'location_name': location_name,
                         'risk_score': round(random.uniform(0.85, 0.99), 3) if is_fraud else round(random.uniform(0.01, 0.4), 3),
                         'country': 'EG'})
        print(f"Created a pool of {len(pool)} {'fraudulent' if is_fraud else 'legitimate'} merchants.")
        return pool

    def _get_or_create_persona(self):
        if len(self.personas) < 200 or random.random() < 0.15:
            if random.random() < FRAUD_PERSONA_RATE:
                fraud_types = [
                    FraudPersona_AccountTakeover, FraudPersona_CardTesting, FraudPersona_VelocityAttack, FraudPersona_ImpossibleTravel,
                    FraudPersona_MerchantBustOut, FraudPersona_SpendingAnomaly, FraudPersona_SyntheticIdentity, FraudPersona_AnomalousHour,
                    FraudPersona_AddressChange, FraudPersona_ChannelPivot
                ]
                persona_type = random.choice(fraud_types)
                if persona_type == FraudPersona_MerchantBustOut: new_persona = persona_type(fraudulent_merchant=random.choice(self.fraud_merchant_pool))
                else: new_persona = persona_type()
            else: new_persona = NormalPersona()
            self.personas[new_persona.customer_id] = new_persona; return new_persona
        else: return random.choice(list(self.personas.values()))

    def run(self, num_transactions):
        written_count, start_time = 0, time.time()
        
        total_seconds_in_interval = (END_DATE - START_DATE).total_seconds()
        average_time_increment = total_seconds_in_interval / num_transactions
        current_simulation_time = START_DATE
        
        while written_count < num_transactions:
            try:
                valid_personas = [p for p in self.personas.values() if p.last_txn_timestamp < current_simulation_time]
                if not valid_personas or random.random() < 0.2: 
                    persona = self._get_or_create_persona()
                else:
                    persona = random.choice(valid_personas)

                if (hasattr(persona, 'attack_executed') and persona.attack_executed) or \
                   (hasattr(persona, 'burst_count') and persona.burst_count <= 0) or \
                   (hasattr(persona, 'cashout_executed') and persona.cashout_executed):
                    if persona.customer_id in self.personas:
                        del self.personas[persona.customer_id]
                    continue
                
                transactions = persona.generate_transaction(current_simulation_time, self.merchant_pool)
                if not transactions: continue
                
                with open(OUTPUT_CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=self.schema_header)
                    for txn in transactions:
                        if written_count >= num_transactions: break
                        writer.writerow({h: txn.get(h, None) for h in self.schema_header}); fraud_label = "FRAUD" if txn.get('is_fraud') else "Normal"
                        print(f"[{written_count+1}/{num_transactions}] Wrote txn {txn['transaction_id'][:8]}... | Time: {txn['transaction_timestamp']} | {fraud_label}")
                        written_count += 1
                
                time_increment_seconds = max(1, average_time_increment * (1 + random.uniform(-0.5, 1.5)))
                current_simulation_time += timedelta(seconds=time_increment_seconds)
                if current_simulation_time > END_DATE: 
                    current_simulation_time = START_DATE + timedelta(days=random.randint(1,5))

            except KeyError: continue
            except Exception as e: print(f"An unexpected error occurred: {e}"); time.sleep(1)
            
        print(f"\n--- Simulation Complete ---\nGenerated {written_count} transactions to '{OUTPUT_CSV_FILE}'.")
        print(f"Time range: {START_DATE.isoformat()} to {END_DATE.isoformat()}")
        print(f"Total time to generate: {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    simulator = Simulator()
    simulator.run(num_transactions=NUM_TRANSACTIONS)