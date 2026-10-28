# test_phase2.py
from text_to_sql import TextToSQL

engine = TextToSQL()

questions = [
    #"Show me all open bugs assigned to user jdoe."
    "How many issues were created last month?"
    # "List the top 3 projects with the most unresolved issues.",
]

for q in questions:
    print(f"\n❓ Question: {q}")
    res = engine.ask(q)
    if res["error"]:
        print(f"❌ Error: {res['error']}")
    else:
        print(f"📝 SQL:\n{res['sql']}")
        print(f"📊 Results ({len(res['data'])} rows):")
        print(res["data"].to_markdown(index=False))