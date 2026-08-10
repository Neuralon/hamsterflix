import express from 'express';
import sqlite3 from 'sqlite3';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3002;

// Fetch real movies
app.get('/api/movies', (req, res) => {
  const dbPath = path.join(__dirname, '../hamsterflix.db');
  
  if (!fs.existsSync(dbPath)) {
    return res.json([]);
  }

  // Load the trailer scripts to pull the inspiration metadata
  const scriptsPath = path.join(__dirname, 'public/trailer_scripts.json');
  let scriptsData = [];
  try {
    scriptsData = JSON.parse(fs.readFileSync(scriptsPath, 'utf8'));
  } catch(e) {}
  
  const getInspiration = (uid) => {
    const s = scriptsData.find(x => x.uid === uid);
    return s ? s.inspiration : null;
  };

  const db = new sqlite3.Database(dbPath);
  db.all('SELECT * FROM real_movies', [], (err, realRows) => {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'DB Error' });
    } else {
      const processedReal = (realRows || []).map(r => ({
        ...r,
        id: r.uid, // 32-character string UUID
        img: `/posters_real/${r.poster_filename}`,
        genres: JSON.parse(r.genres || '[]'),
        mood: JSON.parse(r.mood || '[]'),
        inspiration: getInspiration(r.uid)
      }));
      
      // Also fetch fake movies
      db.all('SELECT * FROM movies', [], (err, fakeRows) => {
          if (err) {
              res.json(processedReal);
          } else {
              const processedFake = (fakeRows || []).map(r => ({
                  ...r,
                  id: r.uid, // 32-character string UUID
                  img: `/posters_ai/poster_${r.id}.png?v=${Date.now()}`,
                  genres: JSON.parse(r.genres || '[]'),
                  mood: JSON.parse(r.mood || '[]'),
                  inspiration: getInspiration(r.uid)
              }));
              // Serve real movies first so the initial featured poster is from the real set
              res.json([...processedReal, ...processedFake]);
          }
          db.close();
      });
    }
  });
});

app.get('/api/movies/:id', (req, res) => {
  const dbPath = path.join(__dirname, '../hamsterflix.db');
  const db = new sqlite3.Database(dbPath);
  
  const uid = req.params.id; // 32-character string UUID
  
  // Load scripts for inspiration
  const scriptsPath = path.join(__dirname, 'public/trailer_scripts.json');
  let scriptsData = [];
  try {
    scriptsData = JSON.parse(fs.readFileSync(scriptsPath, 'utf8'));
  } catch(e) {}
  const inspiration = scriptsData.find(x => x.uid === uid)?.inspiration || null;
  
  db.get('SELECT * FROM real_movies WHERE uid = ?', [uid], (err, row) => {
    if (row) {
      row.id = row.uid;
      row.img = `/posters_real/${row.poster_filename}`;
      row.genres = JSON.parse(row.genres || '[]');
      row.mood = JSON.parse(row.mood || '[]');
      row.inspiration = inspiration;
      res.json(row);
      db.close();
    } else {
      // Check fake movies
      db.get('SELECT * FROM movies WHERE uid = ?', [uid], (err, fakeRow) => {
          if (fakeRow) {
              fakeRow.img = `/posters_ai/poster_${fakeRow.id}.png?v=${Date.now()}`; // Use original id before overwriting
              fakeRow.id = fakeRow.uid;
              fakeRow.genres = JSON.parse(fakeRow.genres || '[]');
              fakeRow.mood = JSON.parse(fakeRow.mood || '[]');
              fakeRow.inspiration = inspiration;
              res.json(fakeRow);
          } else {
              res.status(404).json({ error: 'Not found' });
          }
          db.close();
      });
    }
  });
});

