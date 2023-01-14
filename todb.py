from app import db,reg

data= open('data1.csv')

header=data.readline()

while True:
    line = data.readline()
    if not line:
        break
    else:
        fl=line.split(",")
        print(fl)
        n= reg(
            timestamp=fl[0].strip('"'),
            name=fl[1].strip('"'),
            roll=int(fl[2].strip("\"")),
            course=fl[3].strip('"'),
            year=fl[4].strip('"'),
            phone=fl[5].strip('"'),
            email=fl[6].rstrip('"').lstrip('"')
        )
        db.session.add(n)

db.session.commit()