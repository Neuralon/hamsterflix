import sqlite3 from 'sqlite3';
const db = new sqlite3.Database('/Users/ckaplan/dev/neuralon/hamster/hamsterflix.db');
db.get("SELECT * FROM movies WHERE uid = 'a03b40866cdd47caa326f0ad95375308'", (err, row) => {
  console.log("Fake Error:", err);
  console.log("Fake Row:", row);
});
