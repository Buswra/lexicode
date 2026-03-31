"""
LexiCode — Disleksi Dostu İngilizce Öğrenme Uygulaması
Python 3 + Flask + SQLite
"""
from flask import Flask, jsonify, request, Response
import json
import logging
import os
import random
import sqlite3
from datetime import datetime, timedelta

try:
    from .config import (
        APP_NAME,
        APP_VERSION,
        CLAUDE_MODEL,
        DB_PATH,
        DEBUG,
        DEFAULT_HOST,
        DEFAULT_PORT,
        RESOURCE_DIR,
    )
    from .services.tts_service import clean_tts_text, generate_tts_audio
    from .utils.responses import api_error
    from .words import WORDS as BASE_WORDS
    from .words_cs import CS_WORDS
except ImportError:
    from config import (
        APP_NAME,
        APP_VERSION,
        CLAUDE_MODEL,
        DB_PATH,
        DEBUG,
        DEFAULT_HOST,
        DEFAULT_PORT,
        RESOURCE_DIR,
    )
    from services.tts_service import clean_tts_text, generate_tts_audio
    from utils.responses import api_error
    from words import WORDS as BASE_WORDS
    from words_cs import CS_WORDS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("lexicode")

app = Flask(
    __name__,
    template_folder=os.path.join(RESOURCE_DIR, "templates"),
    static_folder=os.path.join(RESOURCE_DIR, "static"),
)
app.config["JSON_AS_ASCII"] = False
app.config["SECRET_KEY"] = os.getenv("LEXICODE_SECRET_KEY", "lexicode-dev-secret")
DB = str(DB_PATH)

# ── kelimeleri buraya import et ──
DAILY_WORDS = [w for w in BASE_WORDS if w.get("mod") == "daily"]
WORDS = CS_WORDS + DAILY_WORDS

# ═══════════════════════════════════════════════════════
# VERİTABANI
# ═══════════════════════════════════════════════════════
def init_db():
    c = get_conn()
    c.execute("""CREATE TABLE IF NOT EXISTS progress (
        word_id INTEGER PRIMARY KEY, word TEXT, mod TEXT, level TEXT,
        learned INTEGER DEFAULT 0, skipped INTEGER DEFAULT 0,
        correct_count INTEGER DEFAULT 0, wrong_count INTEGER DEFAULT 0,
        last_seen TEXT, first_learned TEXT,
        next_review TEXT, review_interval INTEGER DEFAULT 1)""")
    c.execute("""CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS badges (badge_id TEXT PRIMARY KEY, earned_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS daily_log (
        date TEXT PRIMARY KEY,
        cs_studied INTEGER DEFAULT 0, daily_studied INTEGER DEFAULT 0,
        quiz_score INTEGER DEFAULT 0)""")
    for k,v in [("xp","0"),("streak","0"),("last_study",""),
                ("daily_goal","10"),("streak_goal","7"),
                ("active_mod","cs"),("active_level",""),("focus_mode","0")]:
        c.execute("INSERT OR IGNORE INTO settings VALUES (?,?)", (k,v))
    c.execute("UPDATE settings SET value='' WHERE key='active_level' AND value='A1'")
    c.connection.commit(); c.connection.close()

def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn.cursor()

def get_s(k, d=""):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (k,))
    r = c.fetchone(); conn.close()
    return r[0] if r else d

def set_s(k, v):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings VALUES (?,?)", (k,str(v)))
    conn.commit(); conn.close()

def get_progress():
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT word_id,learned,skipped,correct_count,wrong_count,next_review,review_interval FROM progress")
    rows = c.fetchall(); conn.close()
    return {r[0]:{"learned":r[1],"skipped":r[2],"correct":r[3],"wrong":r[4],"next_review":r[5],"interval":r[6]} for r in rows}

