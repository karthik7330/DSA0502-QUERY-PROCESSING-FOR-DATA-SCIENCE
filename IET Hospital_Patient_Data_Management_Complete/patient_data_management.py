
import csv
import re
import sqlite3
from difflib import SequenceMatcher
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB = BASE_DIR / "patient_database.db"
TEST_CSV = BASE_DIR / "test_patient_data.csv"

PHONE_RE = re.compile(r"^\+?[0-9]{10,15}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")
FIELDS = ["Patient_ID","Name","Age","Gender","Phone","Email","Diagnosis"]
GENDER = {"male":"Male","m":"Male","female":"Female","f":"Female","other":"Other","o":"Other"}

SAMPLE = [
(1,"RAHUL kumar",35,"male","9876543210","rahul@gmail.com","Diabetes"),
(2,"rahul KUMAR",35,"M","9876543210","rahul@gmail.com","Diabetes"),
(3,"Priya SHARMA",28,"Female","9876543211","priya@gmail.com","Hypertension"),
(4,"priya sharma",28,"f","9876543211","priya@gmail.com","Hypertension"),
(5,"Arun Kumar",-5,"Male","9876543212","arun@gmail.com","Asthma"),
(6,"Meena Devi",130,"FEMALE","98765432","meena@gmail.com","Migraine"),
(7,"Vijay Raj",42,"male","9876543213","","Heart Disease"),
(8,"Anitha",31,"female","","anitha@gmail.com","Diabetes"),
(9,"SURESH babu",55,"MALE","9876543214","suresh@gmail.com","Diabetes"),
(10,"Suresh Babu",55,"Male","9876543214","suresh@gmail.com","Diabetes"),
(11,"Kavya Nair",25,"Female","9876543215","kavya@gmail.com","Thyroid"),
(12,"Ravi",150,"male","abcdefghij","ravi@example.com","Fever")]

UNSEEN = [
(101,"  rahul KUMAR ",35,"M","+91-9876543210","rahul@gmail.com","Diabetes"),
(102,"Priya sharma",28,"female","9876543211","priya@gmail.com","Hypertension"),
(103,"John Doe",45,"M","9876543216","john.doe@example.com","Asthma"),
(104,"Anu",22,"F","","anu@example.com","Fever"),
(105,"Test Invalid",121,"female","9876543217","test@example.com","Fever"),
(106,"Another Invalid",30,"female","12345","","Cold")]

def connect():
    try:
        c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
        print("[OK] Database connection successful."); return c
    except sqlite3.Error as e:
        print("[ERROR] Connection failed:",e); return None

def create_tables(c):
    c.execute("""CREATE TABLE IF NOT EXISTS Patient(
        Patient_ID INTEGER PRIMARY KEY, Name TEXT, Age INTEGER, Gender TEXT,
        Phone TEXT, Email TEXT, Diagnosis TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS Clean_Patient(
        Patient_ID INTEGER PRIMARY KEY, Name TEXT NOT NULL, Age INTEGER NOT NULL,
        Gender TEXT NOT NULL, Phone TEXT, Email TEXT, Diagnosis TEXT NOT NULL,
        Clean_Status TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS Cleaning_Log(
        Log_ID INTEGER PRIMARY KEY AUTOINCREMENT, Patient_ID INTEGER,
        Issue TEXT, Action TEXT)""")
    c.commit(); print("[OK] Patient, Clean_Patient and Cleaning_Log tables are ready.")

def insert_records(c,records):
    c.executemany("INSERT OR REPLACE INTO Patient VALUES(?,?,?,?,?,?,?)",records)
    c.commit(); print(f"[OK] {len(records)} records inserted into Patient.")

def name_clean(x):
    x="" if x is None else str(x); x=re.sub(r"\s+"," ",x.strip())
    return " ".join(w.capitalize() for w in x.split())

def gender_clean(x):
    return GENDER.get(str(x).strip().lower(),"") if x is not None else ""

def phone_clean(x):
    if x is None: return ""
    d=re.sub(r"\D","",str(x))
    if d.startswith("91") and len(d)==12: d=d[2:]
    return d

def email_clean(x): return "" if x is None else str(x).strip().lower()

def diagnosis_clean(x):
    x="" if x is None else str(x); x=re.sub(r"\s+"," ",x.strip())
    return " ".join(w.capitalize() for w in x.split())

def age_valid(x):
    try: return 0<=int(x)<=120
    except (TypeError,ValueError): return False

def phone_valid(x): return bool(x) and bool(PHONE_RE.fullmatch(x))
def email_valid(x): return bool(x) and bool(EMAIL_RE.fullmatch(x))

def exact_duplicates(rows):
    seen=set(); dup=[]
    for r in rows:
        key=(name_clean(r["Name"]).lower(),phone_clean(r["Phone"]),email_clean(r["Email"]),
             r["Age"],gender_clean(r["Gender"]),diagnosis_clean(r["Diagnosis"]).lower())
        if key in seen: dup.append(r["Patient_ID"])
        else: seen.add(key)
    return dup

def fuzzy_pairs(rows,threshold=.88):
    out=[]
    for i,a in enumerate(rows):
        for b in rows[i+1:]:
            score=SequenceMatcher(None,name_clean(a["Name"]).lower(),name_clean(b["Name"]).lower()).ratio()
            pa,pb=phone_clean(a["Phone"]),phone_clean(b["Phone"])
            ea,eb=email_clean(a["Email"]),email_clean(b["Email"])
            identifier=(pa and pb and pa==pb) or (ea and eb and ea==eb)
            if identifier and score>=.80: out.append((a["Patient_ID"],b["Patient_ID"],round(score,3)))
            elif score>=threshold: out.append((a["Patient_ID"],b["Patient_ID"],round(score,3)))
    return out

