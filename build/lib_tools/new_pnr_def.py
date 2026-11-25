import json
def P(i,t,x,y,ball=False):
    d={"id":i,"team":t,"x":x,"y":y}
    if ball: d["ball"]=True
    return d
def A(t,f,path=None,to=None):
    d={"type":t,"from":f}
    if path: d["path"]=path
    if to: d["to"]=to
    return d
base=dict(kind="play",category="Pick & Roll Defense",minutes=None)
items=[]
# 1 Over + rearview pursuit
s1=[P("1","O",25,30,True),P("5","O",27.5,28.5),P("x1","X",24.5,28),P("x5","X",27,23),P("2","O",3,3),P("3","O",47,3)]
s2=[P("1","O",34,22,True),P("5","O",27.5,28.5),P("x1","X",33,24),P("x5","X",29,18),P("2","O",3,3),P("3","O",47,3)]
items.append({"id":"cov-over","data":dict(base,name="Over + Rearview Pursuit (with Drop)",level="נוער",players="2 על 2 + קלעים",leagues=["NBA","EuroLeague","NCAA"],
 description="השומר על הכדור עובר מעל החסימה, צמוד לכדרר, ודוחף אותו פנימה מקו השלוש. אם הוא נתפס בחסימה, הוא רודף מאחור לכתף הפנימית (rearview pursuit) עד שהוא חוזר. הביג נסוג (דרופ) לעומק שנקבע מראש ושומר את הכדרר ואת הרולר לפניו.",
 points=["x1 צמוד לכדור כבר לפני החסימה, נמוך וצר","אחרי שנחסם: לרדוף מאחור לכתף הפנימית ולהפריע לזריקה","x5 מוכן מוקדם בעומק שלו ולא עושה צעד מאוחר קדימה לכדור","קריאה מוקדמת וחזקה עם כיוון: 'דרופ ימין!'"],
 source="https://medium.com/the-basketball-dictionary/drop-part-i-42add19791f1",sourceName="The Basketball Dictionary",
 tags=["over","chase","rearview pursuit","drop","אובר","מעל החסימה","רדיפה"],
 diagram={"court":"half","steps":[
  {"caption":"x1 צמוד ל-1 ועובר מעל החסימה; x5 נסוג לעומק שלו ושומר את 1 ואת 5 לפניו.","players":s1,
   "actions":[A("dribble","1",[[31,27],[34,22]]),A("cut","x1",[[27,30],[31,28],[33,24]]),A("cut","x5",[[29,18]])]},
  {"caption":"x1 נתפס ורודף מאחור לכתף הפנימית של 1; 5 מתגלגל ו-x5 נשאר בינו לבין הסל.","players":s2,
   "actions":[A("cut","5",[[28,17],[26,9]]),A("cut","x1",[[33,20]]),A("cut","x5",[[27,13]])]}]})})
# 2 Peel switch
s1=[P("1","O",29,27,True),P("x1","X",28,29),P("2","O",42,22),P("x2","X",35,19),P("5","O",18,7),P("x5","X",21,8),P("3","O",3,3)]
s2=[P("1","O",32,15,True),P("x1","X",30,24),P("2","O",42,22),P("x2","X",32,16),P("5","O",18,7),P("x5","X",21,8),P("3","O",3,3)]
items.append({"id":"cov-peel-switch","data":dict(base,name="Peel Switch (Help Takes the Driver)",level="בוגרים",players="5 על 5",leagues=["NBA","EuroLeague"],
 description="הכדרר עקף את השומר שלו. השומר שעוזר במרחק מסירה מחליף ועוצר את החדירה, והשומר שנעקף 'מתקלף' מהכדרר ויוצא לשחקן שנשאר פתוח. ב-FIBA (בילבאו) קוראים לגרסה דומה גם 'Next'.",
 points=["מי שנעקף לא רודף אחרי הכדור – הוא לוקח את הפנוי","שתי קריאות: העוזר מודיע שהוא על הכדור, ואז 'פיל!'","מקדים את הרוטציה ולא נותן לוב לסל, אבל יכולה להישאר שלשה אחרי קיק-אאוט"],
 source="https://medium.com/thebasketballactiondictionary/peel-switch-ac84e9e93633",sourceName="The Basketball Action Dictionary",
 tags=["peel switch","go switch","fly switch","next","פיל סוויץ'","החלפה"],
 diagram={"court":"half","steps":[
  {"caption":"1 עוקף את x1; x2, שעוזר במרחק מסירה, מחליף ועוצר את החדירה.","players":s1,
   "actions":[A("dribble","1",[[32,21],[32,15]]),A("cut","x2",[[32,16]])]},
  {"caption":"x2 קורא 'פיל!'; x1 עוזב את 1 ויוצא בקלוזאאוט ל-2 שנשאר פתוח.","players":s2,
   "actions":[A("cut","x1",[[35,23],[39,22]])]}]})})