def get_learned_count(mod=None):
    conn = sqlite3.connect(DB); c = conn.cursor()
    if mod:
        c.execute("SELECT COUNT(*) FROM progress WHERE learned=1 AND mod=?", (mod,))
    else:
        c.execute("SELECT COUNT(*) FROM progress WHERE learned=1")
    n = c.fetchone()[0]; conn.close(); return n

def add_xp(n):
    xp = int(get_s("xp","0")) + n; set_s("xp", xp); return xp

def update_spaced(word_id, correct):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT review_interval FROM progress WHERE word_id=?", (word_id,))
    row = c.fetchone()
    iv = row[0] if row else 1
    if correct:
        iv = {1:3,3:7,7:14,14:30}.get(iv, min(iv*2,30))
    else:
        iv = 1
    nr = (datetime.now().date() + timedelta(days=iv)).isoformat()
    c.execute("""INSERT INTO progress(word_id,review_interval,next_review) VALUES(?,?,?)
                 ON CONFLICT(word_id) DO UPDATE SET review_interval=?,next_review=?""",
              (word_id,iv,nr,iv,nr))
    conn.commit(); conn.close()

def get_due_ids():
    today = datetime.now().date().isoformat()
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT word_id FROM progress WHERE learned=1 AND next_review<=?", (today,))
    ids = {r[0] for r in c.fetchall()}; conn.close(); return ids

def get_weak_ids(limit=20):
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT word_id FROM progress WHERE wrong_count>0 ORDER BY wrong_count DESC LIMIT ?", (limit,))
    ids = {r[0] for r in c.fetchall()}; conn.close(); return ids

BADGES_DEF = [
    {"id":"first",  "icon":"👶","name":"İlk Adım",       "desc":"İlk kelimeyi öğrendiniz",        "req":lambda lc,ls,qp:lc>=1},
    {"id":"five",   "icon":"🌱","name":"5 Kelime",        "desc":"5 kelime öğrendiniz",            "req":lambda lc,ls,qp:lc>=5},
    {"id":"ten",    "icon":"🔟","name":"10 Kelime",       "desc":"10 kelime öğrendiniz",           "req":lambda lc,ls,qp:lc>=10},
    {"id":"s3",     "icon":"🔥","name":"3 Günlük Seri",   "desc":"3 gün üst üste çalıştınız",     "req":lambda lc,ls,qp:ls>=3},
    {"id":"s7",     "icon":"📅","name":"Haftalık Seri",   "desc":"7 gün üst üste çalıştınız",     "req":lambda lc,ls,qp:ls>=7},
    {"id":"fifty",  "icon":"🏆","name":"50 Kelime",       "desc":"50 kelime öğrendiniz",           "req":lambda lc,ls,qp:lc>=50},
    {"id":"qa",     "icon":"🎯","name":"Quiz Ustası",     "desc":"Quizden 5/5 aldınız",            "req":lambda lc,ls,qp:qp>=1},
    {"id":"hundred","icon":"💯","name":"100 Kelime",      "desc":"100 kelime öğrendiniz",          "req":lambda lc,ls,qp:lc>=100},
    {"id":"a1done", "icon":"🌿","name":"A1 Tamamlandı",   "desc":"A1 seviyesini tamamladınız",     "req":lambda lc,ls,qp:lc>=40},
    {"id":"b1reach","icon":"🌊","name":"B1 Seviyesi",     "desc":"B1 seviyesine ulaştınız",        "req":lambda lc,ls,qp:lc>=120},
    {"id":"master", "icon":"🎓","name":"LexiCode Master", "desc":"Tüm kelimeleri öğrendiniz",       "req":lambda lc,ls,qp:lc>=len(WORDS)},
]

def check_badges():
    lc = get_learned_count(); ls = int(get_s("streak","0"))
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT badge_id FROM badges")
    earned = {r[0] for r in c.fetchall()}
    c.execute("SELECT COUNT(*) FROM settings WHERE key='quiz_perfect' AND CAST(value AS INTEGER)>0")
    qp = c.fetchone()[0]
    new_b = []
    for b in BADGES_DEF:
        if b["id"] not in earned and b["req"](lc,ls,qp):
            c.execute("INSERT OR IGNORE INTO badges VALUES(?,?)",(b["id"],datetime.now().isoformat()))
            new_b.append({"id":b["id"],"icon":b["icon"],"name":b["name"],"desc":b["desc"]})
    conn.commit(); conn.close(); return new_b

