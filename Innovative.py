from tkinter import *

window = Tk()
window.title("Functional Dependency Calculator")
window.geometry("1500x600")

elelabel = Label(window, text="Enter elements: ", font=('Georgia', 12))
elelabel.grid(row=1, column=0, padx=3, pady=10, sticky=W)
eledata = StringVar()
eletextbox = Entry(window, textvariable=eledata, font=('Georgia', 12))
eletextbox.grid(row=1, column=1, sticky=W)
ex1label = Label(window, text="E.g. A, B, C, D", font=('Georgia', 12))
ex1label.grid(row=1, column=2, padx=3, pady=10, sticky=W)

fdlabel = Label(window, text="Enter functional dependency: ", font=('Georgia', 12))
fdlabel.grid(row=2, column=0, padx=3, pady=10, sticky=W)
fddata = StringVar()
fdtextbox = Entry(window, textvariable=fddata, font=('Georgia', 12))
fdtextbox.grid(row=2, column=1, sticky=W)
fdlabel = Label(window, text="E.g. A -> BC, C -> BD", font=('Georgia', 12))
fdlabel.grid(row=2, column=2, padx=3, pady=10, sticky=W)

def input():
    global li, n, dic, m
    li = eledata.get()
    li = li.split(", ")
    n = len(li)
    str = fddata.get()
    str = str.split(", ")
    dic = {}
    for i in str:
        x = i.split(" -> ")
        dic.update({x[0]: x[1]})
    m = len(dic)
    return li, n, dic, m

def closure(li, dic):
    li_set = []
    li_setnew = []
    li_new = []
    for e in li:
        li_set.append(set(e))
        li_setnew.append(set(e))
        li_new.append(e)

    for f in dic.keys():
        if f not in li:
            li_setnew.append(set(f))
            li_new.append(f)

    def upd(set_ele, dic):
        old = set_ele
        for k in dic:
            if set(k).issubset(set_ele):
                set_ele = set_ele | set(dic[k])
        while old != set_ele:
            old = set_ele
            for k in dic:
                if set(k).issubset(set_ele):
                    set_ele = set_ele | set(dic[k])
        ans = ""
        for i in set_ele:
            ans += i
        return ans

    ans = {}
    ans_new = {}
    for i in range(len(li_set)):
        ans[li[i]] = upd(li_set[i], dic)

    for i in range(len(li_setnew)):
        ans_new[li_new[i]] = upd(li_setnew[i], dic)
    return ans_new

def candidateKey(ans, li, dic):
    ck = []
    notleftright = []
    onlyright = []
    onlyleft = []

    for ele in li:
        f = 0
        for j in dic:
            if ele in dic[j] or ele in j:
                f = 1
                break
        if f == 0:
            notleftright.append(ele)
    for ele in li:
        f = 0
        y = 0
        for j in dic:
            if ele in j:
                f = 1
                break
        for k in dic:
            if ele in dic[k]:
                y = 1
                break
        if y == 0 and f == 1:
            onlyleft.append(ele)
    for ele in li:
        f = 0
        y = 0
        for j in dic:
            if ele in dic[j]:
                f = 1
                break
        for k in dic:
            if ele in k:
                y = 1
                break
        if y == 0 and f == 1:
            onlyright.append(ele)

    mergenlrol = notleftright + onlyleft

    tempck = []
    for ele in mergenlrol:
        x = ans[ele]
        for i in range(len(x)):
            tempck.append(x[i])
    for ele in dic:
        f = 0
        tl = list(ele)
        for i in tl:
            if i not in tempck:
                f = 1
                break
        if f == 0:
            x = dic[ele]
            for i in range(len(x)):
                tempck.append(x[i])

    if len(set(tempck)) == n:
        ck.append(mergenlrol)
        return ck
    else:
        ck = []
        notmergeonlyright = []
        for ele in li:
            if ele not in mergenlrol and ele not in onlyright:
                notmergeonlyright.append(ele)

        if len(mergenlrol) == 0:
            for ele in notmergeonlyright:
                for ele2 in notmergeonlyright:
                    if len(set(ans[ele] + ans[ele2])) == n:
                        ck.append((ele + ele2))
        else:
            for ele in notmergeonlyright:
                for ele2 in mergenlrol:
                    if len(set(ans[ele] + ans[ele2])) == n:
                        ck.append((ele + ele2))
        return ck

def canonicalCover():
    dic_new = {}
    dic_new1 = {}
    for i in dic.keys():
        dic_new[i] = list(dic[i])
        dic_new1[i] = list(dic[i])

    def upd(set_ele, dic):
        old = set_ele
        for k in dic:
            if set(k).issubset(set_ele):
                set_ele = set_ele | set(dic[k])
        while old != set_ele:
            old = set_ele
            for k in dic:
                if set(k).issubset(set_ele):
                    set_ele = set_ele | set(dic[k])
        ans = ""
        for i in set_ele:
            ans += i
        return ans

    for i in dic_new.keys():
        v = dic_new[i]
        if len(v) > 1:
            p = len(v)
        else:
            p = 1
        x = 0
        while p:
            a1 = upd(set(i), dic_new)
            dic_new1[i].pop(dic_new1[i].index(v[x]))
            a2 = upd(set(i), dic_new1)

            if a1 == a2:
                dic_new[i].pop(dic_new[i].index(v[x]))
            else:
                dic_new1[i].append(v[x])
                x += 1
            p = p - 1

    for i in dic_new.keys():
        if len(i) > 1:
            s = [char for char in i]
            for j in range(len(i)):
                a3 = upd(set(i), dic_new)
                a4 = upd(set(s[j]), dic_new)
                if a3 == a4:
                    dic_new[s[j]] = dic_new[i]
                    dic_new.pop(i)
    k = 0
    cv = ""
    for i in dic_new:
        for j in dic_new[i]:
            cv = cv+i+"->"+j+", "
            k += 1
    cv = cv[:-2]
    return cv

def run():
    global closure, ck
    li, n, dic, m = input()
    closure = closure(li, dic)
    ck = candidateKey(closure, li, dic)
    cv = canonicalCover()

    emptyLabel1.config(text="Closure:")
    emptyLabel2.config(text=closure)
    emptyLabel3.config(text="Candidate Key:")
    emptyLabel4.config(text=ck)
    emptyLabel5.config(text="Canonical Cover:")
    emptyLabel6.config(text=cv)

cbutton = Button(window, command=run, text="Compute", font=('Georgia', 12), fg='green')
cbutton.grid(row=3, column=0, padx=3, pady=5, sticky=W)
emptyLabel1 = Label(window, fg='navy', font=('Georgia', 12))
emptyLabel1.grid(row=4, column=0, sticky=W)
emptyLabel2 = Label(window, fg='navy', font=('Georgia', 12))
emptyLabel2.grid(row=4, column=1, sticky=W)
emptyLabel3 = Label(window, fg='navy', font=('Georgia', 12))
emptyLabel3.grid(row=5, column=0, sticky=W)
emptyLabel4 = Label(window, fg='navy', font=('Georgia', 12))
emptyLabel4.grid(row=5, column=1, sticky=W)
emptyLabel5 = Label(window, fg='navy', font=('Georgia', 12))
emptyLabel5.grid(row=6, column=0, sticky=W)
emptyLabel6 = Label(window, fg='navy', font=('Georgia', 12))
emptyLabel6.grid(row=6, column=1, sticky=W)

window.mainloop()