app.get('/api/report', (req, res) => {
  const dbPath = path.join(__dirname, '../hamsterflix.db');
  const db = new sqlite3.Database(dbPath);
  
  // Load scripts
  const scriptsPath = path.join(__dirname, 'public/trailer_scripts.json');
  let scriptsData = [];
  try {
    scriptsData = JSON.parse(fs.readFileSync(scriptsPath, 'utf8'));
  } catch(e) {}

  const durationCache = app.locals.durationCache || {};
  app.locals.durationCache = durationCache;

  const getDuration = (filePath) => {
    if (!fs.existsSync(filePath)) return '-';
    const stats = fs.statSync(filePath);
    if (stats.size < 1000) return '-';
    const cacheKey = filePath + '_' + stats.mtimeMs;
    if (durationCache[cacheKey]) return durationCache[cacheKey];
    
    try {
      const out = execSync(`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${filePath}"`, {stdio: 'pipe'});
      const secs = parseFloat(out.toString().trim());
      if (isNaN(secs)) return '-';
      const m = Math.floor(secs / 60);
      const s = Math.floor(secs % 60);
      const formatted = `${m}:${s.toString().padStart(2, '0')}`;
      durationCache[cacheKey] = formatted;
      return formatted;
    } catch(e) {
      return '-';
    }
  };

  const getReportData = (rows, type) => {
    return rows.map(r => {
      const uid = r.uid;
      const hasScript = scriptsData.some(s => s.uid === uid);
      
      let trailerStatus = 'Missing';
      const trailerPath = path.join(__dirname, `public/trailers/trailer_${uid}.mp4`);
      let trailerLen = '-';
      if (fs.existsSync(trailerPath)) {
        const stats = fs.statSync(trailerPath);
        if (stats.size > 8000000) { // >8MB indicates a completed multi-scene Veo trailer (even if <40s)
          trailerStatus = 'Ready (Veo)';
        } else if (stats.size > 1000000) { // 1MB-8MB indicates partial or generic 15s trailer
          trailerStatus = 'Partial / Generic';
        }
        trailerLen = getDuration(trailerPath);
      }
      
      let musicStatus = 'Missing';
      let musicLen = '-';
      const themePath = path.join(__dirname, `public/trailers/theme_${uid}.mp3`);
      const customMusicFiles = fs.readdirSync(path.join(__dirname, 'public/trailers')).filter(f => f.startsWith(`bgm_${uid}`) && f.endsWith('.mp3'));
      if (fs.existsSync(themePath) && fs.statSync(themePath).size > 1000) {
        musicStatus = 'Real Soundtrack';
        musicLen = getDuration(themePath);
      } else if (customMusicFiles.length > 0) {
        musicStatus = 'Synth';
        musicLen = getDuration(path.join(__dirname, `public/trailers/${customMusicFiles[0]}`));
      } else {
        const epicPath = path.join(__dirname, 'public/trailers/epic_music.mp3');
        if (fs.existsSync(epicPath)) {
          musicStatus = 'Placeholder';
        }
      }
      
      let voStatus = 'Missing';
      let voLen = '-';
      const voV2Path = path.join(__dirname, `public/voiceovers/${uid}_v2.mp3`);
      const voV1Path = path.join(__dirname, `public/voiceovers/${uid}.mp3`);
      if (fs.existsSync(voV2Path) && fs.statSync(voV2Path).size > 1000) {
        voStatus = 'Ready';
        voLen = getDuration(voV2Path);
      } else if (fs.existsSync(voV1Path) && fs.statSync(voV1Path).size > 1000) {
        voStatus = 'Ready (Old)';
        voLen = getDuration(voV1Path);
      }
      
      let actorImagesCount = 0;
      try {
        const cast = JSON.parse(r.cast || '[]');
        cast.forEach(c => {
          const imgPath = path.join(__dirname, 'public', c.img.replace(/^\//, ''));
          if (fs.existsSync(imgPath) && fs.statSync(imgPath).size > 1000) {
            actorImagesCount++;
          }
        });
      } catch (e) {}

      return { uid, title: r.title, type, hasScript, trailerStatus, trailerLen, actorImagesCount, musicStatus, musicLen, voStatus, voLen, approved: r.approved || 0, notes: r.notes || '' };
    });
  };

  db.all('SELECT uid, title, "cast", approved, notes FROM real_movies', [], (err, realRows) => {
    const realReport = getReportData(realRows || [], 'Real');
    db.all('SELECT uid, title, "cast", approved, notes FROM movies', [], (err, fakeRows) => {
      const fakeReport = getReportData(fakeRows || [], 'Fake');
      res.json([...realReport, ...fakeReport]);
      db.close();
    });
  });
});

app.post('/api/movies/:uid/approve', express.json(), (req, res) => {
  const uid = req.params.uid;
  const approved = req.body.approved ? 1 : 0;
  const dbPath = path.join(__dirname, '../hamsterflix.db');
  const db = new sqlite3.Database(dbPath);
  
  db.run('UPDATE real_movies SET approved = ? WHERE uid = ?', [approved, uid], (err) => {
    db.run('UPDATE movies SET approved = ? WHERE uid = ?', [approved, uid], (err2) => {
      res.json({ success: true, approved });
      db.close();
    });
  });
});

app.post('/api/movies/:uid/notes', express.json(), (req, res) => {
  const uid = req.params.uid;
  const notes = req.body.notes || '';
  const dbPath = path.join(__dirname, '../hamsterflix.db');
  const db = new sqlite3.Database(dbPath);
  
  db.run('UPDATE real_movies SET notes = ? WHERE uid = ?', [notes, uid], (_err) => {
    db.run('UPDATE movies SET notes = ? WHERE uid = ?', [notes, uid], (_err2) => {
      res.json({ success: true, notes });
      db.close();
    });
  });
});

app.use(express.static(path.join(__dirname, 'dist')));

// SPA fallback for React Router
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'dist/index.html'));
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