LEVELS = ["A1","A2","B1","B2","C1"]
LEVELS_XP = {"A1":0,"A2":200,"B1":500,"B2":1000,"C1":1800}
LEVEL_NAMES = {"A1":"A1 🌱","A2":"A2 🌿","B1":"B1 🌊","B2":"B2 ⭐","C1":"C1 🔥"}

def get_level_info(xp):
    lvl = "A1"
    for l in LEVELS:
        if xp >= LEVELS_XP[l]: lvl = l
    idx = LEVELS.index(lvl)
    nxt = LEVELS[idx+1] if idx+1 < len(LEVELS) else None
    xmin = LEVELS_XP[lvl]; xmax = LEVELS_XP[nxt] if nxt else xmin+500
    pct = min(100, int((xp-xmin)/(xmax-xmin)*100)) if xmax>xmin else 100
    return {"name":LEVEL_NAMES[lvl],"level":lvl,
            "next":LEVEL_NAMES[nxt] if nxt else None,
            "xp_to_next":(xmax-xp) if nxt else 0,"pct":pct}

# ═══════════════════════════════════════════════════════
# ROUTES — DATA
# ═══════════════════════════════════════════════════════

@app.route("/")
def index():
    with open(os.path.join(RESOURCE_DIR, "templates", "index.html"), encoding="utf-8") as f:
        return f.read()


@app.route("/api/health")
def api_health():
    return jsonify({
        "ok": True,
        "app": APP_NAME,
        "version": APP_VERSION,
        "tts_primary": "edge-tts",
        "database": os.path.basename(DB),
    })


@app.route("/api/tts", methods=["POST"])
def api_tts():
    payload = request.get_json(silent=True) or {}
    text = clean_tts_text(payload.get("text", ""))
    if not text:
        return api_error("text_required", "Ses üretmek için metin gerekli.", status=400)

    language = payload.get("lang", "en-US")
    gender = payload.get("gender", "female")
    rate = payload.get("rate", 0.92 if str(language).lower().startswith("tr") else 0.86)

    try:
        audio, voice = generate_tts_audio(text, language=language, gender=gender, rate=rate)
        response = Response(audio, mimetype="audio/mpeg")
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Lexicode-Voice"] = voice
        return response
    except ValueError:
        return api_error("text_required", "Ses üretmek için metin gerekli.", status=400)
    except RuntimeError as exc:
        if str(exc) == "server_tts_unavailable":
            return api_error("server_tts_unavailable", "Neural ses servisi şu anda kullanılamıyor.", status=503)
        logger.warning("TTS runtime error: %s", exc)
        return api_error("tts_generation_failed", "Ses dosyası üretilemedi.", status=502, detail=str(exc))
    except Exception as exc:
        logger.warning("TTS generation failed: %s", exc)
        return api_error("tts_generation_failed", "Ses dosyası üretilemedi.", status=502, detail=str(exc))

@app.route("/api/words")
def api_words():
    mod   = request.args.get("mod","cs")
    level = request.args.get("level","")
    cat   = request.args.get("cat","")
    mode  = request.args.get("mode","normal")

    ws = [w for w in WORDS if w["mod"]==mod] if mod!="all" else list(WORDS)
    if level: ws = [w for w in ws if w["level"]==level]
    if cat:   ws = [w for w in ws if w["cat"]==cat]

    progress = get_progress()
    if mode == "due":
        due = get_due_ids()
        ws2 = [w for w in ws if w["id"] in due]
        ws = ws2 if ws2 else ws
    elif mode == "weak":
        weak = get_weak_ids()
        ws2 = [w for w in ws if w["id"] in weak]
        ws = ws2 if ws2 else ws
    elif mode == "focus":
        ids = get_due_ids() | get_weak_ids()
        ws2 = [w for w in ws if w["id"] in ids]
        ws = ws2 if ws2 else ws

    result = []
    for w in ws:
        p = progress.get(w["id"],{"learned":0,"skipped":0,"correct":0,"wrong":0,"next_review":None,"interval":1})
        result.append({**w,"progress":p})
    return jsonify(result)

