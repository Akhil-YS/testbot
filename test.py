import requests

full_path = "https://youngsoft.com/ritwik_employee/details.php?func=getEmpByName&empName=Priyanka"
results = requests.get(full_path).json()