def log(c,pid,issue,action):
    c.execute("INSERT INTO Cleaning_Log(Patient_ID,Issue,Action) VALUES(?,?,?)",(pid,issue,action))

def clean_table(c,source="Patient",clear=True):
    rows=c.execute(f"SELECT * FROM {source} ORDER BY Patient_ID").fetchall()
    if clear:
        c.execute("DELETE FROM Clean_Patient"); c.execute("DELETE FROM Cleaning_Log")
    seen=set(); clean=[]; rejected=[]
    for r in rows:
        pid=r["Patient_ID"]; n=name_clean(r["Name"]); a=r["Age"]; g=gender_clean(r["Gender"])
        p=phone_clean(r["Phone"]); e=email_clean(r["Email"]); d=diagnosis_clean(r["Diagnosis"])
        if not n: log(c,pid,"Missing name","Record excluded")
        if not age_valid(a): log(c,pid,"Invalid age","Record excluded")
        if not g: log(c,pid,"Invalid/missing gender","Record excluded")
        if p and not phone_valid(p): log(c,pid,"Invalid phone","Phone set to NULL"); p=""
        if e and not email_valid(e): log(c,pid,"Invalid email","Email set to NULL"); e=""
        if not p: log(c,pid,"Missing phone","Retained as NULL")
        if not e: log(c,pid,"Missing email","Retained as NULL")
        if not d: log(c,pid,"Missing diagnosis","Record excluded")
        key=(n.lower(),p,e,a,g,d.lower()); duplicate=key in seen
        if duplicate: log(c,pid,"Exact duplicate","Duplicate record excluded")
        invalid=(not n or not age_valid(a) or not g or not d or duplicate)
        if invalid: rejected.append(pid); continue
        seen.add(key)
        clean.append((pid,n,int(a),g,p or None,e or None,d,"Validated"))
    c.executemany("""INSERT OR REPLACE INTO Clean_Patient
        (Patient_ID,Name,Age,Gender,Phone,Email,Diagnosis,Clean_Status)
        VALUES(?,?,?,?,?,?,?,?)""",clean)
    c.commit(); return rows,clean,rejected

def crud(c):
    print("\n--- SQL CRUD ---\nSELECT:")
    for r in c.execute("SELECT * FROM Clean_Patient ORDER BY Patient_ID LIMIT 5"): print(dict(r))
    c.execute("UPDATE Clean_Patient SET Diagnosis='Diabetes' WHERE LOWER(Diagnosis)='diabetes'"); c.commit()
    print("UPDATE executed successfully.")
    c.execute("DELETE FROM Clean_Patient WHERE Age<0 OR Age>120"); c.commit()
    print("DELETE executed successfully.")

def make_csv():
    with TEST_CSV.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(FIELDS); w.writerows(UNSEEN)

def unseen_test(c):
    print("\n--- UNSEEN DATA TEST ---"); make_csv()
    c.execute("DROP TABLE IF EXISTS Unseen_Test_Patient")
    c.execute("""CREATE TABLE Unseen_Test_Patient(
        Patient_ID INTEGER PRIMARY KEY,Name TEXT,Age INTEGER,Gender TEXT,
        Phone TEXT,Email TEXT,Diagnosis TEXT)""")
    c.executemany("INSERT INTO Unseen_Test_Patient VALUES(?,?,?,?,?,?,?)",UNSEEN); c.commit()
    rows,clean,rejected=clean_table(c,"Unseen_Test_Patient",False)
    print("Input:",len(rows)," Accepted:",len(clean)," Rejected:",len(rejected))
    print("Rejected IDs:",rejected)
    clean_table(c,"Patient",True)
    c.execute("DROP TABLE Unseen_Test_Patient"); c.commit()
    passed=len(clean)==5 and len(rejected)==1
    print("Unseen-data test:","PASS" if passed else "REVIEW REQUIRED")
    return passed

def main():
    print("="*55); print("HOSPITAL PATIENT DATA MANAGEMENT"); print("="*55)
    c=connect()
    if not c: return
    try:
        create_tables(c); insert_records(c,SAMPLE)
        rows=c.execute("SELECT * FROM Patient ORDER BY Patient_ID").fetchall()
        print("\nExact duplicate IDs:",exact_duplicates(rows))
        pairs=fuzzy_pairs(rows); print("\nPotential fuzzy duplicates:")
        for pair in pairs: print(" ",pair)
        _,clean,rejected=clean_table(c)
        print("\nCleaning complete."); print("Original:",len(rows)," Clean:",len(clean)," Excluded:",len(rejected))
        print("Excluded IDs:",rejected); crud(c); unseen_test(c)
        print("\n--- FINAL SUMMARY ---")
        print("Patient records:",c.execute("SELECT COUNT(*) FROM Patient").fetchone()[0])
        print("Clean_Patient records:",c.execute("SELECT COUNT(*) FROM Clean_Patient").fetchone()[0])
        print("Cleaning log entries:",c.execute("SELECT COUNT(*) FROM Cleaning_Log").fetchone()[0])
        print("Fuzzy candidate pairs:",len(pairs))
    finally:
        c.close(); print("\n[OK] Database connection closed.")

if __name__=="__main__": main()