@app.route("/api/stats")
def api_stats():
    xp      = int(get_s("xp","0"))
    streak  = int(get_s("streak","0"))
    learned = get_learned_count()
    today   = datetime.now().date().isoformat()
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("SELECT cs_studied,daily_studied FROM daily_log WHERE date=?", (today,))
    row = c.fetchone()
    today_cs    = row[0] if row else 0
    today_daily = row[1] if row else 0
    c.execute("SELECT badge_id FROM badges")
    earned = [r[0] for r in c.fetchall()]
    conn.close()
    dg = int(get_s("daily_goal","10"))
    am = get_s("active_mod","cs")
    al = get_s("active_level","")
    fm = get_s("focus_mode","0")=="1"
    return jsonify({
        "total":len(WORDS),"learned":learned,
        "cs_learned":get_learned_count("cs"),
        "daily_learned":get_learned_count("daily"),
        "xp":xp,"streak":streak,
        "level_info":get_level_info(xp),
        "due_count":len(get_due_ids()),
        "weak_count":len(get_weak_ids()),
        "today_cs":today_cs,"today_daily":today_daily,
        "daily_goal":dg,"earned_badges":earned,
        "active_mod":am,"active_level":al,"focus_mode":fm,
        "pct":round(learned/len(WORDS)*100,1),
    })

@app.route("/api/mark_learned", methods=["POST"])
def mark_learned():
    d   = request.json
    wid = d.get("word_id"); word=d.get("word",""); mod=d.get("mod","cs"); lv=d.get("level","A1")
    now = datetime.now().isoformat()
    nr  = (datetime.now().date()+timedelta(days=1)).isoformat()
    today = datetime.now().date().isoformat()
    conn = sqlite3.connect(DB); c = conn.cursor()
    c.execute("""INSERT INTO progress(word_id,word,mod,level,learned,last_seen,first_learned,next_review,review_interval)
                 VALUES(?,?,?,?,1,?,?,?,1)
                 ON CONFLICT(word_id) DO UPDATE SET
                 learned=1,last_seen=?,first_learned=COALESCE(first_learned,?),next_review=COALESCE(next_review,?)""",
              (wid,word,mod,lv,now,nr,1,now,now,nr))
    if mod=="cs":
        c.execute("INSERT INTO daily_log(date,cs_studied) VALUES(?,1) ON CONFLICT(date) DO UPDATE SET cs_studied=cs_studied+1",(today,))
    else:
        c.execute("INSERT INTO daily_log(date,daily_studied) VALUES(?,1) ON CONFLICT(date) DO UPDATE SET daily_studied=daily_studied+1",(today,))
    conn.commit(); conn.close()
    streak = int(get_s("streak","0"))+1; set_s("streak",streak)
    xp = add_xp(10); lc = get_learned_count(); nb = check_badges()
    return jsonify({"success":True,"learned":lc,"streak":streak,"xp":xp,
                    "level_info":get_level_info(xp),"new_badges":nb,
                    "trigger_quiz":lc>0 and lc%50==0})

@app.route("/api/mark_skipped", methods=["POST"])
def mark_skipped():
    d=request.json; wid=d.get("word_id"); word=d.get("word",""); mod=d.get("mod","cs"); lv=d.get("level","A1")
    now=datetime.now().isoformat()
    conn=sqlite3.connect(DB); c=conn.cursor()
    c.execute("INSERT INTO progress(word_id,word,mod,level,skipped,last_seen) VALUES(?,?,?,?,1,?) ON CONFLICT(word_id) DO UPDATE SET skipped=skipped+1,last_seen=?",
              (wid,word,mod,lv,now,now))
    conn.commit(); conn.close()
    return jsonify({"success":True})

