import json, os
CAT_MAP = {
 "פיק אנד רול":"Pick & Roll","High P&R":"Pick & Roll","Side P&R":"Pick & Roll","הגנה על פיק אנד רול":"Pick & Roll Defense",
 "סקרינים בלי כדור":"Off-Ball Screens & Cuts","הגנה אזורית":"Zone Defense","התקפה נגד אזורית":"Zone Offense","לחץ אזורי (פרס)":"Press",
 "הורנס":"Horns","קומבינציות":"Zoom & DHO","Pistol / 21":"Pistol (21)",
 "קליעה":"Shooting","הגנה":"Defensive Drills","אימון אישי":"Individual Workouts","מעבר":"Transition","התקפה":"Offensive Drills","כדרור":"Ball Handling",
 "מסירות":"Passing","פוטוורק":"Footwork","ריבאונד":"Rebounding","משחק":"Small-Sided Games","טכניקה":"Fundamentals","כושר":"Conditioning",
 "חימום":"Warm-Up","טקטיקה":"Offensive Drills","סיום":"Finishing","מול אישית":"Offensive Drills","מול אזור":"Zone Offense","אאוט מהצד":"SLOB","Inbounds (SLOB)":"SLOB",
 "אאוט מקו הבסיס":"BLOB","Inbounds (BLOB)":"BLOB","סוף משחק":"End of Game","Offense":"Offensive Drills","Defense":"Defensive Drills"}
ID_CAT = {"pb-drag":"Drag","pb-double-drag":"Drag","pb-miami":"Zoom & DHO","pb-pistol":"Pistol (21)","pb-blind-pig":"Off-Ball Screens & Cuts",
 "pb-spain-hoopdirt":"Pick & Roll"}
REMOVE = {"pb-floppy":"flp-reads","pb-ram":"ram-high-filled","pb-stagger":"stg-reads","pb-pindown":"pd-reads","pb-spread-pnr":"hp-4out-filled","pb-ghost":"ghost-flare"}
CAT_GROUPS = [
 ["Offense",["Pick & Roll","Drag","Ram","Ghost","Horns","Pistol (21)","Delay","Zoom & DHO","Pin-Down","Stagger","Floppy","Off-Ball Screens & Cuts","Zone Offense"]],
 ["Defense",["Pick & Roll Defense","Zone Defense","Press"]],
 ["Special Situations",["BLOB","SLOB","End of Game"]],
 ["Drills",["Warm-Up","Fundamentals","Ball Handling","Passing","Shooting","Finishing","Footwork","Rebounding","Offensive Drills","Defensive Drills","Transition","Small-Sided Games","Individual Workouts","Conditioning"]]]
CATEGORIES = [c for g in CAT_GROUPS for c in g[1]]
def newcat(i, c): return ID_CAT.get(i) or CAT_MAP.get(c) or c
if __name__ == "__main__":
    R="/home/claude"
    L=json.load(open(R+"/knowball/library.json"))
    byid={x["id"]:x for x in L}
    # merge tags of removed into kept
    for a,b in REMOVE.items():
        if a in byid and b in byid:
            t=byid[b]["data"].setdefault("tags",[])
            for g in byid[a]["data"].get("tags",[]):
                if g not in t: t.append(g)
    L=[x for x in L if x["id"] not in REMOVE]
    for x in L: x["data"]["category"]=newcat(x["id"],x["data"].get("category",""))
    new=json.load(open(R+"/lib/new_pnr_def.json"))+json.load(open(R+"/lib/new_batch2.json"))
    have={x["id"] for x in L}
    L+= [n for n in new if n["id"] not in have]
    L.sort(key=lambda x:x["id"])
    bad=sorted({x["data"]["category"] for x in L}-set(CATEGORIES)); assert not bad, bad
    json.dump(L,open(R+"/knowball/library.json","w"),ensure_ascii=False,separators=(",",":"))
    import collections; print(len(L), collections.Counter(x["data"]["category"] for x in L).most_common())
    # merged tags for artifact patch
    tagpatch={b:byid[b]["data"]["tags"] for a,b in REMOVE.items()}
    js=("  var CAT_GROUPS = "+json.dumps(CAT_GROUPS,ensure_ascii=False)+";\n  var CATEGORIES = [].concat.apply([], CAT_GROUPS.map(function (g) { return g[1]; }));\n"
        "  var CAT_MAP = "+json.dumps(CAT_MAP,ensure_ascii=False)+";\n"
        "  var LIB_MIG = { v: 2, idCat: "+json.dumps(ID_CAT,ensure_ascii=False)+", remove: "+json.dumps(sorted(REMOVE),ensure_ascii=False)+", tags: "+json.dumps(tagpatch,ensure_ascii=False)+" };\n")
    open(R+"/lib/consts.js","w").write(js)
    open(R+"/lib/pack_pnr.js","w").write(json.dumps({"id":"pnr-def-1","bank":False,"items":json.load(open(R+"/lib/new_pnr_def.json"))},ensure_ascii=False))
    open(R+"/lib/pack_b2.js","w").write(json.dumps({"id":"inb-next-1","bank":False,"items":json.load(open(R+"/lib/new_batch2.json"))},ensure_ascii=False))