# 3 Pre-switch
s1=[P("1","O",25,30,True),P("x1","X",25,28),P("5","O",19,10),P("x5","X",20,12),P("2","O",8,22),P("x2","X",11,20),P("3","O",47,3)]
s2=[P("1","O",25,30,True),P("x1","X",25,28),P("5","O",27.5,28.5),P("x5","X",10,21),P("2","O",8,22),P("x2","X",26,25),P("3","O",47,3)]
items.append({"id":"cov-pre-switch","data":dict(base,name="Pre-Switch (Small Defends the Screen Action)",level="בוגרים",players="3 על 3 + קלעים",leagues=["NBA","EuroLeague"],
 description="לפני שהחסימה מגיעה, שני שומרים מחליפים ביניהם כדי ששומר קטן ומהיר (x2) יהיה על החוסם במקום הביג האיטי (x5). כשהסוויץ' על הפיק אנד רול מגיע, הוא בין שני שחקנים קטנים ואין מיסמאצ'.",
 points=["ההחלפה המוקדמת קורית כשהחוסם רק מתחיל לעלות","הביג עובר לשחקן בפינה או בכנף ושומר עליו רחוק מהכדור","בפיק אנד רול עצמו מחליפים כרגיל, צמוד, בלי רווח"],
 source="https://thehoopsgeek.com/basketball-plays/switch-defense/",sourceName="The Hoops Geek",
 tags=["pre-switch","switch","mismatch","פרי-סוויץ'","החלפה מוקדמת"],
 diagram={"court":"half","steps":[
  {"caption":"5 מתחיל לעלות לחסום; x2 ו-x5 מתחלפים מראש: x2 לוקח את 5, x5 יוצא ל-2.","players":s1,
   "actions":[A("cut","5",[[24,20],[27.5,28.5]]),A("cut","x2",[[20,16],[26,25]]),A("cut","x5",[[15,17],[10,21]])]},
  {"caption":"עכשיו הסוויץ' על הפיק אנד רול הוא בין x1 ל-x2 – שני שומרים קטנים.","players":s2,
   "actions":[A("dribble","1",[[31,27],[34,22]]),A("cut","x2",[[31,26]]),A("cut","x1",[[27,24]]),A("cut","5",[[27,17],[25,9]])]}]})})
# 4 Defending Spain
s1=[P("1","O",25,30,True),P("x1","X",24.5,28),P("5","O",27,28.5),P("x5","X",26,25),P("2","O",25,19),P("x2","X",24,16),P("3","O",3,3),P("4","O",47,3)]
s2=[P("1","O",35,22,True),P("x1","X",30,27),P("5","O",26,14),P("x5","X",26,25),P("2","O",26,22),P("x2","X",24,17),P("3","O",3,3),P("4","O",47,3)]
items.append({"id":"cov-spain","data":dict(base,name="Defending Spain P&R (Drop Under + Switch)",level="בוגרים",players="3 על 3 + קלעים",leagues=["NBA"],
 description="נגד ספיין: השומר של הביג (x5) יורד מתחת לבק-סקרין ונשאר עם הרולר. השומר של מציב הבק-סקרין (x2) מחליף לכדרר, והשומר של הכדרר (x1) מחליף לשחקן שיוצא לשלשה אחרי הבק-סקרין.",
 points=["x5 יורד מתחת לבק-סקרין – לא נלחם דרכו","x2 לוקח את הכדור, x1 לוקח את מי שפותח לשלשה","מי שרואה את הסטאק קורא 'ספיין!' מוקדם"],
 source="https://rohitnaimpally.substack.com/p/can-the-wolves-go-spanish",sourceName="Rohit Naimpally (Substack)",
 tags=["spain","defending spain","stack","ספיין","הגנה על ספיין"],
 diagram={"court":"half","steps":[
  {"caption":"1 יוצא מהחסימה של 5, 5 מתגלגל ו-2 בא להציב בק-סקרין על x5.","players":s1,
   "actions":[A("dribble","1",[[31,27],[35,22]]),A("cut","5",[[27,20],[26,14]]),A("screen","2",[[26,22]])]},
  {"caption":"x5 עובר מתחת לבק-סקרין ונשאר עם 5; x2 מחליף לכדור, ו-x1 מחליף ל-2 שפותח לשלשה.","players":s2,
   "actions":[A("cut","x5",[[23,21],[25,13]]),A("cut","x2",[[30,20],[34,21]]),A("cut","2",[[24,30]]),A("cut","x1",[[25,28]])]}]})})