@app.route("/api/quiz")
def api_quiz():
    mod   = request.args.get("mod","cs")
    level = request.args.get("level","")
    mode  = request.args.get("mode","learned")
    if mode=="weak":
        weak = get_weak_ids()
        pool = [w for w in WORDS if w["id"] in weak and w["mod"]==mod]
    elif mode=="level" and level:
        pool = [w for w in WORDS if w["mod"]==mod and w["level"]==level]
    else:
        conn=sqlite3.connect(DB); c=conn.cursor()
        c.execute("SELECT word_id FROM progress WHERE learned=1 AND mod=?",(mod,))
        ids={r[0] for r in c.fetchall()}; conn.close()
        pool=[w for w in WORDS if w["id"] in ids]
    base = [w for w in WORDS if w["mod"]==mod]
    if len(pool)<5: pool = [w for w in WORDS if w["mod"]==mod and (level=='' or w["level"]==level)]
    chosen = random.sample(pool, min(5,len(pool)))
    questions=[]
    for w in chosen:
        oth = random.sample([x for x in base if x["id"]!=w["id"]], min(3,len(base)-1))
        opts=[w["word"]]+[x["word"] for x in oth]; random.shuffle(opts)
        questions.append({"id":w["id"],"word":w["word"],"tr":w["tr"],"icon":w["icon"],
                          "cat":w["cat"],"level":w["level"],"mod":w["mod"],
                          "sentence":w["sent"],"structure":w["str"],
                          "options":opts,"answer":w["word"],
                          "why":w.get("why",""),"da":w.get("da",""),"db":w.get("db","")})
    return jsonify(questions)

@app.route("/api/quiz/answer", methods=["POST"])
def quiz_answer():
    d=request.json; wid=int(d.get("word_id",0)); correct=d.get("correct",False)
    word=d.get("word",""); mod=d.get("mod","cs")
    now=datetime.now().isoformat()
    conn=sqlite3.connect(DB); c=conn.cursor()
    if correct:
        c.execute("INSERT INTO progress(word_id,word,mod,correct_count,last_seen) VALUES(?,?,?,1,?) ON CONFLICT(word_id) DO UPDATE SET correct_count=correct_count+1,last_seen=?",
                  (wid,word,mod,now,now))
        xp=add_xp(15)
    else:
        c.execute("INSERT INTO progress(word_id,word,mod,wrong_count,last_seen) VALUES(?,?,?,1,?) ON CONFLICT(word_id) DO UPDATE SET wrong_count=wrong_count+1,last_seen=?",
                  (wid,word,mod,now,now))
        xp=int(get_s("xp","0"))
    conn.commit(); conn.close()
    update_spaced(wid,correct); nb=check_badges()
    return jsonify({"success":True,"xp":xp,"level_info":get_level_info(xp),"new_badges":nb})

@app.route("/api/mindmap")
def api_mindmap():
    mod=request.args.get("mod","cs"); level=request.args.get("level","")
    conn=sqlite3.connect(DB); c=conn.cursor()
    c.execute("SELECT word_id FROM progress WHERE learned=1 AND mod=?",(mod,))
    learned_ids={r[0] for r in c.fetchall()}; conn.close()
    due_ids=get_due_ids()
    ws=[w for w in WORDS if w["mod"]==mod and (not level or w["level"]==level)]
    pool=[w for w in ws if w["id"] in learned_ids]
    if len(pool)<6: pool=random.sample(ws,min(30,len(ws)))
    by_cat={}
    for w in pool:
        by_cat.setdefault(w["cat"],[]).append({
            "id":w["id"],"word":w["word"],"tr":w["tr"],
            "icon":w["icon"],"level":w["level"],
            "rel":w.get("rel",[]),"why":w.get("why",""),
            "due":w["id"] in due_ids,"learned":w["id"] in learned_ids})
    return jsonify(by_cat)

