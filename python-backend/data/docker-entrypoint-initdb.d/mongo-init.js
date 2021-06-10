print('###############Start init mongo database###############')

conn = new Mongo();
db = conn.getDB('animal-cards');
db.createUser({
  user: "dev",
  pwd: "BXxcRbi8csvha5DQ",
  roles: [{ role: 'readWrite', db: 'animal-cards' }]
});
db.createCollection('users');

print('###############End init mongo database###############')