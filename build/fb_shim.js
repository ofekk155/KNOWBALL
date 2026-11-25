/* KnowBall on Firebase: auth gate + adapter that gives the app the same db/user API it uses as an artifact. */
(function () {
  "use strict";
  window.KB_FIREBASE = true;
  var firebaseConfig = {
    apiKey: "AIzaSyBk9DQK4yyG8gBR7V2AX-puMvTBjVODa2I",
    authDomain: "knowball-32101.firebaseapp.com",
    projectId: "knowball-32101",
    storageBucket: "knowball-32101.firebasestorage.app",
    messagingSenderId: "1070685428177",
    appId: "1:1070685428177:web:a1f35f9b6ba3556b5a68f0"
  };
  firebase.initializeApp(firebaseConfig);
  var auth = firebase.auth();
  auth.languageCode = "he";
  var fs = firebase.firestore();
  try { fs.settings({ ignoreUndefinedProperties: true }); } catch (e) {}

  /* Firestore can't store arrays inside arrays (diagram paths are [[x,y], ...]). Wrap them on write, unwrap on read. */
  function enc(v) {
    if (Array.isArray(v)) return v.map(function (x) { return Array.isArray(x) ? { __arr: enc(x) } : enc(x); });
    if (v && typeof v === "object" && !(v instanceof Date)) { var o = {}; Object.keys(v).forEach(function (k) { if (v[k] !== undefined) o[k] = enc(v[k]); }); return o; }
    return v;
  }
  function dec(v) {
    if (Array.isArray(v)) return v.map(dec);
    if (v && typeof v === "object") {
      var ks = Object.keys(v);
      if (ks.length === 1 && ks[0] === "__arr" && Array.isArray(v.__arr)) return dec(v.__arr);
      var o = {}; ks.forEach(function (k) { o[k] = dec(v[k]); }); return o;
    }
    return v;
  }
  function wrapSnap(s) {
    var data = s.exists ? dec(s.data()) : undefined;
    return { id: s.id, exists: s.exists, data: function () { return data; }, metadata: s.metadata, ref: wrapDoc(s.ref) };
  }
  function wrapQuery(qs) {
    var docs = qs.docs.map(wrapSnap);
    return { docs: docs, size: docs.length, empty: !docs.length, metadata: qs.metadata, forEach: function (f) { docs.forEach(f); } };
  }
  function wrapDoc(ref) {
    return {
      id: ref.id, path: ref.path,
      onSnapshot: function (cb, err) { return ref.onSnapshot(function (s) { cb(wrapSnap(s)); }, err); },
      get: function () { return ref.get().then(wrapSnap); },
      set: function (d, o) { return ref.set(enc(d), o || {}); },
      update: function (d) { return ref.update(enc(d)); },
      delete: function () { return ref.delete(); },
      collection: function (c) { return wrapCol(ref.collection(c)); }
    };
  }
  function wrapCol(col) {
    return {
      path: col.path,
      doc: function (id) { return wrapDoc(id ? col.doc(id) : col.doc()); },
      add: function (d) { return col.add(enc(d)).then(wrapDoc); },
      onSnapshot: function (cb, err) { return col.onSnapshot(function (qs) { cb(wrapQuery(qs)); }, err); },
      get: function () { return col.get().then(wrapQuery); }
    };
  }

  /* The drill library is a static file shipped with the site (read-only for everyone). */
  var libPromise = fetch("library.json", { cache: "no-cache" }).then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; });
  function denied() { return Promise.reject({ code: "permission-denied" }); }
  var staticLib = {
    path: "library",
    onSnapshot: function (cb, err) {
      var dead = false;
      libPromise.then(function (items) {
        if (dead) return;
        var docs = items.map(function (it) { var d = it.data; return { id: it.id, exists: true, data: function () { return d; }, metadata: { fromCache: false } }; });
        cb({ docs: docs, size: docs.length, empty: !docs.length, metadata: { fromCache: false }, forEach: function (f) { docs.forEach(f); } });
      }, err);
      return function () { dead = true; };
    },
    doc: function (id) { return { id: id, set: denied, update: denied, delete: denied, get: denied }; },
    add: denied
  };

  function makeDb(uid) {
    return {
      doc: function (path) {
        if (path === "data/users/" + uid + "/profile") return wrapDoc(fs.doc("users/" + uid));
        return wrapDoc(fs.doc(path));
      },
      collection: function (path) { return path === "library" ? staticLib : wrapCol(fs.collection(path)); }
    };
  }
  var downloads = {
    save: function (o) {
      try {
        var url = URL.createObjectURL(o.data), a = document.createElement("a");
        a.href = url; a.download = o.filename || "download"; document.body.appendChild(a); a.click();
        setTimeout(function () { URL.revokeObjectURL(url); a.remove(); }, 1500);
        return Promise.resolve();
      } catch (e) { return Promise.reject(e); }
    }
  };

  /* ---------- auth UI ---------- */
  var $ = function (id) { return document.getElementById(id); };
  var mode = "login"; // login | signup | reset
  function msg(t, ok) { var m = $("kbMsg"); m.textContent = t || ""; m.className = "msg " + (ok ? "ok" : "err"); }
  function setMode(m) {
    mode = m; msg("");
    $("kbTitle").textContent = m === "signup" ? "הרשמה" : m === "reset" ? "איפוס סיסמה" : "כניסה";
    $("kbSubmit").textContent = m === "signup" ? "יצירת חשבון" : m === "reset" ? "שליחת קישור לאיפוס" : "כניסה";
    $("kbPassWrap").hidden = m === "reset";
    $("kbPass").autocomplete = m === "signup" ? "new-password" : "current-password";
    $("kbToggle").textContent = m === "login" ? "אין לך חשבון? הרשמה" : "יש לך חשבון? כניסה";
    $("kbForgot").hidden = m === "reset";
  }
  function errText(e) {
    var c = (e && e.code) || "";
    if (c === "auth/invalid-credential" || c === "auth/wrong-password" || c === "auth/user-not-found" || c === "auth/invalid-login-credentials") return "האימייל או הסיסמה לא נכונים.";
    if (c === "auth/email-already-in-use") return "כבר יש חשבון עם האימייל הזה. נסה להיכנס.";
    if (c === "auth/weak-password") return "הסיסמה קצרה מדי (לפחות 6 תווים).";
    if (c === "auth/invalid-email" || c === "auth/missing-email") return "כתובת האימייל לא תקינה.";
    if (c === "auth/too-many-requests") return "יותר מדי ניסיונות. נסה שוב בעוד כמה דקות.";
    if (c === "auth/network-request-failed") return "אין חיבור לאינטרנט.";
    return "משהו השתבש. נסה שוב.";
  }
  function wireAuth() {
    $("kbToggle").addEventListener("click", function () { setMode(mode === "login" ? "signup" : "login"); });
    $("kbForgot").addEventListener("click", function () { setMode("reset"); });
    $("kbForm").addEventListener("submit", function (e) {
      e.preventDefault();
      var em = $("kbEmail").value.trim(), pw = $("kbPass").value, btn = $("kbSubmit");
      if (!em) { msg("צריך אימייל."); return; }
      if (mode !== "reset" && pw.length < 6) { msg("הסיסמה צריכה להיות לפחות 6 תווים."); return; }
      btn.disabled = true; msg("");
      var p = mode === "signup" ? auth.createUserWithEmailAndPassword(em, pw)
        : mode === "reset" ? auth.sendPasswordResetEmail(em).then(function () { msg("אם יש חשבון עם האימייל הזה, נשלח אליו קישור לאיפוס. בדוק גם בספאם.", true); })
        : auth.signInWithEmailAndPassword(em, pw);
      p.catch(function (er) { msg(errText(er)); }).then(function () { btn.disabled = false; });
    });
    setMode("login");
  }
  function userBar(user) {
    var hdr = document.querySelector("header");
    if (!hdr || $("kbUserBar")) return;
    var bar = document.createElement("div");
    bar.className = "kb-userbar no-export"; bar.id = "kbUserBar";
    var span = document.createElement("span"); span.dir = "ltr"; span.textContent = user.email || "";
    var out = document.createElement("button"); out.type = "button"; out.className = "btn small ghost"; out.textContent = "התנתקות";
    out.addEventListener("click", function () { auth.signOut().then(function () { location.reload(); }); });
    bar.appendChild(span); bar.appendChild(out); hdr.appendChild(bar);
  }

  var started = false;
  document.addEventListener("DOMContentLoaded", function () {
    wireAuth();
    auth.onAuthStateChanged(function (user) {
      if (!user) { if (started) { location.reload(); return; } $("kbAuth").hidden = false; return; }
      $("kbAuth").hidden = true;
      if (started) return;
      started = true;
      userBar(user);
      var db = makeDb(user.uid);
      var userNs = { id: function () { return Promise.resolve(user.uid); }, canEdit: function () { return false; } };
      window.claude = {
        use: function (n) {
          if (n === "db") return Promise.resolve(db);
          if (n === "user") return Promise.resolve(userNs);
          if (n === "downloads") return Promise.resolve(downloads);
          return Promise.resolve(null); /* sample (AI) and assets (video) come in the next stage */
        }
      };
    });
  });
})();