@app.route("/api/analytics")
def api_analytics():
    mod=request.args.get("mod","")
    conn=sqlite3.connect(DB); c=conn.cursor()
    if mod:
        c.execute("SELECT word_id,word,wrong_count,correct_count FROM progress WHERE wrong_count>0 AND mod=? ORDER BY wrong_count DESC LIMIT 10",(mod,))
    else:
        c.execute("SELECT word_id,word,wrong_count,correct_count FROM progress WHERE wrong_count>0 ORDER BY wrong_count DESC LIMIT 10")
    hardest=[{"id":r[0],"word":r[1],"wrong":r[2],"correct":r[3]} for r in c.fetchall()]
    c.execute("SELECT date,cs_studied,daily_studied FROM daily_log ORDER BY date DESC LIMIT 7")
    daily=[{"date":r[0],"cs":r[1],"daily":r[2]} for r in c.fetchall()]
    c.execute("SELECT level,COUNT(*) FROM progress WHERE learned=1 GROUP BY level")
    by_level={r[0]:r[1] for r in c.fetchall()}
    conn.close()
    return jsonify({"hardest":hardest,"daily":daily,"by_level":by_level})

@app.route("/api/badges")
def api_badges():
    lc=get_learned_count(); ls=int(get_s("streak","0"))
    conn=sqlite3.connect(DB); c=conn.cursor()
    c.execute("SELECT badge_id,earned_at FROM badges")
    earned={r[0]:r[1] for r in c.fetchall()}; conn.close()
    return jsonify([{"id":b["id"],"icon":b["icon"],"name":b["name"],"desc":b["desc"],
                     "earned":b["id"] in earned,"earned_at":earned.get(b["id"],"")}
                    for b in BADGES_DEF])

@app.route("/api/settings", methods=["GET","POST"])
def api_settings():
    if request.method=="POST":
        for k in ["daily_goal","streak_goal","active_mod","active_level","focus_mode"]:
            if k in request.json: set_s(k,request.json[k])
        return jsonify({"success":True})
    return jsonify({"daily_goal":int(get_s("daily_goal","10")),
                    "streak_goal":int(get_s("streak_goal","7")),
                    "active_mod":get_s("active_mod","cs"),
                    "active_level":get_s("active_level",""),
                    "focus_mode":get_s("focus_mode","0")=="1"})

@app.route("/api/reset", methods=["POST"])
def api_reset():
    conn=sqlite3.connect(DB); c=conn.cursor()
    c.execute("DELETE FROM progress"); c.execute("DELETE FROM badges")
    c.execute("DELETE FROM daily_log")
    c.execute("UPDATE settings SET value='0' WHERE key IN ('xp','streak')")
    conn.commit(); conn.close()
    return jsonify({"success":True})

# ── AI ROUTES ──────────────────────────────────────────
def _strip_html(text):
    import re
    from html import unescape
    return re.sub(r"<[^>]+>", "", unescape(text or "")).strip()


def _find_word_entry(word, mod=None):
    needle = (word or "").strip().lower()
    if not needle:
        return None
    exact = [w for w in WORDS if w["word"].lower() == needle and (mod is None or w["mod"] == mod)]
    if exact:
        return exact[0]
    partial = [w for w in WORDS if needle in w["word"].lower() and (mod is None or w["mod"] == mod)]
    return partial[0] if partial else None