# 5-7 DHO
dho=dict(base,level="נוער",players="2 על 2",leagues=["FIBA","NCAA","NBA"],source="https://wabc.fiba.com/?p=1302",sourceName="FIBA WABC")
s1=[P("1","O",36,26,True),P("x1","X",34,24),P("2","O",45,12),P("x2","X",43,13)]
s2=[P("1","O",36,26,True),P("x1","X",34,24),P("2","O",41,21),P("x2","X",38,24)]
items.append({"id":"dho-def-jump","data":dict(dho,name="DHO Defense – Jump (Deny the Handoff)",
 description="כש-2 רץ ישר ליד 1 לקבל הנד-אוף, השומר שלו (x2) קופץ לנתיב ונעמד בין 2 ל-1, כך שההנד-אוף לא יכול לקרות. אם 2 חותך בקדור, x2 הולך איתו. אם x2 נתקע מאחורי 1, x1 לוקח את החיתוך ו-x2 עובר ל-1.",
 points=["הקפיצה רק כש-2 עובר ישר ליד 1","להישאר בין 2 ל-1, לא מאחורי 2","תקשורת על הבקדור: מי שקרוב לוקח אותו"],
 tags=["dho","handoff","jump","הנד-אוף","הגנה על הנד-אוף"],
 diagram={"court":"half","steps":[
  {"caption":"2 רץ לקבל הנד-אוף מ-1; x2 קופץ לנתיב ונעמד בין 2 ל-1.","players":s1,
   "actions":[A("cut","2",[[43,18],[41,21]]),A("cut","x2",[[40,21],[38,24]])]},
  {"caption":"2 חותך בקדור – x2 הולך איתו (או x1 לוקח אותו אם x2 נתקע).","players":s2,
   "actions":[A("cut","2",[[39,14],[30,8]]),A("cut","x2",[[37,15],[31,9]])]}]})})
s1=[P("1","O",36,26,True),P("x1","X",34,24),P("2","O",41,22),P("x2","X",42,20)]
s2=[P("1","O",33,29),P("x1","X",37,22),P("2","O",36,24,True),P("x2","X",36,26)]
items.append({"id":"dho-def-show","data":dict(dho,name="DHO Defense – Show and Recover",
 description="ברגע ההנד-אוף, השומר של מוסר הכדור (x1) יוצא לרגע לנתיב של מקבל הכדור ועוצר אותו מלהסתובב לכיוון הצבע. זה נותן ל-x2 זמן לחזור ל-2, ואז x1 חוזר מיד לשחקן שלו.",
 points=["צעד מהיר לנתיב ומיד חזרה","x2 עובר צמוד מאחורי ההנד-אוף","לא להישאר שניים על הכדור"],
 tags=["dho","handoff","show","הנד-אוף","שואו"],
 diagram={"court":"half","steps":[
  {"caption":"1 מוסר ביד ל-2; x1 יוצא לנתיב של 2 ועוצר את הסיבוב פנימה, x2 עובר ונצמד ל-2.","players":s1,
   "actions":[A("handoff","1",to="2"),A("cut","x1",[[37,22]]),A("cut","x2",[[39,25],[36,26]])]},
  {"caption":"x1 חוזר מיד ל-1; x2 כבר על 2.","players":s2,
   "actions":[A("cut","x1",[[34,27]]),A("cut","x2",[[35,23]])]}]})})
s1=[P("1","O",36,26,True),P("x1","X",34,24),P("2","O",41,22),P("x2","X",42,20)]
items.append({"id":"dho-def-switch","data":dict(dho,name="DHO Defense – Switch",
 description="בהנד-אוף בין שני גארדים: השומר של המוסר (x1) לוקח את מקבל הכדור, והשומר של המקבל (x2) לוקח את המוסר. אם ההתקפה מוסיפה חוסם להנד-אוף, אפשר ש-x4 יעשה ג'אם על החסימה ו-x2 יעבור מתחת, או ש-x4 יחליף לכדור כשהשעון קצר.",
 points=["השומרים 'נפגשים' בהחלפה כדי שלא ייפתח רווח לחדירה","הכי מתאים להנד-אוף בין שני גארדים","עם חוסם נוסף: ג'אם ומתחת, או החלפה של הביג"],
 tags=["dho","handoff","switch","הנד-אוף","סוויץ'"],
 diagram={"court":"half","steps":[
  {"caption":"1 מוסר ביד ל-2; x1 לוקח את 2 ו-x2 לוקח את 1, צמודים בלי רווח.","players":s1,
   "actions":[A("handoff","1",to="2"),A("cut","x1",[[37,23]]),A("cut","x2",[[38,25],[35,27]]),A("cut","1",[[32,29]])]}]})})
json.dump(items,open('/home/claude/lib/new_pnr_def.json','w'),ensure_ascii=False,indent=1)
print(len(items))
