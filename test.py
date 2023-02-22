import re
import modules
S = modules.read_file("tables.py")
chunks = []
var = []
curr = 0
for i in S.split("\n\n"):
    if(i.startswith("class") == False):
        if("table_dict" in i):
            continue
        chunks[curr] += "\n\n" + i + "\n"
        curr += 1
        continue
    chunks.append(i)
    i = i.split("\n")[2]
    res = re.findall(r"self.(.*?) |,", i)
    res[-1] = res[-1] + ","
    var.append(res)
    print(res)
res = ""
for i in range(len(chunks)):
    S = "['" + " '".join(var[i])
    S = S.replace(",", ",'") + "]"
    res += chunks[i] + f"\n    items = {S}\n\n"
print(res)
modules.write_file("tables.py", res)
# for i in range(len(chunks)):
#     S = ""
#     for a in var[i]:
#         a = a[:-1]
#         temp = "{self."
#         a1 = a + "}"
#         S += f"{a}:{temp}{a1}\\n"
#     chunks[i] = chunks[i].replace("str(self.args)", f"f'{S}'")
# S = "\n".join(chunks)
# print(S)