def _fallback_correct(sentence):
    import re
    original = " ".join((sentence or "").strip().split())
    corrected = original
    rules = [
        (r"\bI am agree\b", "I agree"),
        (r"\bI go yesterday school\b", "I went to school yesterday"),
        (r"\bI go to school yesterday\b", "I went to school yesterday"),
        (r"\bI go yesterday\b", "I went yesterday"),
        (r"\bgo school\b", "go to school"),
        (r"\bI have ([0-9]+) years old\b", r"I am \1 years old"),
        (r"\bHe go\b", "He goes"),
        (r"\bShe go\b", "She goes"),
        (r"\bIt go\b", "It goes"),
        (r"\bI am study\b", "I am studying"),
    ]
    for pattern, repl in rules:
        corrected = re.sub(pattern, repl, corrected, flags=re.IGNORECASE)
    corrected = re.sub(r"\bi\b", "I", corrected)
    corrected = corrected[:1].upper() + corrected[1:] if corrected else corrected
    if corrected and corrected[-1] not in ".!?":
        corrected += "."
    is_same = corrected.rstrip(".") == original.rstrip(".")
    return {
        "correct": is_same,
        "original": original,
        "corrected": corrected,
        "errors": [] if is_same else ["Temel zaman / cümle yapısı düzenlendi."],
        "explanation": "İnternet AI servisi kullanılamadığı için güvenli yerel düzeltme modu kullanıldı.",
        "tip": "Kısa kalıp kullan: özne + fiil + nesne.",
        "structure": "S+V+O"
    }


def _fallback_generate(word, mod):
    entry = _find_word_entry(word, mod) or _find_word_entry(word)
    clean_word = (entry or {}).get("word", word.strip())
    tr = (entry or {}).get("tr", "anlam")
    sentence1 = _strip_html((entry or {}).get("sent", "")) or f"I use {clean_word} when I study English."
    sentence2 = ((entry or {}).get("tpl", "") or "").replace("___", clean_word).strip()
    if not sentence2 or "___" in sentence2:
        sentence2 = f"The word {clean_word} is useful in {('computer English' if mod == 'cs' else 'daily English')}."
    if sentence2[-1] not in ".!?":
        sentence2 += "."
    structure1 = (entry or {}).get("str", "S+V+O")
    return {
        "sentences": [sentence1, sentence2],
        "turkish": [
            f"\"{clean_word}\" kelimesi için örnek kullanım. Türkçesi: {tr}.",
            f"{clean_word} kelimesi {('bilgisayar' if mod == 'cs' else 'günlük')} İngilizcesinde sık kullanılır."
        ],
        "structures": [structure1, "S+V+O"],
        "motivation": "Harika gidiyorsun — şimdi bu iki cümleyi yüksek sesle tekrar et. 💙"
    }


def _fallback_dialog(word, msg, mod):
    entry = _find_word_entry(word, mod) or _find_word_entry(word)
    tr = (entry or {}).get("tr", "bir kelime")
    example = _strip_html((entry or {}).get("sent", "")) or f"I use {word} every day."
    reply = f"Nice try! You can use {word} like this: {example}"
    translation = f"Güzel deneme! {word} kelimesini şöyle kullanabilirsin: {tr}."
    return {"reply": reply, "translation": translation, "used_word": word.lower() in reply.lower()}


def call_claude(system, user, max_tokens=600):
    import urllib.request, urllib.error
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY ayarlı değil")
    payload = json.dumps({
        "model": CLAUDE_MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}]
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": api_key,
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = result["content"][0]["text"]
            cleaned = text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Claude API {e.code}: {detail[:180] or e.reason}") from e

@app.route("/api/ai/correct", methods=["POST"])
def ai_correct():
    s = request.json.get("sentence", "").strip()
    if not s:
        return api_error("validation_error", "Cümle boş.", status=400)
    try:
        d = call_claude(
            'You are a warm encouraging English grammar tutor for a Turkish dyslexic CS student. '
            'Reply ONLY raw JSON: {"correct":true/false,"original":"...","corrected":"...",'
            '"errors":["Turkish error"],"explanation":"encouraging Turkish","tip":"dyslexia tip Turkish","structure":"S+V+O"}',
            f"Check: {s}")
        return jsonify(d)
    except Exception as e:
        logger.warning("AI correct fallback used: %s", e)
        return jsonify(_fallback_correct(s))


