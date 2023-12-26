import sqlite3

#вывод полной фильтрованной таблицы
def MainFind(W1,W2,A1,A2,Win1,Win2):#,D):
    outData=[]
    with db:
        sql1=(f"""SELECT s.name, s.age, s.weight, s.height, s.name_coach, c.level, 
        COUNT(*)(c1.name) AS winCount, tl.dataListTrauma, tl.dedlinesList
        FROM sportsmens AS s
        JOIN coachs AS c ON s.name_coach = c.name
        JOIN competitions AS c1 ON (c1.first_name = s.name OR c1.second_name = s.name) AND c1.winner_name = s.name
        JOIN (
        SELECT t.name_sportsmen, MAX(t.date) AS dataListTrauma, MAX(t.deadline) AS dedlinesList
        FROM traumas AS t
        GROUP BY t.name_sportsmen
        ) AS tl ON s.name = tl.name_sportsmen
        WHERE s.weight > {W1} AND s.weight < {W2}
        AND s.age > {A1} AND s.age < {A2}
        AND winCount > {Win1} AND winCount < {Win2}
        AND c1.date > tl.dataListTrauma
        AND c1.date > DATE(tl.dataListTrauma, '+' || tl.dedlinesList || ' days')
        GROUP BY s.name;""")

        sql2=(f"""SELECT s.name, s.age, s.weight, s.height, s.name_coach, c.level AS lvl, 
        (SELECT COUNT(*) FROM competitions WHERE winner_name = s.name) AS winCount,
        GROUP_CONCAT(t.date) AS dataListTrauma,
        GROUP_CONCAT(t.deadline) AS dedlinesList
        FROM sportsmens AS s
        INNER JOIN coachs AS c ON s.name_coach = c.name
        LEFT JOIN traumas AS t ON s.name = t.name_sportsmen
        WHERE s.weight > {W1} AND s.weight < {W2}
        AND s.age > {A1} AND s.age < {A2}
        AND (SELECT COUNT(*) FROM competitions WHERE  winner_name = s.name) > {Win1}
        AND (SELECT COUNT(*) FROM competitions WHERE  winner_name = s.name) < {Win2}
        AND DATE(s.dataListTrauma || '+' || s.dedlinesList) < D
        GROUP BY s.name""")

        sql3=(f"""SELECT sportsmens.name, sportsmens.age, sportsmens.weight, sportsmens.height, sportsmens.name_coach, coachs.level AS lvl, (SELECT COUNT(*) FROM competitions WHERE winner_name = sportsmens.name) AS winCount,
         GROUP_CONCAT(traumas.date) AS dataListTrauma, GROUP_CONCAT(traumas.deadline) AS dedlinesList
        FROM sportsmens
        LEFT JOIN coachs ON sportsmens.name_coach = coachs.name
        LEFT JOIN competitions ON (competitions.winner_name = sportsmens.name)
        LEFT JOIN traumas ON traumas.name_sportsmen = sportsmens.name
        WHERE sportsmens.weight > {W1} AND sportsmens.weight < {W2}
        AND sportsmens.age > {A1} AND sportsmens.age < {A2}
        AND (SELECT COUNT(*) FROM competitions WHERE  winner_name = sportsmens.name) >= {Win1}
        AND (SELECT COUNT(*) FROM competitions WHERE  winner_name = sportsmens.name) < {Win2}
        GROUP BY sportsmens.name""")
        data=db.execute(sql3)
    result = data.fetchall()  # получение всех строк результата запроса

    # Преобразование результата в многомерный список
    for row in result:
        row_list = list(row)
        outData.append(row_list)

    print(outData)
    return outData

#вывод таблицы лучших спортсменов
def TheBestSportsmen():
    outData = []
    with db:
        sql1 = (f"""
        SELECT s.name, s.age, s.weight, s.height, s.name_coach, COUNT(*) AS winCount, GROUP_CONCAT(t.date) AS dataListTrauma, GROUP_CONCAT(t.deadline) AS dedlinesList
        FROM sportsmens s
        JOIN competitions c ON s.name = c.winner_name
        LEFT JOIN traumas t ON s.name = t.name_sportsmen
        GROUP BY s.name
        ORDER BY winCount DESC
        
""")

        sql2=(f"""
        SELECT s.name, s.age, s.weight, s.height, s.name_coach, COUNT(c.winner_name) AS winCount
        FROM sportsmens s
        LEFT JOIN competitions c ON s.name = c.winner_name
        GROUP BY s.name
        ORDER BY winCount DESC
        LIMIT 5;
""")
        data=db.execute(sql2)
    result = data.fetchall()  # получение всех строк результата запроса

    # Преобразование результата в многомерный список
    for row in result:
        row_list = list(row)
        outData.append(row_list)
    #for row in data:
        #outData.append(row)

    print(outData)
    return outData

