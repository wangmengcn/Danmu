import sys
sys.path.append("..")
import calculate

sortsender = calculate.sortNames(calculate.senderrows, "sender_id")
count = calculate.senderrows.count()
value = []
name = []

for i in range(0, 19):
    contributer = sortsender[i]
    name.append(contributer[0])
    value.append(contributer[1])