@app.route("/api/ai/generate", methods=["POST"])
def ai_generate():
    word = request.json.get("word", "")
    mod = request.json.get("mod", "cs")
    ctx = "computer science" if mod == "cs" else "everyday English"
    if not word:
        return api_error("validation_error", "Kelime gerekli.", status=400)
    try:
        d = call_claude(
            f'You are an encouraging English tutor for Turkish dyslexic students. '
            f'Generate 2 simple short sentences for the word in {ctx} context. '
            'Reply ONLY raw JSON: {"sentences":["s1","s2"],"turkish":["tr1","tr2"],'
            '"structures":["S+V+O","..."],"motivation":"Turkish motivational note"}',
            f"Word: {word}")
        return jsonify(d)
    except Exception as e:
        logger.warning("AI generate fallback used: %s", e)
        return jsonify(_fallback_generate(word, mod))


@app.route("/api/ai/dialog", methods=["POST"])
def ai_dialog():
    word = request.json.get("word", "")
    msg = request.json.get("message", "")
    mod = request.json.get("mod", "cs")
    ctx = "IT workplace" if mod == "cs" else "everyday situation"
    if not word or not msg:
        return api_error("validation_error", "Eksik parametre.", status=400)
    try:
        d = call_claude(
            f'You are in a short {ctx} conversation. Key word: "{word}". '
            'Reply in 1-2 short sentences. Try to use the word. Be encouraging. '
            'Reply ONLY raw JSON: {"reply":"...","translation":"Turkish","used_word":true/false}',
            msg, max_tokens=250)
        return jsonify(d)
    except Exception as e:
        logger.warning("AI dialog fallback used: %s", e)
        return jsonify(_fallback_dialog(word, msg, mod))

@app.errorhandler(404)
def handle_not_found(error):
    if request.path.startswith("/api/"):
        return api_error("not_found", "İstenen API rotası bulunamadı.", status=404)
    return "Not Found", 404


@app.route("/api/history")
def api_history():
    mod = request.args.get("mod", "")
    limit = min(int(request.args.get("limit", "30")), 100)
    conn = sqlite3.connect(DB); c = conn.cursor()
    if mod:
        c.execute(
            "SELECT word_id, word, mod, level, first_learned, correct_count, wrong_count "
            "FROM progress WHERE learned=1 AND mod=? ORDER BY first_learned DESC LIMIT ?",
            (mod, limit))
    else:
        c.execute(
            "SELECT word_id, word, mod, level, first_learned, correct_count, wrong_count "
            "FROM progress WHERE learned=1 ORDER BY first_learned DESC LIMIT ?",
            (limit,))
    rows = c.fetchall(); conn.close()
    result = []
    for r in rows:
        entry = _find_word_entry(r[1], r[2])
        result.append({
            "word_id": r[0], "word": r[1], "mod": r[2], "level": r[3],
            "learned_at": r[4] or "", "correct": r[5], "wrong": r[6],
            "tr": entry["tr"] if entry else "", "icon": entry["icon"] if entry else "📖",
        })
    return jsonify(result)


@app.errorhandler(500)
def handle_server_error(error):
    logger.exception("Unhandled server error: %s", error)
    if request.path.startswith("/api/"):
        return api_error("internal_server_error", "Beklenmeyen bir sunucu hatası oluştu.", status=500)
    return "<h3>Beklenmeyen bir hata oluştu.</h3>", 500


# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    init_db()
    from words import get_stats
    s = get_stats()
    print("=" * 55)
    print("  LexiCode — Disleksi Dostu İngilizce Öğrenme")
    print("=" * 55)
    print(f"  📚 Toplam: {s['total']} | CS: {s['cs']} | Günlük: {s['daily']}")
    print(f"  📊 Seviyeler: {s['by_level']}")
    print(f"  🌐 http://{DEFAULT_HOST}:{DEFAULT_PORT}")
    print("=" * 55)
    logger.info("Starting %s v%s on %s:%s", APP_NAME, APP_VERSION, DEFAULT_HOST, DEFAULT_PORT)
    app.run(debug=DEBUG, host=DEFAULT_HOST, port=DEFAULT_PORT)