#вывод таблицы лучших тренеров
def TheBestCoach():
    outData = []
    with db:
        sql1 = (f"""
        SELECT c.name, c.level, COUNT(comp.winner_name) AS winCount
        FROM coachs c
        JOIN sportsmens s ON c.name = s.name_coach
        LEFT JOIN competitions comp ON s.name = comp.winner_name
        GROUP BY c.name, c.level
        ORDER BY c.level DESC, winCount DESC
        LIMIT 5;        
""")
        sql2=(f"""
        SELECT c.name, c.level, COUNT(s.name) AS winCount
        FROM coachs c
        JOIN sportsmens s ON c.name = s.name_coach
        LEFT JOIN competitions comp ON s.name = comp.winner_name
        
        GROUP BY c.name
        ORDER BY c.level DESC
        LIMIT 5;
""")

        data=db.execute(sql1)
    result = data.fetchall()  # получение всех строк результата запроса

    # Преобразование результата в многомерный список
    for row in result:
        row_list = list(row)
        outData.append(row_list)
    print(outData)
    return outData

#добавление спортсменов
def InsertSportsmen (data):
    with db:
        if (data[0][1].isdigit() and data[0][2].isdigit() and data[0][3].isdigit()):
            data = [[data[0][0],int(data[0][1]),int(data[0][2]),int(data[0][3]),data[0][4]]]
            db.executemany("""INSERT INTO sportsmens (name, age, weight, height, name_coach) values(?, ?, ?, ?, ?)""", data)
            db.commit()
        else:
            pass

#добавление тренера
def InsertCoach (data):
    with db:
        if (data[0][1].isdigit()):
            data = [[data[0][0], int(data[0][1])]]
            db.executemany("""INSERT INTO coachs (name, level) values(?, ?)""", data)
            db.commit()
        else:
            pass

#добавление травмы
def InsertTrauma (data):
    with db:
        if (data[0][3].isdigit()):
            data = [[data[0][0],data[0][1],data[0][2], int(data[0][3])]]
        db.executemany("""INSERT INTO traumas (name_sportsmen, date, type, deadline) values(?, ?, ?, ?)""", data)
        db.commit()

#добавление соревнования
def InsertCompetition (data):
    with db:
        db.executemany("""INSERT INTO competitions (name, date, first_name, second_name, winner_name) values(?, ?, ?, ?, ?)""", data)
        db.commit()

#вывод таблицы
def InputData(str,db):
    outData=[]
    with db:
        data = db.execute("SELECT * FROM "+str)

    for row in data:
        outData.append(row)
    return outData

#вывод списка тренеров
def OutCoachsName():
    outData=[]
    with db:
        data = db.execute("SELECT name FROM coachs")
    for row in data:
        outData.append(row[0])
    #print(outData)
    return outData

#вывод списка спортсменов
def OutName():
    outData=[]
    with db:
        data = db.execute("SELECT name FROM sportsmens")
    for row in data:
        outData.append(row[0])
    #print(outData)
    return outData

#замена тренера
def ChangeSportsmenInfo(name,newCoach):
    with db:
        sql = f"UPDATE sportsmens SET name_coach = '{newCoach}'  WHERE name = '{name}' "
        db.execute(sql)
        db.commit()

#вывод всей инфы о спортсмене
def AllInfoSportsmen(name):
    outData=[]

    with db:
        sql = f"""SELECT s.name, s.age, s.weight, s.height, s.name_coach, c.level as lvl, COUNT(comp.winner_name) as winCount, GROUP_CONCAT(t.date) as listTraumas,GROUP_CONCAT(t.deadline) as listTraumas2
                FROM sportsmens s
                LEFT JOIN coachs c ON s.name_coach = c.name
                LEFT JOIN competitions comp ON s.name = comp.winner_name
                LEFT JOIN traumas t ON s.name = t.name_sportsmen
                WHERE s.name = '{name}'
                GROUP BY s.name;"""
        data=db.execute(sql)

    for row in data:
        outData.append(row)
    #print(outData)
    return outData


db=sqlite3.connect('test.db')
with db:
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS coachs (
        name TEXT PRIMARY KEY NOT NULL UNIQUE,
        level INTEGER NOT NULL
        );""")

    sql.execute("""CREATE TABLE IF NOT EXISTS sportsmens (
        name TEXT PRIMARY KEY NOT NULL UNIQUE,
        age INTEGER NOT NULL,
        weight INTEGER NOT NULL,
        height INTEGER NOT NULL,
        name_coach TEXT NOT NULL,
        
        FOREIGN KEY (name_coach) REFERENCES coachs(name)
        );""")

    sql.execute("""CREATE TABLE IF NOT EXISTS competitions (
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        first_name TEXT NOT NULL,
        second_name TEXT NOT NULL,
        winner_name TEXT NOT NULL,
        
        FOREIGN KEY (first_name) REFERENCES sportsmens(name),
        FOREIGN KEY (second_name) REFERENCES sportsmens(name),
        FOREIGN KEY (winner_name) REFERENCES sportsmens(name)
        );""")

    sql.execute("""CREATE TABLE IF NOT EXISTS traumas (
        name_sportsmen TEXT NOT NULL,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        deadline TEXT NOT NULL,
        
        FOREIGN KEY (name_sportsmen) REFERENCES sportsmens(name)
        );""")


dataInputSportsmens=[]
dataInputCoachs=[]
dataInputTraums=[]
dataInputCompetitions=[]

dataInputSportsmens=InputData("sportsmens",db)
dataInputCoachs=InputData("coachs",db)
dataInputTraums=InputData("traumas",db)
dataInputCompetitions=InputData("competitions",db)


