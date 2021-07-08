print('###############Start init mongo test database###############')

conn = new Mongo();
db = conn.getDB('animal-cards-test');
db.createUser({
  user: "test",
  pwd: "BXxcRbi8csvha5DQ",
  roles: [{ role: 'readWrite', db: 'animal-cards-test' }]
});
db.createCollection('users');

print('###############End init mongo database###############')