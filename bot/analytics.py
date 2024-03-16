from database import Database

db_c = Database()

db = db_c.get_db()

print()

print(f'TOTAL COUNT OF USERS: {len(db)}')
print(f'TOTAL COUNT OF TESTS: {sum([st[-1]["passCount"] for st in db])}')

print()

print(*db, sep='\n')

